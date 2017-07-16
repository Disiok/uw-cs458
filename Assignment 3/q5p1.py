import requests
import base64
from nacl import encoding, hash
from IPython import embed

from utils import API_TOKEN, JESSIE_PUBLIC_KEY_FILE

GET_KEY_URL = 'https://whoomp.cs.uwaterloo.ca/458a3/api/pke/get-key'

data = {
	'api_token': API_TOKEN,
	'user': 'jessie'
}

response = requests.post(
	url=GET_KEY_URL,
	data=data,
)

print 'The response has status: {} {}'.format(response.status_code, response.reason)
messages = response.json()
print 'The response is: {}'.format(messages)

encoded_public_key = messages['public_key']
with open(JESSIE_PUBLIC_KEY_FILE, 'w+') as jessie_public_key_file:
	jessie_public_key_file.write(encoded_public_key)
	
decoded_public_key = base64.b64decode(encoded_public_key)
finger_print = hash.blake2b(decoded_public_key)
print 'Finger print is: {}'.format(finger_print)