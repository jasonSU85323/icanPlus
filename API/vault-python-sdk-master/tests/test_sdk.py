import pytest

import os
from uuid import uuid4
import vault

CLIENT_ID = 'ba6cabfb4de8d9f4f388124b1afe82b1'
CLIENT_SECRET = 'aefd2b59d780eb29bc95b6cf8f3503233ad702141b20f53c8a645afbb8c6616048c5e9cc741e0ebee1a2469c68364e57e29dbeeabadc0b67958b9c3da7eabab9'
MINING_KEY = 'demo'

AUTHORIZATION = '1668ff50dca1a85086b558e9e5abc521f14f2317712cb7725d8a9b0f670afe04ea61e091f1060e7845e16e55e300995cb79340782ce34ba683ec9e37e856ff95'

def test_sdk():
    sdk = vault.MithVaultSDK(CLIENT_ID, CLIENT_SECRET, MINING_KEY)

    state = os.urandom(16).hex()
    bind_uri = sdk.getBindURI(state)
    assert bind_uri == f'{sdk.config["host"]}{sdk.config["authorize"]}?client_id={CLIENT_ID}&state={state}'

    info = sdk.getClientInformation()
    assert info != []
    assert 'currency'   in info[0]
    assert 'balance'    in info[0]
    assert 'updated_at' in info[0]

def test_bind_user():
    sdk = vault.MithVaultSDK(CLIENT_ID, CLIENT_SECRET, MINING_KEY)

    info = sdk.getUserInformation(AUTHORIZATION)
    assert 500.0 >= info['balance'] >= 0.0
    assert 500.0 >= info['amount'] >= 0.0


    activities = sdk.getUserMiningAction(AUTHORIZATION)

    uuid = str(uuid4())
    sdk.postUserMiningAction(AUTHORIZATION, uuid, reward=4)
    activities = sdk.getUserMiningAction(AUTHORIZATION)
    for activity in activities:
        if activity['uuid'] == uuid:
            assert activity['status'] in ('PENDING', 'MINING', 'MINED')
            assert activity['reward'] == 4
            break
    else:
        raise KeyError(f'uuid {uuid} not found')

    sdk.deleteUserMiningAction(AUTHORIZATION, uuid)
    activities = sdk.getUserMiningAction(AUTHORIZATION)
    for activity in activities:
        if activity['uuid'] == uuid:
            assert activity['status'] in ('DELETED')
            break
    else:
        raise KeyError(f'uuid {uuid} not found')

    # support pagination for the getUserMiningAction
    activities = sdk.getUserMiningAction(AUTHORIZATION, next_id=100)
