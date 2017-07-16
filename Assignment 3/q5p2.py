import requests
import base64
from nacl import encoding, signing, public
from IPython import embed

API_TOKEN = 'cac5fe74adf74deec069bb8f929b13a8b28e9e8765f7f173f9db1c410c8f90c9'

psk_send_url = 'https://whoomp.cs.uwaterloo.ca/458a3/api/psk/send'
plain_inbox_url = 'https://whoomp.cs.uwaterloo.ca/458a3/api/plain/inbox'
psp_send_url = 'https://whoomp.cs.uwaterloo.ca/458a3/api/psp/send'
set_key_url = 'https://whoomp.cs.uwaterloo.ca/458a3/api/signed/set-key'
pke_set_key_url = 'https://whoomp.cs.uwaterloo.ca/458a3/api/pke/set-key'
pke_sent_url = 'https://whoomp.cs.uwaterloo.ca/458a3/api/pke/send'

SIGNING_KEY_FILE = 'signing.key'
VERIFY_KEY_FILE = 'verify.key'

JESSIE_PUBLIC_KEY_FILE = 'jessie.public.key'

PUBLIC_KEY_FILE = 'public.key'
PRIVATE_KEY_FILE = 'private.key'


private_key = public.PrivateKey.generate()
public_key = private_key.public_key

encoded_private_key = private_key.encode(encoder=encoding.Base64Encoder)
with open(PRIVATE_KEY_FILE, 'w+') as private_key_file:
	private_key_file.write(encoded_private_key)

encoded_public_key = public_key.encode(encoder=encoding.Base64Encoder)
with open(PUBLIC_KEY_FILE, 'w+') as public_key_file:
	public_key_file.write(encoded_public_key)

with open(JESSIE_PUBLIC_KEY_FILE) as jessie_public_key_file:
	encoded_jessie_public_key = jessie_public_key_file.read()
jessie_public_key = public.PublicKey(encoded_jessie_public_key, encoder=encoding.Base64Encoder)



data = {
	'api_token': API_TOKEN,
	'public_key': encoded_public_key
}

response = requests.post(
	url=pke_set_key_url,
	data=data,
)

print 'The response has status: {} {}'.format(response.status_code, response.reason)
messages = response.json()
print 'The response is: {}'.format(messages)




plaintext_message = 'Hello, World!'
box = public.Box(private_key, jessie_public_key)

encrypted_message = box.encrypt(plaintext_message)
processed_message = base64.b64encode(encrypted_message)


data = {
	'api_token': API_TOKEN,
	'to': 'jessie',
	'message': processed_message
}

response = requests.post(
	url=pke_sent_url,
	data=data,
)

print 'The response has status: {} {}'.format(response.status_code, response.reason)
messages = response.json()
print 'The response is: {}'.format(messages)