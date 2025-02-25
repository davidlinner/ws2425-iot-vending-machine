import requests
import os

shop_vm_user = os.getenv("SHOP_VM_USER", None)
shop_vm_password = os.getenv("SHOP_VM_PASSWORD", None)

SHOP_BASE_URL = "https://mad-shop.onrender.com/api"


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


def get_pickup(pickupID: str):
    token = get_login_token()
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f'{SHOP_BASE_URL}/pickups/{pickupID}?populate=items&populate=items.product',
                            headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Login failed: {response.status_code}")
        return None

# data = get_pickup('nifahblkoskjq0wa5zf4rwqn')
# print(json.dumps(data, indent=4))

