# Install a pip package in the current Jupyter kernel
import sys
#!{sys.executable} -m pip install python-jose

import json
from jose import jwt
from urllib.request import urlopen

# Configuration
# UPDATE THIS TO REFLECT YOUR AUTH0 ACCOUNT
AUTH0_DOMAIN = 'simoennova.eu.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'image'

# Link per il Token JWT
# https://simoennova.eu.auth0.com/authorize?audience=image&response_type=token&client_id=DCpYAsWXwzgmriunr0IvlM8z5g9Vowtt&redirect_uri=http://localhost:8080/login-results
# Link per il Login
# https://simoennova.eu.auth0.com/login?state=g6Fo2SBzbUs1Yk9xWVdkSHNMR1lscmV1cy1LX3BtUzlRZ0M5aaN0aWTZIGx4aUhrMkdDV2Z6aENXWnh2YXBiUWFxWDN2NFRVSE5uo2NpZNkgWThOZTRBVFF4TTdsSVBmbVh4VWF4WVdPOHdkTzRKVDE&client=Y8Ne4ATQxM7lIPfmXxUaxYWO8wdO4JT1&protocol=oauth2&prompt=consent&response_type=code&redirect_uri=https%3A%2F%2Fmanage.auth0.com%2Ftester%2Fcallback%3Fconnection%3Dgoogle-oauth2&scope=openid%20profile

'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

# PASTE YOUR OWN TOKEN HERE
# MAKE SURE THIS IS A VALID AUTH0 TOKEN FROM THE LOGIN FLOW
token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik9FSXlNREUxTnpKQk1EZ3pORVpGTkRRNU1rVTFRalpETlRoQ1F6RXdSakJCUXpRMlJVWkRNQSJ9.eyJpc3MiOiJodHRwczovL3NpbW9lbm5vdmEuZXUuYXV0aDAuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTAzNTA3NDUwMzk0MTEwNjQ3MDg3IiwiYXVkIjpbImltYWdlIiwiaHR0cHM6Ly9zaW1vZW5ub3ZhLmV1LmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE1Nzk1NTI1MDksImV4cCI6MTU3OTU1OTcwOSwiYXpwIjoiRENwWUFzV1h3emdtcml1bnIwSXZsTTh6NWc5Vm93dHQiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIn0.Poy0W14jz_0zcsNgnEc1mcIqvtd9vn0UIjLRickeYZOrcc44PzJfGnb2l0iOkCRpa9Pk8weuTR-c_PfNwSuPrtjgjLZDWE3BiuuhiGHwsXrkhaLGLtuRMv-U6G48b9OgUqreaPHwRPO0rKqTRgEyJhg1n5MmSO9GEaC-2QbMKEp9tJciWHl8olLQ-ruyMJiTxpcCB268SU3d8ejsdl3xjlwzjyi5bBoLu0DycaFbOqHNWItBouKkLIbU3BR2bkkpgSs9PigNrllLOdrMDKBTubV_xIXwefeNz7Mvd9yixhj2pHmjqYeqo8jxCm3KyKojsiA0QmjzD2zsKs7S11_7Og"

## Auth Header
def verify_decode_jwt(token):
    # GET THE PUBLIC KEY FROM AUTH0
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    print('JSONURL: ' + str(jsonurl))
    jwks = json.loads(jsonurl.read())

    # GET THE DATA IN THE HEADER
    unverified_header = jwt.get_unverified_header(token)
    print('unverified_header: ' + str(unverified_header))

    # CHOOSE OUR KEY
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    # Finally, verify!!!
    if rsa_key:
        try:
            # USE THE KEY TO VALIDATE THE JWT
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
        'code': 'invalid_header',
        'description': 'Unable to find the appropriate key.'
    }, 400)


if __name__ == '__main__':
    verify_decode_jwt(token)
