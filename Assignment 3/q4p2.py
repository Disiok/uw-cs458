import requests
import base64
from nacl import encoding, signing
from IPython import embed

API_TOKEN = 'cac5fe74adf74deec069bb8f929b13a8b28e9e8765f7f173f9db1c410c8f90c9'

psk_send_url = 'https://whoomp.cs.uwaterloo.ca/458a3/api/psk/send'
plain_inbox_url = 'https://whoomp.cs.uwaterloo.ca/458a3/api/plain/inbox'
psp_send_url = 'https://whoomp.cs.uwaterloo.ca/458a3/api/psp/send'
set_key_url = 'https://whoomp.cs.uwaterloo.ca/458a3/api/signed/set-key'
signed_send_url = 'https://whoomp.cs.uwaterloo.ca/458a3/api/signed/send'

SIGNING_KEY_FILE = 'signing.key'
VERIFY_KEY_FILE = 'verify.key'

plaintext_message = 'Hello, World!'

with open(SIGNING_KEY_FILE) as signing_key_file:
	encoded_signing_key = signing_key_file.read()


with open(VERIFY_KEY_FILE) as verify_key_file:
	encoded_verify_key = verify_key_file.read()

signing_key = signing.SigningKey(encoded_signing_key, encoder=encoding.Base64Encoder)
verify_key = signing.VerifyKey(encoded_verify_key, encoder=encoding.Base64Encoder)


signed_message = signing_key.sign(plaintext_message, encoder=encoding.Base64Encoder)
print 'Signed message is: {}'.format(signed_message)


data = {
	'api_token': API_TOKEN,
	'to': 'jessie',
	'message': signed_message
}

response = requests.post(
	url=signed_send_url,
	data=data,
)

print 'The response has status: {} {}'.format(response.status_code, response.reason)
messages = response.json()
print 'The response is: {}'.format(messages)