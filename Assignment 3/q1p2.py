import requests
import base64

API_TOKEN = 'cac5fe74adf74deec069bb8f929b13a8b28e9e8765f7f173f9db1c410c8f90c9'

data = {
	'api_token': API_TOKEN,
}

inbox_url = 'https://whoomp.cs.uwaterloo.ca/458a3/api/plain/inbox'

response = requests.post(
	url=inbox_url,
	data=data,
)

print 'The response has status: {} {}'.format(response.status_code, response.reason)
messages = response.json()
print 'The response is: {}'.format(messages)

for message in messages:
	s = base64.b64decode(message['message'])
	print 'Message: {}'.format(s)