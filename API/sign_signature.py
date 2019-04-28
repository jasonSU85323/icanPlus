import hashlib
import hmac
import time
from random import Random

# encoding=utf8  
import sys  
# print sys.getdefaultencoding()
# reload(sys)  
# sys.setdefaultencoding('utf8')
# print sys.getdefaultencoding()

def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]
    return str


# def sign_signature(payload, key):
#     def preprocess(payload):
#         if isinstance(payload, dict):
#             data = '&'.join(
#                 f'{key}={preprocess(value)}'
#                 for key, value in sorted(payload.items())
#             )
#         elif isinstance(payload, list):
#             data = [f'{preprocess(key)}' for key in payload]    
#             data = f'[{",".join(data)}]'
#         else:
#             data = f'{payload}'
#         return data

#     return hmac.new(key, msg=preprocess(payload).encode(), digestmod=hashlib.sha512).hexdigest()

def sign_signature_q(payload, key):
    datalist = []
    
    for key, value in sorted(payload.items()):
        datalist.append("{}={}".format(key, value))

    data = '&'.join(datalist)
    print(data)
    return hmac.new(key, msg=data.encode(), digestmod=hashlib.sha512).hexdigest()

if __name__ == '__main__':
    
    t = time.time()


    client_key = 'ba25da088600b74d608ea44a4cb03bd0c898432875be9eaa0ffaf273f03949707d58b6d9724bcdf94f33aeedfb9418d931ef8bebf0e081251f16ce91b7e80730' # OK
    payload = {    
        'client_id': '3b6fdff04b7127e9a3bca33b7f2ec731',    # OK
        'nonce' : '2a4355be3210faeb9007111228132f3b',       # ??
        'timestamp' : 1543593600,                               # OK
    }    

    print(client_key.decode("hex"))
    import binascii
    data=client_key
    bits = ""
    for x in xrange(0, len(data), 2):
      bits += chr(int(data[x:x+2], 16))
    print(bits)
    exit()
    # signature = sign_signature(payload, bytes.fromhex(client_key))
    signature = sign_signature_q(payload,  client_key.decode("hex"))
    print(signature)
    assert signature == 'e09d0997c3399b9575c7ad33b12903fbc0899a8812f1ad9de017f570404e165ab220a9ff0bdf36c276dc08452e9e03a649445dfe264a8db96a6b5768e1fa9641'
    # print(random_str(3))




# b'\xba%\xda\x08\x86\x00\xb7M`\x8e\xa4JL\xb0;\xd0\xc8\x98C(u\xbe\x9e\xaa\x0f\xfa\xf2s\xf09Ip}X\xb6\xd9rK\xcd\xf9O3\xae\xed\xfb\x94\x18\xd91\xef\x8b\xeb\xf0\xe0\x81%\x1f\x16\xce\x91\xb7\xe8\x070'    