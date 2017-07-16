import requests
import base64
from utils import API_TOKEN, PLAINTEXT_MESSAGE, process_response

PLAIN_SEND_URL = 'https://whoomp.cs.uwaterloo.ca/458a3/api/plain/send'


# Encode message
encoded_message = base64.b64encode(PLAINTEXT_MESSAGE)
print 'Base 64 encoded string is: {}'.format(encoded_message)

# Send message
data = {
	'api_token': API_TOKEN,
	'to': 'jessie',
	'message': encoded_message
}

response = requests.post(
	url=PLAIN_SEND_URL,
	data=data,
)

# Process response
process_response(response)