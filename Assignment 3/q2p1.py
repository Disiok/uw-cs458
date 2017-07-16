import requests
import base64
import nacl
import nacl.secret
import nacl.utils

from utils import PLAINTEXT_MESSAGE, API_TOKEN, process_response

PSK = 'decaa3c85279cddd5fab45e6ee4aa7a2e746edada959823863c792e19cbf91aa'
PSK_SEND_URL = 'https://whoomp.cs.uwaterloo.ca/458a3/api/psk/send'

# Decode pre-shared key
decoded_psk = base64.b16decode(PSK.upper())
print 'Decoded psk is: {}'.format(decoded_psk)

# Create secret box
secret_box = nacl.secret.SecretBox(decoded_psk)

# Encrypt and encode message
encrypted_message = secret_box.encrypt(PLAINTEXT_MESSAGE)
print 'Encrypted message is: {}'.format(encrypted_message)

encoded_message = base64.b64encode(encrypted_message)
print 'Base 64 encoded encrypted message is: {}'.format(encoded_message)

# Send message
data = {
	'api_token': API_TOKEN,
	'to': 'jessie',
	'message': encoded_message
}

response = requests.post(
	url=PSK_SEND_URL,
	data=data,
)

# Process response
def decode_and_print_messages(messages):
	for message in messages:
		decoded_message = base64.b64decode(message['message'])
		print 'Message: {}'.format(decoded_message)

process_response(response, process_messages=decode_and_print_messages)