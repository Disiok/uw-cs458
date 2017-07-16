import requests
import base64
from nacl import encoding, signing, public
from IPython import embed

API_TOKEN = 'cac5fe74adf74deec069bb8f929b13a8b28e9e8765f7f173f9db1c410c8f90c9'

set_identity_url = 'https://whoomp.cs.uwaterloo.ca/458a3/api/prekey/set-identity-key'
set_signed_prekey_url = 'https://whoomp.cs.uwaterloo.ca/458a3/api/prekey/set-signed-prekey'

SIGNING_KEY_FILE = 'pre_signing.key'
VERIFY_KEY_FILE = 'pre_verify.key'

PUBLIC_KEY_FILE = 'pre_public.key'
PRIVATE_KEY_FILE = 'pre_private.key'

# Generate certificate key pairs
signing_key = signing.SigningKey.generate()
verify_key = signing_key.verify_key

# Save key pairs
encoded_signing_key = signing_key.encode(encoder=encoding.Base64Encoder)
with open(SIGNING_KEY_FILE, 'w+') as signing_key_file:
	signing_key_file.write(encoded_signing_key)

encoded_verify_key = verify_key.encode(encoder=encoding.Base64Encoder)
with open(VERIFY_KEY_FILE, 'w+') as verify_key_file:
	verify_key_file.write(encoded_verify_key)

# Submit verifying key
data = {
	'api_token': API_TOKEN,
	'public_key': encoded_verify_key
}

response = requests.post(
	url=set_identity_url,
	data=data,
)

print 'The response has status: {} {}'.format(response.status_code, response.reason)
messages = response.json()
print 'The response is: {}'.format(messages)

# Generate encryption key pairs
private_key = public.PrivateKey.generate()
public_key = private_key.public_key

# Save encryption key pairs
encoded_private_key = private_key.encode(encoder=encoding.Base64Encoder)
with open(PRIVATE_KEY_FILE, 'w+') as private_key_file:
	private_key_file.write(encoded_private_key)

encoded_public_key = public_key.encode(encoder=encoding.Base64Encoder)
with open(PUBLIC_KEY_FILE, 'w+') as public_key_file:
	public_key_file.write(encoded_public_key)
decoded_public_key = base64.b64decode(encoded_public_key)

# Sign prekey
signed_prekey = signing_key.sign(decoded_public_key, encoder=encoding.Base64Encoder)

# Submit signed prekey
data = {
	'api_token': API_TOKEN,
	'public_key': signed_prekey
}

response = requests.post(
	url=set_signed_prekey_url,
	data=data,
)

print 'The response has status: {} {}'.format(response.status_code, response.reason)
messages = response.json()
print 'The response is: {}'.format(messages)