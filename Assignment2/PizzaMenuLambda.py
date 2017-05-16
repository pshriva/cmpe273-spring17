import json
import uuid
import boto3

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('Pizza')

print "Loading functions.."

def lambda_handler(event,context):
    method = event['method']
    response = None
    if(method == 'POST'):
        response = createMenu(event,context)
    elif(method == 'PUT'):
        response = alterMenu(event,context)
    elif(method == 'GET'):
        response = getMenu(event,context)
    elif(method == 'DELETE'):
        response = removeMenu(event,context)
    return response
    
def createMenu(event,context):    
    
    store_name = event['body']['store_name']
    selection = event['body']['selection']
    size = event['body']['size']
    price = event['body']['price']
    store_hours = event['body']['store_hours']
    item = {
        'menu_id': str(uuid.uuid1()),
        'store_name': store_name,
        'selection': selection,
        'size': size,
        'sequence': ["selection","size"],
        'price': price,
        'store_hours' : store_hours
    }
    # write the menu items to the database
    table.put_item(Item=item)

    # create a response
    #response = "200 Ok"
    return "200 OK"
     
def getMenu(event,context):
    menu_id = event['params']['menu-id']
    result = table.get_item(
        Key= {
            'menu_id': menu_id
        }
    )
    response = result['Item']
    return response
    
def alterMenu(event,context): 
    
     result = table.update_item(
        Key= {
            'menu_id': event['params']['menu-id']
        },UpdateExpression="set selection = :val",
    ExpressionAttributeValues={
        ':val': event['body']['selection']
    },
    ReturnValues="UPDATED_NEW"
    )
     #response = "200 Ok"
     return "200 OK"
    
def removeMenu(event,context):
    
    menu_id = event['params']['menu-id']
    #pathParameters = event.get(pathParameters)
    # fetch todo from the database
    #menuId =  "cd8af4b8-36df-11e7-9e67-0a2f22f3a5b9"
    result = table.delete_item(
        Key= {
            'menu_id': menu_id
        }
    )
    #response = "200 Ok"
    return "200 OK"
