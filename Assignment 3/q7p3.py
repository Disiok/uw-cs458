import requests
import base64
from nacl import encoding, signing, public
from IPython import embed

from utils import API_TOKEN, PUBLIC_KEY_FILE, load_encryption_keys, load_key, process_response

PREKEY_INBOX_URL = 'https://whoomp.cs.uwaterloo.ca/458a3/api/prekey/inbox'

# Load encryption key pair
private_key, encoded_private_key, public_key, encoded_public_key = load_encryption_keys()

# Load Jessie public key
jessie_public_key, _ = load_key(public.PublicKey, PUBLIC_KEY_FILE + '.pre.jessie')

# Create box
box = public.Box(private_key, jessie_public_key)

# Send inbox request
data = {
	'api_token': API_TOKEN,
}

response = requests.post(
	url=PREKEY_INBOX_URL,
	data=data,
)

# Process response
def decode_decrypt_and_print_messages(messages):
	for message in messages:
		encrypted_message = base64.b64decode(message['message'])
		decrypted_message = box.decrypt(encrypted_message)
		print 'Decrypted message is: {}'.format(decrypted_message)

process_response(response, process_messages=decode_decrypt_and_print_messages)
