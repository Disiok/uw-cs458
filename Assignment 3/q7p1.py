import requests
import base64
from nacl import encoding, signing, public
from IPython import embed

from utils import API_TOKEN, load_certificate_keys, process_response, load_encryption_keys

set_identity_url = 'https://whoomp.cs.uwaterloo.ca/458a3/api/prekey/set-identity-key'
set_signed_prekey_url = 'https://whoomp.cs.uwaterloo.ca/458a3/api/prekey/set-signed-prekey'

# Load certificate key pairs
signing_key, encoded_signing_key, verify_key, encoded_verify_key = load_certificate_keys()

# Submit verifying key
data = {
	'api_token': API_TOKEN,
	'public_key': encoded_verify_key
}

response = requests.post(
	url=set_identity_url,
	data=data,
)

process_response(response)

# Load encryption key pairs
private_key, encoded_private_key, public_key, encoded_public_key = load_encryption_keys()

# Decode public key
decoded_public_key = base64.b64decode(encoded_public_key)

# Sign public prekey
signed_prekey = signing_key.sign(decoded_public_key, encoder=encoding.Base64Encoder)

# Submit signed prekey
data = {
	'api_token': API_TOKEN,
	'public_key': signed_prekey
}

response = requests.post(
	url=set_signed_prekey_url,
	data=data,
)

process_response(response)