import json
import boto3

Instance_ID = ''


ec2 = boto3.client('ec2')


def Start_Instance():

    print("Attempting to Start the Instance... : {Instance_ID}")

    try:
        responce = ec2.describe_instances_status(InstanceIds=[Instance_ID])

        if (responce['InstanceStatuses'] and responce['InstanceStatuses'][0]['InstanceState']['Name'] == 'running'):
            print("Instance {Instance_ID} is already running.")
            return {
                'statusCode': 200,
                'body': json.dumps('Instance is already running')
            }
       

        ec2.start_instances(InstacesIds=[Instance_ID])
        print("Start command issued for Instance {Instance_ID}. ")
        print("Waiting for the instance state to change to 'running' ...")

    except Exception as e:
        print("Error while Starting the Instance : {e}")
        raise



def Stop_Instance():

    print("Attempting to Stop the Instance... : {Instance_ID}")

    try:
        responce = ec2.describe_instances_status(InstanceIds=[Instance_ID])
        if (responce['InstanceStatuses'] and responce['InstanceStatuses'][0]['InstanceState']['Name'] in ('stopped', 'terminated')):
            print("Instance {Instance_ID} is already stopped or Terminated.")
            return {
                'statusCode': 200,
                'body': json.dumps('Instance is already stopped or Terminated')
            }
        
        
        ec2.stop_instances(InstanceIds=[Instance_ID])
        print("Stop command issued for Instance {Instance_ID}. ")        
        
        return {
            'statusCode': 200,
            'body': json.dumps('Instance stop command sent.')
        }
        

    except Exception as e:
        print("Error while Stopping the Instance : {e}")
        raise



def lambda_handler (event , context) :

    action = event.get('action')

    if not action:
        print("ERROR: 'action' key not found in event payload. Doing nothing.")
        return {
            'statusCode': 400,
            'body': json.dumps('Missing required "action" parameter.')
        }
    

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