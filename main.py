import boto3
import sys

boto3.setup_default_session(profile_name='personal')
client = boto3.client('rds', region_name='us-west-1')


def create_rds_instance(name):
    try:
        response = client.create_db_instance(
            AllocatedStorage=5,
            DBInstanceClass='db.t2.micro',
            DBInstanceIdentifier=name,
            Engine='MySQL',
            MasterUserPassword='Password1',
            MasterUsername='admin01',
        )
        print(response)
    except Exception as e:
        print("Exceptiom!")
        print(e)
    return


def get_rds_instances():
    try:
        response = client.describe_db_instances(DBInstanceIdentifier='', Filters=[{'Name': 'engine', 'Values': ['MySQL']}])
        return response['DBInstances']
    except Exception as e:
        print(e)
    return


def print_instance_list(instance_list):
    print("Listing " + str(len(instance_list)) + " instances:")
    print("==================")
    for instance in instance_list:
        print(instance['DBInstanceIdentifier'])
        print(instance['DBInstanceClass'])
        print(instance['DBInstanceIdentifier'])
    print("==================")
    return


def check_if_instance_exists(instance_list, instance_name):
    for instance in instance_list:
        if instance['DBInstanceIdentifier'] == instance_name:
            return instance['DBInstanceClass'], instance['DBInstanceStatus']
    return None


def modify_instance(instance_name, new_instance_class):
    print("Modifying " + instance_name + " to be " + new_instance_class)
    try:
        response = client.modify_db_instance(DBInstanceIdentifier=instance_name, DBInstanceClass=new_instance_class,
                                             ApplyImmediately=True)
        print(response)
    except Exception as e:
        print(e)
    return


if __name__ == '__main__':

    if len(sys.argv) != 3:
        print("Incorrect arguments")
        print("python3 main.py <instance-name> <new-instance-class>")
        exit(1)
        
    my_instance_name = sys.argv[1]
    new_instance_type = sys.argv[2]

    my_instance_list = get_rds_instances()
    print_instance_list(my_instance_list)
    my_instance_type, my_instance_status = check_if_instance_exists(my_instance_list, my_instance_name)

    if my_instance_type == new_instance_type:
        print("Instance types match")
        exit(0)
    else:
        if my_instance_status == 'available':
            modify_instance(my_instance_name, new_instance_type)
        else:
            print("Instance status is not available")
            print("Current status is " + my_instance_status)
    print("Done!")
