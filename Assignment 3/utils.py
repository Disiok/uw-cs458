from nacl import encoding, signing, public

# Basic
PLAINTEXT_MESSAGE = 'Hello, World!'

# API Key
API_TOKEN = 'cac5fe74adf74deec069bb8f929b13a8b28e9e8765f7f173f9db1c410c8f90c9'

# Key Files
SIGNING_KEY_FILE = 'signing.key'
VERIFY_KEY_FILE = 'verify.key'

PUBLIC_KEY_FILE = 'public.key'
PRIVATE_KEY_FILE = 'private.key'

JESSIE_PUBLIC_KEY_FILE = 'jessie.public.key'

def save_key(key, key_file_path):
	encoded_key = key.encode(encoder=encoding.Base64Encoder)
	with open(key_file_path, 'w+') as key_file:
		key_file.write(encoded_key)

	return encoded_key


def generate_and_save_encryption_keys():
	private_key = public.PrivateKey.generate()
	public_key = private_key.public_key

	encoded_private_key = save_key(private_key, PRIVATE_KEY_FILE)
	encoded_public_key = save_key(public_key, PUBLIC_KEY_FILE)

	return private_key, encoded_private_key, public_key, encoded_public_key


def generate_and_save_certificate_keys():
	signing_key = signing.SigningKey.generate()
	verify_key = signing_key.verify_key

	encoded_signing_key = save_key(signing_key, SIGNING_KEY_FILE)
	encoded_verify_key = save_key(verify_key, VERIFY_KEY_FILE)

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