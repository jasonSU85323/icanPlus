#! /usr/bin/env python
# Copyright (C) . All right reserved.
import json
from datetime import datetime
import hashlib
import hmac
import os
from uuid import uuid4
import requests


class MithVaultSDK():
    '''

        Ref: https://documenter.getpostman.com/view/4856913/RztrHRU9
    '''
    def __init__(self, client_id, client_secret, mining_key):
        self.config = {
            # general endpoint and SHOULD NOT change
            'host': 'https://2019-hackathon.mithvault.io',
            'api': 'https://2019-hackathon.api.mithvault.io',
            'authorize': '/#/oauth/authorize',
            'donate': '/#/donate/request'
        }
        self.client_id = client_id
        self.client_secret = client_secret
        self.mining_key = mining_key

    # oauth api
    def getBindURI(self, state=None, user_id=None):
        payload = {
            'client_id': self.client_id,
            'state': state or os.urandom(16).hex(),
            'user_id': user_id
        }

        # query_string = '&'.join([f'{k}={v}' for k, v in payload.items()])
        datalist = []
        for key, value in sorted(payload.items()):
            datalist.append("{}={}".format(key, value))
        query_string = '&'.join(datalist)        

        # url = f'{self.config["host"]}{self.config["authorize"]}?{query_string}'
        url = "{}{}?{}".format(self.config["host"], self.config["authorize"], query_string)

        return url

    def getAccessToken(self, grant_code, state):
        payload = {
            'client_id': self.client_id,
            'timestamp': int(datetime.utcnow().timestamp()),
            'nonce': os.urandom(16).hex(),

            'grant_code': grant_code,
            'state': state,
        }

        resp = self._sendAPI_('oauth/token', 'POST', data=payload)
        return resp

    def deleteUserToken(self, token):
        '''
        ME
        '''
        payload = {
            'client_id': self.client_id,
            'timestamp': int(datetime.utcnow().timestamp()),
            'nonce': os.urandom(16).hex(),
        }
        headers = {'Authorization': token}

        resp = self._sendAPI_('oauth/token', 'DELETE', params=payload, headers=headers)
        return resp

    def getClientInformation(self):
        '''
        Used for get the OAuth application information. This API reply
        a list of object, contains the balance amount, currency name and
        final updated.

        >>> sdk = MithVaultSDK()
        >>> info = sdk.getClientInformation()
        >>> assert info != []
        >>> assert 'currency'   in info[0]
        >>> assert 'balance'    in info[0]
        >>> assert 'updated_at' in info[0]
        '''
        payload = {
            'client_id': self.client_id,
            'timestamp': int(datetime.utcnow().timestamp()),
            'nonce': os.urandom(16).hex(),
        }
        info = self._sendAPI_('oauth/balance', 'GET', params=payload)
        return info

    def getUserInformation(self, token):
        '''
        Used for get the specified user information.
        '''
        payload = {
            'client_id': self.client_id,
            'timestamp': int(datetime.utcnow().timestamp()),
            'nonce': os.urandom(16).hex(),
        }

        headers = {'Authorization': token}
        info = self._sendAPI_('oauth/user-info', 'GET', params=payload, headers=headers)
        return info

    # mining-related api
    def getUserMiningAction(self, token, next_id=None):
        payload = {
            'client_id': self.client_id,
            'timestamp': int(datetime.utcnow().timestamp()),
            'nonce': os.urandom(16).hex(),
            'mining_key': self.mining_key,
        }

        if next_id:
            payload['next_id'] = next_id

        headers = {
            'Authorization': token,
        }

        activities = self._sendAPI_('mining', 'GET', params=payload, headers=headers)
        return activities

    def postUserMiningAction(self, token, reward=1, uuid=None, happened_at=None):
        payload = {
            'client_id': self.client_id,
            'timestamp': int(datetime.utcnow().timestamp()),
            'nonce': os.urandom(16).hex(),
            'mining_key': self.mining_key,

            'uuid': uuid or str(uuid4()),
            'reward': reward,
            'happened_at': happened_at or datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S'),
        }
        headers = {
            'Authorization': token,
        }

        resp = self._sendAPI_('mining', 'POST', data=payload, headers=headers)
        return resp

    def deleteUserMiningAction(self, token, uuid):
        payload = {
            'client_id': self.client_id,
            'timestamp': int(datetime.utcnow().timestamp()),
            'nonce': os.urandom(16).hex(),
            'mining_key': self.mining_key,

            'uuid': uuid or str(uuid4()),
        }
        headers = {
            'Authorization': token,
        }

        resp = self._sendAPI_('mining', 'DELETE', params=payload, headers=headers)
        return resp

    # donate api
    def getDonateURI(self, amount, app_id, user_id, state=None):
        '''
        Me
        '''
        payload = {
            'amount'        : amount,
            'app_id'        : app_id,
            'user_id'       : user_id,
            'desc'          : 'test',
            'state'         : state or os.urandom(16).hex()
        }

        datalist = []
        for key, value in sorted(payload.items()):
            datalist.append("{}={}".format(key, value))
        query_string = '&'.join(datalist)        

        url = "{}{}?{}".format(self.config["host"], self.config["donate"], query_string)

        return url

        # url = "{}{}".format(self.config["host"], self.config["donate"])
        # payload = {
        #     'app_id'        : self.client_id,
        #     'user_uuid'     : uuid or str(uuid4()),
        #     'amount'        : "20",
        #     'description'   : 'null',
        #     'state'         : state or os.urandom(16).hex()
        # }
        # headers = {
        #   'Content-Type': 'application/json',
        #   'Authorization': token
        # }
        # print(json.dumps(payload, sort_keys=True, indent=4, separators=(',', ':')))
        # return requests.request('POST', url, headers=headers, json=payload).text




    # privated API
    def _sendAPI_(self, endpoint, method='GET', params=None, data=None, headers=None):
        payload = (params or {}) or (data or {})
        headers = headers or {}

        if 'client_id' in payload:
            # print(type(self.client_secret))
            signature = self._generateSignature_(payload, bytes.fromhex(self.client_secret))
            headers['X-Vault-Signature'] = signature

        # url = f'{self.config["api"]}/{endpoint}'
        url = "{}/{}".format(self.config["api"], endpoint)
        req = requests.request(
            method,
            url,
            params=params,
            json=data,
            headers=headers,
        )

        if not req.ok:
            # raise IOError(f'[{req.status_code}] {req.text}')
            raise IOError("[{}] {}".format(req.status_code, req.text))
        if req.content:
            return req.json()
        return None

    def _generateSignature_(self, data, secret_key): # pylint: disable=no-self-use
        # def preprocess(payload):
        #     if isinstance(payload, dict):
        #         data = '&'.join(
        #             f'{key}={preprocess(value)}'
        #             for key, value in sorted(payload.items())
        #         )
        #     elif isinstance(payload, list):
        #         data = [f'{preprocess(key)}' for key in payload]
        #         data = f'[{",".join(data)}]'
        #     else:
        #         data = f'{payload}'
        #     return data

        # signature = hmac.new(secret_key, msg=preprocess(data).encode(), digestmod=hashlib.sha512)
        # return signature.hexdigest()

        def preprocess(payload):
            datalist = []      
            if isinstance(payload, dict):
                data = '&'.join(
                    '{}={}'.format(key, preprocess(value))
                    for key, value in sorted(payload.items())
                )
            elif isinstance(payload, list):
                data = \
                    '[{}]'.format(
                        ",".join(
                            '{}'.format(preprocess(key))
                            for key in payload
                        )
                    )
            else:
                data = '{}'.format(payload)
            return data
        # print(json.dumps(data, sort_keys=True, indent=4, separators=(',', ':')))
        # print(preprocess(data))
        signature = hmac.new(secret_key, msg=preprocess(data).encode(), digestmod=hashlib.sha512)
        return signature.hexdigest()