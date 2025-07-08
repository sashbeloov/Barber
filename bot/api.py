import json
from decouple import config
import requests

BASE_URL = config('BASE_URL')

def create_user(phone, fio, telegram_id, lang):
    url = f"{BASE_URL}/api/auth/register/"
    lang = lang.split(" ")[1]
    print(lang)
    post = requests.post(url=url, data={"phone_number":phone, "first_name":fio, "telegram_id":telegram_id, "user_lang":lang})
    if post.status_code != 201:
        return False
    return True



def check_userid(telegram_id):
    url = f"{BASE_URL}/api/auth/users/"
    response = requests.get(url=url).text
    data = json.loads(response)
    exist_user = False
    user_data = {}
    print(data)
    for i in data:
        if i["telegram_id"] == telegram_id:
            exist_user = True
            user_data['lang'] = i['user_lang']
            user_data['id'] = i['id']
            break
    if exist_user:
        return user_data
    return False

def check_admin(telegram_id):
    url = f"{BASE_URL}/api/auth/users/is_staff/"
    response = requests.get(url=url).text
    data = json.loads(response)
    return [i["telegram_id"] for i in data]


def update_language(user_id,user_lang):
    url = f"{BASE_URL}/api/auth/users/update_lang/{user_id}/"
