import requests
import base64

from utils import API_TOKEN, process_response

INBOX_URL = 'https://whoomp.cs.uwaterloo.ca/458a3/api/plain/inbox'


# Send inbox request
data = {
	'api_token': API_TOKEN,
}

response = requests.post(
	url=INBOX_URL,
	data=data,
)

# Process response
def decode_and_print_messages(messages):
	for message in messages:
		decoded_message = base64.b64decode(message['message'])
		print 'Message: {}'.format(decoded_message)

process_response(response, process_messages=decode_and_print_messages)

