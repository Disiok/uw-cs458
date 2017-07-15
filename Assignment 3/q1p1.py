import requests
import base64

API_TOKEN = 'cac5fe74adf74deec069bb8f929b13a8b28e9e8765f7f173f9db1c410c8f90c9'


message = 'Hello, World!'
message_b64 = base64.b64encode(message)
print 'Base 64 encoded string is: {}'.format(message_b64)


data = {
	'api_token': API_TOKEN,
	'to': 'jessie',
	'message': message_b64
}

url = 'https://whoomp.cs.uwaterloo.ca/458a3/api/plain/send'

response = requests.post(
	url,
	data=data,
)

print 'The response has status: {} {}'.format(response.status_code, response.reason)
print 'The response is: {}'.format(response.json())