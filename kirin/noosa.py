#encoding: utf-8

"""
    {
        "from"      : "a user id who shoot message",
        "timestamp" : "a timestamp",
        "topic_arn" : "a topic_arn",
        "content"   : "{
            "type"  : "text / photo / voice",
            "message" : "text or a link"
        }"
    }

"""

import json
from config import *
from boto.dynamodb2.table import Table

sqs = get_sqs()
sns = get_sns()
dynamo = get_dynamo()
chat_record_table = Table(CHAT_RECORD_TABLE,connection=dynamo)


"""
    Dequeue sqs message to dynamodb and push a notification to specific topic
"""

def noosa(queue):
    # retrieve message
    message_objects = sqs.receive_message(queue)
    if len(message_objects) == 0:
        return

    message_object = message_objects[0]
    # only accept raw message 
    json_string = message_object.get_body()
    message = json.loads(json_string)
    # push notification to user
    topic_arn = message['topic_arn']
    sns.publish(
        topic=topic_arn, 
        message=json_string
    )
    # store to dynamo db
    hash_key = md5(json_string)

    new_record = self.table.put_item(data={
        'RecordID'      : hash_key,
        'UserID'        : message['from'],
        'TopicARN'      : topic_arn,
        'JsonMessage'   : json_string,
        'Timestamp'     : message['timestamp']
    })
    
    # remove this message
    sqs.delete_message(queue, message_object)


def start_eating():
    queues = sqs.get_all_queues()
    while(1):
        for queue in queues:
            noosa(queue)

if __name__ == '__main__':
    print('A ' + noosa_name() + ' noosa starts eating.')
    start_eating()

else:
    print('Fatal Error: Noosa is a cup of yoghurt.')
    exit(0)





