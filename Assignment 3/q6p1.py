import requests
import base64
from nacl import encoding, hash, signing, public, utils, secret
from IPython import embed

API_TOKEN = 'cac5fe74adf74deec069bb8f929b13a8b28e9e8765f7f173f9db1c410c8f90c9'

surveil_set_key_url = 'https://whoomp.cs.uwaterloo.ca/458a3/api/surveil/set-key'
surveil_get_key_url = 'https://whoomp.cs.uwaterloo.ca/458a3/api/surveil/get-key'
surveil_send_url = 'https://whoomp.cs.uwaterloo.ca/458a3/api/surveil/send'

PUBLIC_KEY_FILE = 'surveil_public.key'
PRIVATE_KEY_FILE = 'suveil_private.key'
JESSIE_PUBLIC_KEY_FILE = 'surveil_jessie.public.key'
GOVERNMENT_ENCODED_PUBLIC_KEY = 'jpdkKoSvoe99Q1ZwqnePAcbSW1sOgYGOS66q4kk6GSc='

# Generate key
private_key = public.PrivateKey.generate()
public_key = private_key.public_key

# Save key
encoded_private_key = private_key.encode(encoder=encoding.Base64Encoder)
with open(PRIVATE_KEY_FILE, 'w+') as private_key_file:
	private_key_file.write(encoded_private_key)

encoded_public_key = public_key.encode(encoder=encoding.Base64Encoder)
with open(PUBLIC_KEY_FILE, 'w+') as public_key_file:
	public_key_file.write(encoded_public_key)

# Send key
data = {
	'api_token': API_TOKEN,
	'public_key': encoded_public_key
}

response = requests.post(
	url=surveil_set_key_url,
	data=data,
)

print 'The response has status: {} {}'.format(response.status_code, response.reason)
messages = response.json()
print 'The response is: {}'.format(messages)

# Get Jessie key
data = {
	'api_token': API_TOKEN,
	'user': 'jessie'
}

response = requests.post(
	url=surveil_get_key_url,
	data=data,
)

print 'The response has status: {} {}'.format(response.status_code, response.reason)
messages = response.json()
print 'The response is: {}'.format(messages)

encoded_jessie_public_key = messages['public_key']
with open(JESSIE_PUBLIC_KEY_FILE, 'w+') as jessie_public_key_file:
	jessie_public_key_file.write(encoded_jessie_public_key)
	
jessie_public_key = public.PublicKey(encoded_jessie_public_key, encoder=encoding.Base64Encoder)
jessie_box = public.Box(private_key, jessie_public_key)


# Get government key
government_public_key = public.PublicKey(GOVERNMENT_ENCODED_PUBLIC_KEY, encoder=encoding.Base64Encoder)
government_box = public.Box(private_key, government_public_key)


# Plaintext message
plaintext_message = 'Hello, World!'

# Generate secret key
secret_key = utils.random(secret.SecretBox.KEY_SIZE)
secret_box = secret.SecretBox(secret_key)

# Encrypted message and secret key
encrypted_message = secret_box.encrypt(plaintext_message)
government_encrypted_secret_key = government_box.encrypt(secret_key)
jessie_encrypted_secret_key = jessie_box.encrypt(secret_key)


message = jessie_encrypted_secret_key + government_encrypted_secret_key + encrypted_message
encoded_message = base64.b64encode(message)


# Send message
data = {
	'api_token': API_TOKEN,
	'to': 'jessie',
	'message': encoded_message
}

response = requests.post(
	url=surveil_send_url,
	data=data,
)

print 'The response has status: {} {}'.format(response.status_code, response.reason)
messages = response.json()
print 'The response is: {}'.format(messages)

