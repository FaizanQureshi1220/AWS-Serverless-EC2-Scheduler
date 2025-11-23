import json
import boto3
import os

EC2_INSTANCE_ID = os.environ.get('Instance_Id')


ec2 = boto3.client('ec2')


def Instance_state():
    if not EC2_INSTANCE_ID:
        return "error"
    
    try:
        response = ec2.describe_instances(InstanceIds=[EC2_INSTANCE_ID])
        
        reservations = response.get('Reservations')
        if reservations and reservations[0].get('Instances'):
            return reservations[0]['Instances'][0]['State']['Name']
        
        return None 
    
    except Exception as e:
        print(f"Error retrieving instance state: {e}")
        return "error"


def Start_Instance():

    print("Attempting to Start the Instance... : {EC2_INSTANCE_ID}")
    current_state = Instance_state()

    if current_state == "running":
        print("Instance {EC2_INSTANCE_ID} is already running.")
        return {
            'statusCode': 200,
            'body': json.dumps('Instance is already running')
        }

    try:
        if current_state == "stopped":
            print("Instance {EC2_INSTANCE_ID} is in 'stopped' state. Proceeding to start.")

            ec2.start_instances(InstanceIds=[EC2_INSTANCE_ID])
            print("Start command issued for Instance {EC2_INSTANCE_ID}. ")
            print("Waiting for the instance state to change to 'running' ...")

        return {
            'statusCode': 200,
            'body': json.dumps(f'Start attempt for instance {EC2_INSTANCE_ID} completed.')
        }

    except Exception as e:
        print("Error while Starting the Instance : {e}")
        raise



def Stop_Instance():

    print("Attempting to Stop the Instance... : {EC2_INSTANCE_ID}")
    current_state = Instance_state()

    if current_state == "stopped":
        print("Instance {EC2_INSTANCE_ID} is already stopped.")
        return {
            'statusCode': 200,
            'body': json.dumps('Instance is already stopped')
        }

    try:

        if current_state == "running":
            print("Instance {EC2_INSTANCE_ID} is in 'running' state. Proceeding to stop.")

            ec2.stop_instances(InstanceIds=[EC2_INSTANCE_ID])
            print("Stop command issued for Instance {EC2_INSTANCE_ID}. ")
            print("Waiting for the instance state to change to 'stopped' ...")

        return {
            'statusCode': 200,
            'body': json.dumps(f'Stop attempt for instance {EC2_INSTANCE_ID} completed.')
        }
    
    except Exception as e:
        print("Error while Stopping the Instance : {e}")
        raise



def lambda_handler (event , context) :

    if not EC2_INSTANCE_ID:
        print("ERROR: 'EC2_INSTANCE_ID' environment variable not set. Doing nothing.")
        return {
            'statusCode': 400,
            'body': json.dumps('Missing required "EC2_INSTANCE_ID" environment variable.')
        }
    
    action = event.get('action')


    if action == 'start':
        return Start_Instance()
    
    elif action == 'stop':
        return Stop_Instance()
    
    else:
        print("ERROR: Invalid action received: {action}")

        return {
            'statusCode': 400,
            'body': json.dumps('Invalid action. Use "start" or "stop".')
        }