from nacl import encoding, signing

# Basic
PLAINTEXT_MESSAGE = 'Hello, World!'

# API Key
API_TOKEN = 'cac5fe74adf74deec069bb8f929b13a8b28e9e8765f7f173f9db1c410c8f90c9'

# Key Files
SIGNING_KEY_FILE = 'signing.key'
VERIFY_KEY_FILE = 'verify.key'

JESSIE_PUBLIC_KEY_FILE = 'jessie.public.key'

def generate_and_save_certificate_keys():
	signing_key = signing.SigningKey.generate()
	verify_key = signing_key.verify_key

	encoded_signing_key = signing_key.encode(encoder=encoding.Base64Encoder)
	with open(SIGNING_KEY_FILE, 'w+') as signing_key_file:
		signing_key_file.write(encoded_signing_key)

	encoded_verify_key = verify_key.encode(encoder=encoding.Base64Encoder)
	with open(VERIFY_KEY_FILE, 'w+') as verify_key_file:
		verify_key_file.write(encoded_verify_key)

	return signing_key, encoded_signing_key, verify_key, encoded_verify_key

def load_certificate_keys():
	with open(SIGNING_KEY_FILE) as signing_key_file:
		encoded_signing_key = signing_key_file.read()

	with open(VERIFY_KEY_FILE) as verify_key_file:
		encoded_verify_key = verify_key_file.read()

	signing_key = signing.SigningKey(encoded_signing_key, encoder=encoding.Base64Encoder)
	verify_key = signing.VerifyKey(encoded_verify_key, encoder=encoding.Base64Encoder)

	return signing_key, encoded_signing_key, verify_key, encoded_verify_key

def process_response(response, process_messages=None):
	print 'The response has status: {} {}'.format(response.status_code, response.reason)
	
	messages = response.json()
	print 'The response is: {}'.format(messages)

	if process_messages:
		process_messages(messages)