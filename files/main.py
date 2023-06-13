from googleapiclient import discovery
from google.cloud import asset_v1
import google.auth
import re
import datetime as dt
import os, sys
import google.auth.transport.requests
import google.oauth2.id_token
import requests
from multiprocessing import Pool
import json
from slack_sdk.webhook import WebhookClient
import traceback


# notification function

def webhook_notification(message):
    webhook_url = os.environ.get("WEBHOOK_URL")
    error_msg = "INFO: " + message
    webhook = WebhookClient(webhook_url)
    with open("payload.json", "rt") as block_payload:
        payload = json.load(block_payload)
    msg = {"type": "section", "text": {"type": "mrkdwn", "text": error_msg}}
    payload.append(msg)
    slack_data = json.dumps(payload)
    response = webhook.send(blocks=slack_data)


# Check the state of an image (ACTIVE, DEPRECATED, OBSOLETE)
def check_latest_image(source_image, project, service):
    try:
        image_request = service.images().get(project=project, image=source_image)
        response = image_request.execute()
        if "deprecated" in response.keys():
            return 1, response['deprecated']['state']
        else:
            return 0, "ACTIVE"
    # For images which are from marketplace
    except Exception as exception:
        print(f"Error: {str(exception)}")
        return 1, "OBSOLETE"


# when function is async triggering itself
def call_from_lambda(request_json, credentials):
    compute_service = discovery.build('compute', 'v1', credentials=credentials)
    project_id = list(request_json.keys())[0]
    try:
        for instance in request_json[project_id].keys():
            # Get instance details
            response = compute_service.instances().get(project=project_id, zone=request_json[project_id][instance],
                                                       instance=instance).execute()
            if "labels" in response.keys():
                if "non-compliant" not in response["labels"].keys():
                    disk_name = response["disks"][0]["source"].split("/")[-1]

                    # Get disk details of a particular instance
                    disk_response = compute_service.disks().get(project=project_id,
                                                                zone=request_json[project_id][instance],
                                                                disk=disk_name).execute()
                    source_image = disk_response['sourceImage'].split("/")[-1]
                    image_project = disk_response['sourceImage'].split("/")[-4]

                    # Checking image state (ACTIVE, DECPRECATED, OBSOLETE)
                    status, image_state = check_latest_image(source_image, image_project, compute_service)
                    if status == 1 and image_state == "OBSOLETE":
                        instance_labels = response.get('labels', {})
                        instance_labels.update({'non-compliant': 'true'})
                        instances_set_labels_request_body = {
                            'labels': instance_labels,
                            'labelFingerprint': response.get('labelFingerprint')
                        }
                        instance_update_response = compute_service.instances().setLabels(project=project_id,
                                                                                         zone=request_json[project_id][
                                                                                             instance],
                                                                                         instance=instance,
                                                                                         body=instances_set_labels_request_body).execute()
                        print(f"Instance {instance} label has been updated")
            else:
                disk_name = response["disks"][0]["source"].split("/")[-1]

                # Get disk details of a particular instance
                disk_response = compute_service.disks().get(project=project_id, zone=request_json[project_id][instance],
                                                            disk=disk_name).execute()
                source_image = disk_response['sourceImage'].split("/")[-1]
                image_project = disk_response['sourceImage'].split("/")[-4]

                # Checking image state (ACTIVE, DECPRECATED, OBSOLETE)
                status, image_state = check_latest_image(source_image, image_project, compute_service)
                if status == 1 and image_state == "OBSOLETE":
                    instance_labels = response.get('labels', {})
                    instance_labels.update({'non-compliant': 'true'})
                    instances_set_labels_request_body = {
                        'labels': instance_labels,
                        'labelFingerprint': response.get('labelFingerprint')
                    }
                    instance_update_response = compute_service.instances().setLabels(project=project_id,
                                                                                     zone=request_json[project_id][
                                                                                         instance], instance=instance,
                                                                                     body=instances_set_labels_request_body).execute()
                    print(f"Instance {instance} label has been updated")
    except Exception as exception:
        exception_message = str(exception)
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = os.path.split(exception_traceback.tb_frame.f_code.co_filename)[1]
        webhook_notification(
            str(f"{exception_message} {exception_type} {filename}, Line {exception_traceback.tb_lineno}"))
        exit(1)
        raise


# Thread call the function asynchronously
def call_self(url, data, headers):
    try:
        requests.post(url=url, data=data, headers=headers)
    except Exception as exception:
        exception_message = str(exception)
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = os.path.split(exception_traceback.tb_frame.f_code.co_filename)[1]
        webhook_notification(
            str(f"{exception_message} {exception_type} {filename}, Line {exception_traceback.tb_lineno}"))
        exit(1)


# Get all the instances in a particular project
def get_instances(project_id, credentials):
    try:
        project_resource = "projects/{}".format(project_id)
        client = asset_v1.AssetServiceClient(credentials=credentials)

        # Call ListAssets v1 to list assets.
        response = client.list_assets(
            request={
                "parent": project_resource,
                "read_time": None,
                "asset_types": ["compute.googleapis.com/Instance"],
                "content_type": 1,
                "page_size": 500,
            }
        )

        instances = {}
        for asset in response:
            instances[asset.name.split("/")[-1]] = asset.name.split("/")[-3]
        # print(f"For project {project_id}, instances are: {instances}")   
        return instances
    except Exception as exception:
        exception_message = str(exception)
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = os.path.split(exception_traceback.tb_frame.f_code.co_filename)[1]
        webhook_notification(
            str(f"{exception_message} {exception_type} {filename}, Line {exception_traceback.tb_lineno}"))
        exit(1)


def validate_image(project, credentials):
    try:
        print("Part1 - Validating Images")
        print("Validating Compute Images")
        date = re.sub(r'-', "", str(dt.date.today() - dt.timedelta(days=30)))
        print(dt.date.today())
        service = discovery.build('compute', 'v1', credentials=credentials)
        request = service.images().list(project=project)
        while request is not None:
            response = request.execute()
            for image in response['items']:
                if "deprecated" in image:
                    if image['deprecated']['state'] == "DEPRECATED":
                        if (re.sub(r'|T.*|-|', "", image['labels']['deprecation_time']) <= date):
                            print(image['name'], ":", "is going to marked as obsolete as it's creation date is: ",
                                  image['creationTimestamp'])
                            deprecation_status_body = {
                                "state": "OBSOLETE",
                            }
                            deprecate_request = service.images().deprecate(project=project, image=image['name'],
                                                                           body=deprecation_status_body).execute()
                        else:
                            print(image['name'], ":", "is deprecated but not older than 30 days and creation date is: ",
                                  image['creationTimestamp'])
            request = service.images().list_next(previous_request=request, previous_response=response)
    except Exception as exception:
        exception_message = str(exception)
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = os.path.split(exception_traceback.tb_frame.f_code.co_filename)[1]
        webhook_notification(
            str(f"{exception_message} {exception_type} {filename}, Line {exception_traceback.tb_lineno}"))
        exit(1)


def call_from_scheduler(credentials):
    try:
        validate_image(os.environ.get('IMAGE_PROJECT_ID'), credentials)
        rm_service = discovery.build('cloudresourcemanager', 'v1', credentials=credentials)
        rm_request = rm_service.projects().list(filter="lifecycleState:ACTIVE", pageSize=200)
        all_projects = []

        while rm_request is not None:
            rm_response = rm_request.execute()
            for project in rm_response.get('projects', []):
                all_projects.append(project['projectId'])
            if "nextPageToken" in rm_response.keys():
                rm_request = rm_service.projects().list(filter="lifecycleState:ACTIVE", pageSize=200,
                                                        pageToken=rm_response['nextPageToken'])
            else:
                rm_request = None

        print(f"Total Active Project: {len(all_projects)}")

        thread_pool = Pool(processes=len(all_projects))
        service_url = f"https://{os.environ['FUNCTION_REGION']}-{os.environ['FUNCTION_PROJECT']}.cloudfunctions.net/{os.environ['FUNCTION_NAME']}"
        auth_req = google.auth.transport.requests.Request()
        id_token = google.oauth2.id_token.fetch_id_token(auth_req, service_url)
        headers = {"Authorization": f"Bearer {id_token}", "Content-Type": "application/json"}

        for project_id in all_projects:
            instances = get_instances(project_id, credentials)
            if instances:
                thread_pool.apply_async(call_self, args=[service_url, json.dumps({project_id: instances}), headers])
            else:
                print(f"No instance found under project:{project_id} . Skipping function trigger for this project")
    except Exception as exception:
        exception_message = str(exception)
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = os.path.split(exception_traceback.tb_frame.f_code.co_filename)[1]
        webhook_notification(
            str(f"{exception_message} {exception_type} {filename}, Line {exception_traceback.tb_lineno}"))
        exit(1)


def main(request):
    try:
        request_json = request.get_json()
        credentials, projectid = google.auth.default()
        if not request_json:
            call_from_scheduler(credentials)
            return f"Master Function executed successfully"
        else:

            print(f"Asynchronous trigger for project: {list(request_json.keys())[0]}")
            if request_json[list(request_json.keys())[0]]:
                call_from_lambda(request_json, credentials)
            return f"Worker Function executed successfully for project: {list(request_json.keys())[0]}"

        # return f'Function executed successfully'
    except Exception as exception:
        exception_message = str(exception)
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = os.path.split(exception_traceback.tb_frame.f_code.co_filename)[1]
        webhook_notification(
            str(f"{exception_message} {exception_type} {filename}, Line {exception_traceback.tb_lineno}"))
        exit(1)
