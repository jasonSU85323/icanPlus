# Configuration Profile：
# client ID (e.g. ba6cabfb4de8d9f4f388124b1afe82b1)
# client key (e.g. aefd2b59d780eb29bc95b6cf8f3503233ad702141b20f53c8a645afbb8c6616048c5e9cc741e0ebee1a2469c68364e57e29dbeeabadc0b67958b9c3da7eabab9)
# mining key (e.g. demo)
# ------------------------------------------------------------------------------------------------------------------------------------------------

# product name: Q&A+
# client ID: 6d73661936a1d4f5d8e1fec12086dd20
# client secret: b69af4646ceed2c1bbc44f9c0ac1f63c3edfeb4dc899b7bd38287ccb6791bcdb2d97f35ea6556dd5840ec7e7edf0cbf5e3bbf6e06e18a0e50a3fbf969e60c530
# ------------------------------------------------------------------------------------------------------------------------------------------------
# ClientID：它會是唯一的，也就是這一個 ClientID 就是對應到你所設定的程式
# Secret：通常是可以在服務提供者所提供的申請介面中隨時做更換，避免 Secret 被冒用
# ------------------------------------------------------------------------------------------------------------------------------------------------
import hashlib
import hmac

def sign_signature(payload, key):
    def preprocess(payload):
        if isinstance(payload, dict):
            data = '&'.join(
                f'{key}={preprocess(value)}'
                for key, value in sorted(payload.items())
            )
        elif isinstance(payload, list):
            data = [f'{preprocess(key)}' for key in payload]    
            data = f'[{",".join(data)}]'
        else:
            data = f'{payload}'
        return data

    return hmac.new(key, msg=preprocess(payload).encode(), digestmod=hashlib.sha512).hexdigest() # 密鑰、消息、要使用之算法

if __name__ == '__main__':    
    client_key = 'ba25da088600b74d608ea44a4cb03bd0c898432875be9eaa0ffaf273f03949707d58b6d9724bcdf94f33aeedfb9418d931ef8bebf0e081251f16ce91b7e80730'
    payload = {    
        'client_id': '3b6fdff04b7127e9a3bca33b7f2ec731',    
        'nonce' : '2a4355be3210faeb9007111228132f3b',    
        'timestamp' : 1543593600,    
    }    


    signature = sign_signature(payload, bytes.fromhex(client_key))    
    assert signature == 'e09d0997c3399b9575c7ad33b12903fbc0899a8812f1ad9de017f570404e165ab220a9ff0bdf36c276dc08452e9e03a649445dfe264a8db96a6b5768e1fa9641'

# ------------------------------------------------------------------------------------------------------------------------------------------------
# 請求授權同意書(grant)
# body
# {
#     "client_id": "{{client_id}}",
#     "timestamp": 1553592420,
#     "nonce": "848",
#     "state": "{{state}}",
#     "user_id": "{{user_id}}"
# }
import requests
url = '{{host}}/oauth/authorize'
payload = { "client_id": "{{client_id}}",
            "timestamp": 1553592420,
            "nonce": "881",
            "state": "{{8be761fd22db506428c9b07d31ff549e7f70ecd0a872c2e9af4380d7902d34c23ca3363c9c3e2d6aa7e94221345a4f67737e1dfe3b7179ffd28858afef77bdeb}}",
            "user_id": "{{user_id}}"
}
headers = {
  'X-Vault-Signature': '{{sigunature}}',
  'Content-Type': 'application/json',
  'Authorization': '{{authorization}}'
}
response = requests.request('POST', url, headers = headers, data = payload, allow_redirects=False, timeout=undefined, allow_redirects=false)
print(response.text)    
# 簽署授權同意書(grant)
# 回傳如下
# https://examples.com/?grant_code=fbe481f5ee834834cd885d3a5f18e661956e69ac1
# dfeb36ae3a62d19aed7ee04d2604d62dc174ffd14182462ce752bc9935b8689f24a4213a372a
# 1aca0274063&state=8be761fd22db506428c9b07d31ff549e7f70ecd0a872c2e9af4380d790
# 2d34c23ca3363c9c3e2d6aa7e94221345a4f67737e1dfe3b7179ffd28858afef77bdeb

# ------------------------------------------------------------------------------------------------------------------------------------------------
# 給出授權同意書
# body
# {
#     "client_id": "{{client_id}}",
#     "timestamp": 1553592420,
#     "nonce": "572",
#     "state": "{{state}}",
#     "grant_code": "{{grant_code}}"
# }
import requests
url = '{{host}}/oauth/token'
payload = { "client_id": "{{client_id}}",
            "timestamp": 1553592420,
            "nonce": "464",
            "state": "{{state}}",
            "grant_code": 
            "{{grant_code}}"
}
headers = {
  'X-Vault-Signature': '{{sigunature}}',
  'Content-Type': 'application/json'
}
response = requests.request('POST', url, headers = headers, data = payload, allow_redirects=False, timeout=undefined, allow_redirects=false)
print(response.text)
# 取得授權使用者對應的Token
# 回傳如下
# {
#     "token": "cc9f945b43dc39878f8be0a57399cd6a17cd9ca42c4b008ab72e83f5efa0c5c2d53cf045d056e72e14cf7e10a8cc79541b0338fe9b1211b65e0f3eab29128989"
# }

# ------------------------------------------------------------------------------------------------------------------------------------------------
# 獲取OAuth用戶信息
# 通過您的應用程序獲取綁定到VAULT的用戶信息。
import requests
url = '{{host}}/oauth/user-info?client_id={{client_id}}&nonce=740&timestamp=1553592420'
headers = {
  'Authorization': '{{authorization}}',
  'X-Vault-Signature': '{{signature}}'
}
response = requests.request('GET', url, headers = headers, data = payload, allow_redirects=False, timeout=undefined, allow_redirects=false)
print(response.text)
# 回傳如下
# {
#         'kyc_level': 1,
#         'stake_level': 1,
#         'balance': 1201.234,
#         'amount':1200,
#         'staked_amount': 1.234
# }

# ------------------------------------------------------------------------------------------------------------------------------------------------
# 獲取OAuth餘額信息
# 獲取應用程序的當前餘額。
import requests
url = '{{host}}/oauth/balance?client_id={{client_id}}&nonce=829&timestamp=1553602235'
headers = {
  'Authorization': '{{authorization}}',
  'X-Vault-Signature': '{{signature}}'
}
response = requests.request('GET', url, headers = headers, data = payload, allow_redirects=False, timeout=undefined, allow_redirects=false)
print(response.text)
# 回傳如下
# [
#     {
#         "currency": "MITH",
#         "balance": 50000.0,
#         "updated_at": "2019-01-31T07:06:26"
#     }
# ]