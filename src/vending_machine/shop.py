import dataclasses

import requests
import os

import json

from dacite import from_dict

shop_vm_user = os.getenv("SHOP_VM_USER", None)
shop_vm_password = os.getenv("SHOP_VM_PASSWORD", None)

SHOP_BASE_URL = "https://mad-shop.onrender.com/api"


@dataclasses.dataclass
class Product:
    gtin: str


@dataclasses.dataclass
class PickupItem:
    product: Product
    required: int


@dataclasses.dataclass
class Pickup:
    items: list[PickupItem]


@dataclasses.dataclass
class PickupResponse:
    data: Pickup


def get_login_token():
    login_data = {
        "identifier": shop_vm_user,
        "password": shop_vm_password
    }
    response = requests.post(SHOP_BASE_URL + '/auth/local', json=login_data)
    if response.status_code == 200:
        return response.json().get('jwt')
    else:
        print(f"Login failed: {response.status_code}")
        return None


def get_pickup(pickup_id: str) -> Pickup:
    token = get_login_token()
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f'{SHOP_BASE_URL}/pickups/{pickup_id}?populate=items&populate=items.product',
                            headers=headers)

    if response.status_code == 200:
        pickup_response = from_dict(data_class=PickupResponse, data= response.json())
        return pickup_response.data
    else:
        print(f"Login failed: {response.status_code}")
        return None


def start_pickup(pickup_id: str):
    return _update_pickup_status(pickup_id, 'started')


def finish_pickup(pickup_id: str):
    return _update_pickup_status(pickup_id, 'finished')


def _update_pickup_status(pickup_id: str, status: str) -> bool:
    token = get_login_token()
    headers = {'Authorization': f'Bearer {token}', 'content-type': 'application/json'}
    response = requests.put(f'{SHOP_BASE_URL}/pickups/{pickup_id}',
                            headers=headers,
                            data=json.dumps({'data': {'progress': status}}))

    if response.status_code == 200:
        return True


