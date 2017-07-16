import requests
import base64
from nacl import encoding, hash
from IPython import embed

from utils import API_TOKEN, PUBLIC_KEY_FILE, process_response

GET_KEY_URL = 'https://whoomp.cs.uwaterloo.ca/458a3/api/pke/get-key'

# Send key request
data = {
	'api_token': API_TOKEN,
	'user': 'jessie'
}

response = requests.post(
	url=GET_KEY_URL,
	data=data,
)

# Process response
def save_public_key(messages):
	encoded_public_key = messages['public_key']
	user = messages['user']

	user_public_key_file_path = PUBLIC_KEY_FILE + '.' + user

	with open(user_public_key_file_path, 'w+') as user_public_key_file:
		user_public_key_file.write(encoded_public_key)
		
	decoded_public_key = base64.b64decode(encoded_public_key)
	finger_print = hash.blake2b(decoded_public_key)
	print 'Finger print is: {}'.format(finger_print)

process_response(response, process_messages=save_public_key)