import requests
import base64
from nacl import encoding, hash, signing, public, utils, secret
from IPython import embed

API_TOKEN = 'cac5fe74adf74deec069bb8f929b13a8b28e9e8765f7f173f9db1c410c8f90c9'

surveil_set_key_url = 'https://whoomp.cs.uwaterloo.ca/458a3/api/surveil/set-key'
surveil_get_key_url = 'https://whoomp.cs.uwaterloo.ca/458a3/api/surveil/get-key'
surveil_send_url = 'https://whoomp.cs.uwaterloo.ca/458a3/api/surveil/send'
surveil_inbox_url = 'https://whoomp.cs.uwaterloo.ca/458a3/api/surveil/inbox'

PUBLIC_KEY_FILE = 'surveil_public.key'
PRIVATE_KEY_FILE = 'suveil_private.key'
JESSIE_PUBLIC_KEY_FILE = 'surveil_jessie.public.key'
GOVERNMENT_ENCODED_PUBLIC_KEY = 'jpdkKoSvoe99Q1ZwqnePAcbSW1sOgYGOS66q4kk6GSc='


# Load private key
with open(PRIVATE_KEY_FILE) as private_key_file:
	encoded_private_key = private_key_file.read()
private_key = public.PrivateKey(encoded_private_key, encoder=encoding.Base64Encoder)

# Load Jessie key
with open(JESSIE_PUBLIC_KEY_FILE) as jessie_public_key_file:
	encoded_jessie_public_key = jessie_public_key_file.read()
jessie_public_key = public.PublicKey(encoded_jessie_public_key, encoder=encoding.Base64Encoder)

# Create box
jessie_box = public.Box(private_key, jessie_public_key)



data = {
	'api_token': API_TOKEN,
}

response = requests.post(
	url=surveil_inbox_url,
	data=data,
)

print 'The response has status: {} {}'.format(response.status_code, response.reason)
messages = response.json()
print 'The response is: {}'.format(messages)

for message in messages:
	encoded_message = message['message']
	decoded_message = base64.b64decode(encoded_message)
	embed()
	decrypted_message = box.decrypt(decoded_message)
	print 'Decrypted message is: {}'.format(decrypted_message)


