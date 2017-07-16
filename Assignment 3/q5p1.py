import requests
import base64
from nacl import encoding, hash
from IPython import embed

API_TOKEN = 'cac5fe74adf74deec069bb8f929b13a8b28e9e8765f7f173f9db1c410c8f90c9'

psk_send_url = 'https://whoomp.cs.uwaterloo.ca/458a3/api/psk/send'
plain_inbox_url = 'https://whoomp.cs.uwaterloo.ca/458a3/api/plain/inbox'
psp_send_url = 'https://whoomp.cs.uwaterloo.ca/458a3/api/psp/send'
set_key_url = 'https://whoomp.cs.uwaterloo.ca/458a3/api/signed/set-key'
signed_send_url = 'https://whoomp.cs.uwaterloo.ca/458a3/api/signed/send'
get_key_url = 'https://whoomp.cs.uwaterloo.ca/458a3/api/pke/get-key'

SIGNING_KEY_FILE = 'signing.key'
VERIFY_KEY_FILE = 'verify.key'
JESSIE_PUBLIC_KEY_FILE = 'jessie.public.key'

data = {
	'api_token': API_TOKEN,
	'user': 'jessie'
}

response = requests.post(
	url=get_key_url,
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