import requests
from .config import WEBSITE_TOKEN, BASE_URL

SERVER_ERROR_MESSAGE = "Server hozircha ishlamayapti iltimos keyinroq qayta urinib ko'ring 🤖"


def load_client(user_id):
    full_url = BASE_URL + f"/client/{user_id}/?token={WEBSITE_TOKEN}"
    try:
        req = requests.get(full_url)
        res = req.json()
        try:
            return res
        except KeyError as e:
            print(e, '14 qator recource.py')
            return ""
    except Exception as e:
        print(e,'17 qator recource.py')
        return SERVER_ERROR_MESSAGE

def register_client(message, username):
    first_name = message.contact.first_name
    last_name = message.contact.last_name
    phone = message.contact.phone_number
    user_id = message.contact.user_id
    full_url = BASE_URL + f"/register/?first_name={first_name}&last_name={last_name}&phone={phone}&user_id={user_id}&username={username}&token={WEBSITE_TOKEN}"
    try:
        req = requests.get(full_url)
        res = req.json()
        return res
    except Exception as e:
        print(e)
        return ""

def send_code(code, user_id):
    full_url = BASE_URL + f"/receive-code/{user_id}/?code={code}&token={WEBSITE_TOKEN}"
    print(full_url)
    try:
        req = requests.get(full_url)
        res = req.json()
        return res
    except Exception as e:
        print(e, '43 qator recource.py')
        return SERVER_ERROR_MESSAGE

# try to get the products-list from the website with token and return the products
def load_products():
    full_url = BASE_URL + f"/products-list/?token={WEBSITE_TOKEN}"
    try:
        req = requests.get(full_url)
        res = req.json()
        return res
    except Exception as e:
        print(e, '54 qator recource.py')
        return SERVER_ERROR_MESSAGE

# order product
def order_product(product_id, user_id):
    full_url = BASE_URL + f"/order-product/{product_id}/?token={WEBSITE_TOKEN}&user_id={user_id}"
    try:
        req = requests.get(full_url)
        res = req.json()
        return res
    except Exception as e:
        print(e, '65 qator recource.py')
        return SERVER_ERROR_MESSAGE

