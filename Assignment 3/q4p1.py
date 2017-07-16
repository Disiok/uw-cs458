import requests
import base64
from nacl import encoding, signing
from IPython import embed

API_TOKEN = 'cac5fe74adf74deec069bb8f929b13a8b28e9e8765f7f173f9db1c410c8f90c9'

psk_send_url = 'https://whoomp.cs.uwaterloo.ca/458a3/api/psk/send'
plain_inbox_url = 'https://whoomp.cs.uwaterloo.ca/458a3/api/plain/inbox'
psp_send_url = 'https://whoomp.cs.uwaterloo.ca/458a3/api/psp/send'
set_key_url = 'https://whoomp.cs.uwaterloo.ca/458a3/api/signed/set-key'

SIGNING_KEY_FILE = 'signing.key'
VERIFY_KEY_FILE = 'verify.key'


signing_key = signing.SigningKey.generate()
verify_key = signing_key.verify_key


encoded_signing_key = signing_key.encode(encoder=encoding.Base64Encoder)
with open(SIGNING_KEY_FILE, 'w+') as signing_key_file:
	signing_key_file.write(encoded_signing_key)

encoded_verify_key = verify_key.encode(encoder=encoding.Base64Encoder)
with open(VERIFY_KEY_FILE, 'w+') as verify_key_file:
	verify_key_file.write(encoded_verify_key)

data = {
	'api_token': API_TOKEN,
	'public_key': encoded_verify_key
}

response = requests.post(
	url=set_key_url,
	data=data,
)

print 'The response has status: {} {}'.format(response.status_code, response.reason)
messages = response.json()
print 'The response is: {}'.format(messages)