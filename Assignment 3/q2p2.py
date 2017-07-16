import requests
import base64
import nacl
import nacl.secret
import nacl.utils

from utils import API_TOKEN, process_response

PSK = 'decaa3c85279cddd5fab45e6ee4aa7a2e746edada959823863c792e19cbf91aa'
PSK_INBOX_URL = 'https://whoomp.cs.uwaterloo.ca/458a3/api/psk/inbox'

# Decode pre-shared key
decoded_psk = base64.b16decode(PSK.upper())
print 'Decoded psk is: {}'.format(decoded_psk)

# Create secret box
secret_box = nacl.secret.SecretBox(decoded_psk)

# Send inbox request
data = {
	'api_token': API_TOKEN,
}

response = requests.post(
	url=PSK_INBOX_URL,
	data=data
)

# Process response
def decode_decrypt_and_print_messages(messages):
	for message in messages:
		encrypted_message = base64.b64decode(message['message'])
		decrypted_message = secret_box.decrypt(encrypted_message)
		print 'Message: {}'.format(decrypted_message)

process_response(response, process_messages=decode_decrypt_and_print_messages)