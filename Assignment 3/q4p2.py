import requests
import base64
from nacl import encoding, signing
from IPython import embed
from utils import API_TOKEN, PLAINTEXT_MESSAGE, load_certificate_keys, process_response

SIGNED_SEND_URL = 'https://whoomp.cs.uwaterloo.ca/458a3/api/signed/send'

# Load key pair
signing_key, encoded_signing_key, verify_key, encoded_verify_key = load_certificate_keys()

# Sign message
signed_message = signing_key.sign(PLAINTEXT_MESSAGE, encoder=encoding.Base64Encoder)
print 'Signed message is: {}'.format(signed_message)

# Submit message
data = {
	'api_token': API_TOKEN,
	'to': 'jessie',
	'message': signed_message
}

response = requests.post(
	url=SIGNED_SEND_URL,
	data=data,
)

# Process response
process_response(response)