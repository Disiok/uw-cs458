import requests
import base64
from nacl import encoding, signing, public
from IPython import embed

from utils import API_TOKEN, JESSIE_PUBLIC_KEY_FILE, PLAINTEXT_MESSAGE, generate_and_save_encryption_keys, process_response

pke_set_key_url = 'https://whoomp.cs.uwaterloo.ca/458a3/api/pke/set-key'
pke_sent_url = 'https://whoomp.cs.uwaterloo.ca/458a3/api/pke/send'

# Generate and save encryption key pair
private_key, encoded_private_key, public_key, encoded_public_key = generate_and_save_encryption_keys()

# Send key
data = {
	'api_token': API_TOKEN,
	'public_key': encoded_public_key
}

response = requests.post(
	url=pke_set_key_url,
	data=data,
)

# Process response
process_response(response)

# Load Jessie public key
with open(JESSIE_PUBLIC_KEY_FILE) as jessie_public_key_file:
	encoded_jessie_public_key = jessie_public_key_file.read()
jessie_public_key = public.PublicKey(encoded_jessie_public_key, encoder=encoding.Base64Encoder)

# Create box
box = public.Box(private_key, jessie_public_key)

# Encrypt and encode message
encrypted_message = box.encrypt(PLAINTEXT_MESSAGE)
encoded_message = base64.b64encode(encrypted_message)

# Send message
data = {
	'api_token': API_TOKEN,
	'to': 'jessie',
	'message': encoded_message
}

response = requests.post(
	url=pke_sent_url,
	data=data,
)

process_response(response)