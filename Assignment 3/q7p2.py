import requests
import base64
from nacl import encoding, signing, public
from IPython import embed

from utils import API_TOKEN, VERIFY_KEY_FILE, process_response

GET_IDENTITY_URL = 'https://whoomp.cs.uwaterloo.ca/458a3/api/prekey/get-identity-key'
GET_PREKEY_URL = 'https://whoomp.cs.uwaterloo.ca/458a3/api/prekey/get-signed-prekey'

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

# Save Jessie signed prekey
encoded_signed_jessie_prekey = response.json()['public_key']
decoded_signed_jessie_prekey = base64.b64decode(encoded_signed_jessie_prekey)
jessie_prekey  = jessie_verify_key.verify(decoded_signed_jessie_prekey)
