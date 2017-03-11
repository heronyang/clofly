import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('user-pw')

response = table.get_item(
    Key={
        'user': 'test3',
    }
)
if 'Item' in response:
	item = response['Item']
	print("user exists!")
	quit()


table.put_item(
   Item={
        'user': 'test2',
        'pw': 'Abc123Def',
    }
)

table.delete_item(
    Key={
        'user': 'test2',
    }
)

# print(item)