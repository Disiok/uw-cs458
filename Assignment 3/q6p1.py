import requests
import base64
from nacl import encoding, hash, signing, public, utils, secret
from IPython import embed

from utils import API_TOKEN, PLAINTEXT_MESSAGE, PUBLIC_KEY_FILE, load_encryption_keys, process_response

SURVEIL_SET_KEY_URL = 'https://whoomp.cs.uwaterloo.ca/458a3/api/surveil/set-key'
SURVEIL_GET_KEY_URL = 'https://whoomp.cs.uwaterloo.ca/458a3/api/surveil/get-key'
SURVEIL_SEND_URL = 'https://whoomp.cs.uwaterloo.ca/458a3/api/surveil/send'

GOVERNMENT_ENCODED_PUBLIC_KEY = 'jpdkKoSvoe99Q1ZwqnePAcbSW1sOgYGOS66q4kk6GSc='

# Load encryption key pair
private_key, encoded_private_key, public_key, encoded_public_key = load_encryption_keys()

# Send key
data = {
	'api_token': API_TOKEN,
	'public_key': encoded_public_key
}

response = requests.post(
	url=SURVEIL_SET_KEY_URL,
	data=data,
)

process_response(response)

# Get Jessie public key
data = {
	'api_token': API_TOKEN,
	'user': 'jessie'
}

response = requests.post(
	url=SURVEIL_GET_KEY_URL,
	data=data,
)

process_response(response)

# Save Jessie public key
encoded_jessie_public_key = response.json()['public_key']
jessie_public_key_file_path = PUBLIC_KEY_FILE + '.' + 'surveil' + '.' + 'jessie'
with open(jessie_public_key_file_path, 'w+') as jessie_public_key_file:
	jessie_public_key_file.write(encoded_jessie_public_key)


# Create Jessie box	
jessie_public_key = public.PublicKey(encoded_jessie_public_key, encoder=encoding.Base64Encoder)
jessie_box = public.Box(private_key, jessie_public_key)

# Create government box
government_public_key = public.PublicKey(GOVERNMENT_ENCODED_PUBLIC_KEY, encoder=encoding.Base64Encoder)
government_box = public.Box(private_key, government_public_key)

# Create secret box
secret_key = utils.random(secret.SecretBox.KEY_SIZE)
secret_box = secret.SecretBox(secret_key)

# Encrypted message and secret key
encrypted_message = secret_box.encrypt(PLAINTEXT_MESSAGE)
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
	url=SURVEIL_SEND_URL,
	data=data,
)

process_response(response)