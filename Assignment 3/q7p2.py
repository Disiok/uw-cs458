import requests
import base64
from nacl import encoding, signing, public
from IPython import embed

from utils import API_TOKEN, VERIFY_KEY_FILE, PRIVATE_KEY_FILE, PUBLIC_KEY_FILE, PLAINTEXT_MESSAGE, process_response, load_key, save_key

GET_IDENTITY_URL = 'https://whoomp.cs.uwaterloo.ca/458a3/api/prekey/get-identity-key'
GET_PREKEY_URL = 'https://whoomp.cs.uwaterloo.ca/458a3/api/prekey/get-signed-prekey'
SEND_URL = 'https://whoomp.cs.uwaterloo.ca/458a3/api/prekey/send'

# Get Jessie verify key
data = {
	'api_token': API_TOKEN,
	'user': 'jessie'
}

response = requests.post(
	url=GET_IDENTITY_URL,
	data=data,
)

process_response(response)

# Save Jessie verify key
encoded_jessie_verify_key = response.json()['public_key']
jessie_verify_key_file_path = VERIFY_KEY_FILE + '.' + 'jessie'
with open(jessie_verify_key_file_path, 'w+') as jessie_verify_key_file:
	jessie_verify_key_file.write(encoded_jessie_verify_key)

jessie_verify_key = signing.VerifyKey(encoded_jessie_verify_key, encoder=encoding.Base64Encoder)


# Get Jessie signed prekey
data = {
	'api_token': API_TOKEN,
	'user': 'jessie'
}

response = requests.post(
	url=GET_PREKEY_URL,
	data=data,
)

process_response(response)

# Verify Jessie signed prekey
encoded_signed_jessie_prekey = response.json()['public_key']
decoded_signed_jessie_prekey = base64.b64decode(encoded_signed_jessie_prekey)
jessie_prekey  = jessie_verify_key.verify(decoded_signed_jessie_prekey)

# Create and save public key
jessie_public_key = public.PublicKey(jessie_prekey)
jessie_public_key_file_path = PUBLIC_KEY_FILE + '.' + 'pre' + '.' + 'jessie'
save_key(jessie_public_key, jessie_public_key_file_path)

# Load private key
private_key, _ = load_key(public.PrivateKey, PRIVATE_KEY_FILE)

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
	url=SEND_URL,
	data=data,
)

process_response(response)
