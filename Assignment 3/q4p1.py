import requests
import base64
from nacl import encoding, signing
from IPython import embed

from utils import API_TOKEN, generate_and_save_certificate_keys, process_response


SET_KEY_URL = 'https://whoomp.cs.uwaterloo.ca/458a3/api/signed/set-key'

signing_key, encoded_signing_key, verify_key, encoded_verify_key = generate_and_save_certificate_keys()

data = {
	'api_token': API_TOKEN,
	'public_key': encoded_verify_key
}

response = requests.post(
	url=SET_KEY_URL,
	data=data,
)

process_response(response)