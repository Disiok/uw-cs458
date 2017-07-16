from nacl import encoding, signing, public

# Basic
PLAINTEXT_MESSAGE = 'Hello, World!'

# API Key
API_TOKEN = 'cac5fe74adf74deec069bb8f929b13a8b28e9e8765f7f173f9db1c410c8f90c9'

# Key Files
KEY_DIR = 'keys/'
SIGNING_KEY_FILE = KEY_DIR + 'signing.key'
VERIFY_KEY_FILE = KEY_DIR + 'verify.key'

PUBLIC_KEY_FILE = KEY_DIR + 'public.key'
PRIVATE_KEY_FILE = KEY_DIR + 'private.key'

def save_key(key, key_file_path):
	encoded_key = key.encode(encoder=encoding.Base64Encoder)
	with open(key_file_path, 'w+') as key_file:
		key_file.write(encoded_key)

	return encoded_key

def load_key(key_cls, key_file_path):
	with open(key_file_path) as key_file:
		encoded_key = key_file.read()

	key = key_cls(encoded_key, encoder=encoding.Base64Encoder)

	return key, encoded_key

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
	signing_key, encoded_signing_key = load_key(signing.SigningKey, SIGNING_KEY_FILE)
	verify_key, encoded_verify_key = load_key(signing.VerifyKey, VERIFY_KEY_FILE)

	return signing_key, encoded_signing_key, verify_key, encoded_verify_key

def load_encryption_keys():
	private_key, encoded_private_key = load_key(public.PrivateKey, PRIVATE_KEY_FILE)
	public_key, encoded_public_key = load_key(public.PublicKey, PUBLIC_KEY_FILE)

	return private_key, encoded_private_key, public_key, encoded_public_key

def process_response(response, process_messages=None):
	print 'The response has status: {} {}'.format(response.status_code, response.reason)
	
	messages = response.json()
	print 'The response is: {}'.format(messages)

	if process_messages:
		process_messages(messages)