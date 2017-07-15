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
psp_inbox_url = 'https://whoomp.cs.uwaterloo.ca/458a3/api/psp/inbox'

plaintext_message = 'Hello, World!'
print 'Plaintext message is: {}'.format(plaintext_message)

decoded_salt = base64.b16decode(SALT.upper())

kdf = pwhash.kdf_scryptsalsa208sha256

key = kdf(secret.SecretBox.KEY_SIZE, PSP, decoded_salt, 
		  opslimit=OP_LIMIT, memlimit=MEM_LIMIT)
print 'Key is: {}'.format(key)

box = secret.SecretBox(key)

data = {
	'api_token': API_TOKEN,
}

response = requests.post(
	url=psp_inbox_url,
	data=data,
)

print 'The response has status: {} {}'.format(response.status_code, response.reason)
messages = response.json()
print 'The response is: {}'.format(messages)

for message in messages:
	encrypted_message = base64.b64decode(message['message'])
	decrypted_message = box.decrypt(encrypted_message)
	print 'Message: {}'.format(decrypted_message)