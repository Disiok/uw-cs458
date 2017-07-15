import requests
import base64
from nacl import pwhash, utils, secret

API_TOKEN = 'cac5fe74adf74deec069bb8f929b13a8b28e9e8765f7f173f9db1c410c8f90c9'
PSP = 'poor respondent'
SALT = '91da7bc55ad6846923316d99c171d3b16e518518fa32e7a461f4bf4be346c232'
OP_LIMIT = 524288
MEM_LIMIT = 16777216

psk_send_url = 'https://whoomp.cs.uwaterloo.ca/458a3/api/psk/send'
plain_inbox_url = 'https://whoomp.cs.uwaterloo.ca/458a3/api/plain/inbox'
psp_send_url = 'https://whoomp.cs.uwaterloo.ca/458a3/api/psp/send'

plaintext_message = 'Hello, World!'
print 'Plaintext message is: {}'.format(plaintext_message)

decoded_salt = base64.b16decode(SALT.upper())

kdf = pwhash.kdf_scryptsalsa208sha256

key = kdf(secret.SecretBox.KEY_SIZE, PSP, decoded_salt, 
		  opslimit=OP_LIMIT, memlimit=MEM_LIMIT)
print 'Key is: {}'.format(key)

box = secret.SecretBox(key)

nonce = utils.random(secret.SecretBox.NONCE_SIZE)
print 'Nonce is: {}'.format(nonce)

encrypted_message = box.encrypt(plaintext_message, nonce)
print 'Encrypted message is: {}'.format(encrypted_message)


recreated_key = kdf(secret.SecretBox.KEY_SIZE, PSP, decoded_salt, 
		  			opslimit=OP_LIMIT, memlimit=MEM_LIMIT)

recreated_box = secret.SecretBox(recreated_key)

decrypted_message = recreated_box.decrypt(encrypted_message)
print 'Decrypted message is: {}'.format(decrypted_message)

processed_message = base64.b64encode(encrypted_message)
print 'Base 64 encoded encrypted message is: {}'.format(processed_message)

data = {
	'api_token': API_TOKEN,
	'to': 'jessie',
	'message': processed_message
}

response = requests.post(
	url=psp_send_url,
	data=data,
)

print 'The response has status: {} {}'.format(response.status_code, response.reason)
messages = response.json()
print 'The response is: {}'.format(messages)

for message in messages:
	s = base64.b64decode(message['message'])
	print 'Message: {}'.format(s)