import requests
import base64
import nacl
import nacl.secret
import nacl.utils

API_TOKEN = 'cac5fe74adf74deec069bb8f929b13a8b28e9e8765f7f173f9db1c410c8f90c9'
PSK = 'decaa3c85279cddd5fab45e6ee4aa7a2e746edada959823863c792e19cbf91aa'

psk_send_url = 'https://whoomp.cs.uwaterloo.ca/458a3/api/psk/send'
plain_inbox_url = 'https://whoomp.cs.uwaterloo.ca/458a3/api/plain/inbox'

plaintext_message = 'Hello, World!'
print 'Plaintext message is: {}'.format(plaintext_message)

decoded_psk = base64.b16decode(PSK.upper())
print 'Decoded psk is: {}'.format(decoded_psk)

box = nacl.secret.SecretBox(decoded_psk)

nonce = nacl.utils.random(nacl.secret.SecretBox.NONCE_SIZE)
print 'Nonce is: {}'.format(nonce)

encrypted_message = box.encrypt(plaintext_message, nonce)
print 'Encrypted message is: {}'.format(encrypted_message)

decrypted_message = box.decrypt(encrypted_message)
print 'Decrypted message is: {}'.format(decrypted_message)

processed_message = base64.b64encode(encrypted_message)
print 'Base 64 encoded encrypted message is: {}'.format(processed_message)

data = {
	'api_token': API_TOKEN,
	'to': 'jessie',
	'message': processed_message
}

response = requests.post(
	url=psk_send_url,
	data=data,
)

print 'The response has status: {} {}'.format(response.status_code, response.reason)
messages = response.json()
print 'The response is: {}'.format(messages)

for message in messages:
	s = base64.b64decode(message['message'])
	print 'Message: {}'.format(s)