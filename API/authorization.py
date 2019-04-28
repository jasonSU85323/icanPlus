import hashlib
import hmac
import requests
import time
import string
from random import Random
import hashlib

def nonce_random_str(randomlength=3):
    str = ""
    chars = "0123456789"
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]
    return str
def state_random_str(randomlength=32):
    str = ""
    chars = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789"
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]
    return str    
def sign_signature(payload, key):
    datalist = []
    
    for key, value in sorted(payload.items()):
        datalist.append("{}={}".format(key, value))

    data = '&'.join(datalist)

    return hmac.new(key, msg=data.encode(), digestmod=hashlib.sha512).hexdigest()



if __name__ == '__main__':
	# 1. dataset-----------------------------------------------------------------
    # product name: Q&A+
    client_id  = "6d73661936a1d4f5d8e1fec12086dd20"
    client_key = "b69af4646ceed2c1bbc44f9c0ac1f63c3edfeb4dc899b7bd38287ccb6791bcdb2d97f35ea6556dd5840ec7e7edf0cbf5e3bbf6e06e18a0e50a3fbf969e60c530"

    user_id = "a57345734@yahoo.com.tw"
    timestamp = int(time.time())
    nonce = nonce_random_str(3)
    state = state_random_str(3)
    

    # 2. signature-----------------------------------------------------------------

    S_payload = {    
        "client_id": client_id,    							# OK
        "nonce" : nonce,       				# ??
        "timestamp" : timestamp	                            # OK
    }
    # print(client_key.decode('hex'))
    exit()
    # b'\xb6\x9a\xf4dl\xee\xd2\xc1\xbb\xc4O\x9c\n\xc1\xf6<>\xdf\xebM\xc8\x99\xb7\xbd8(|\xcbg\x91\xbc\xdb-\x97\xf3^\xa6Um\xd5\x84\x0e\xc7\xe7\xed\xf0\xcb\xf5\xe3\xbb\xf6\xe0n\x18\xa0\xe5\n?\xbf\x96\x9e`\xc50'
    signature = sign_signature(S_payload, client_key.decode('hex'))

    # 3. authorization-----------------------------------------------------------------

    url = "https://2019-hackathon.api.mithvault.io/oauth/authorize"
    payload = { "client_id": client_id,
                "timestamp": timestamp,
                "nonce": nonce,
                "state": state,
                "user_id": user_id,
    }
    headers = {
      "X-Vault-Signature": signature,
      "Content-Type": "application/json",
      "Authorization": "Basic " + client_key
    }
    print(payload)
    print(headers) 
    print(signature)   
    response = requests.request("POST", url, headers = headers, data = payload, allow_redirects=False)

    print(response.text)
    print(response.status_code)