import requests
import base64
from nacl import encoding, hash, signing, public, utils, secret
from IPython import embed

from utils import API_TOKEN, PRIVATE_KEY_FILE, PUBLIC_KEY_FILE, load_key, process_response

SURVEIL_INBOX_URL = 'https://whoomp.cs.uwaterloo.ca/458a3/api/surveil/inbox'

# Load private key
private_key, _ = load_key(public.PrivateKey, PRIVATE_KEY_FILE)

# Load Jessie public key
jessie_surveil_public_key_file_path = PUBLIC_KEY_FILE + '.' + 'surveil' + '.' + 'jessie'
jessie_public_key, _ = load_key(public.PublicKey, jessie_surveil_public_key_file_path)

# Create box
jessie_box = public.Box(private_key, jessie_public_key)

# Send inbox request
data = {
	'api_token': API_TOKEN,
}

response = requests.post(
	url=SURVEIL_INBOX_URL,
	data=data,
)

# Process response
def decode_decrypt_and_print_messages(messages):
	for message in messages:
		encoded_message = message['message']
		decoded_message = base64.b64decode(encoded_message)

		recipient_ciphertext = decoded_message[:72]
		government_ciphertext = decoded_message[72:144]
		message_ciphertext = decoded_message[144:]

		secret_key = jessie_box.decrypt(recipient_ciphertext)
		print 'Secret key is: {}'.format(secret_key)

		secret_box = secret.SecretBox(secret_key)

		decrytped_message = secret_box.decrypt(message_ciphertext)
		print 'Decrypted message is {}'.format(decrytped_message)


process_response(response, process_messages=decode_decrypt_and_print_messages)



