import json
from decouple import config
import requests
from datetime import datetime

BASE_URL = config('BASE_URL')

import requests


def create_user(phone, fio, telegram_id, lang):
    """
    Attempts to register a new user.
    Returns a tuple: (success, message)
    """
    url = f"{BASE_URL}/api/auth/register/"

    # This line is fragile. It's better to ensure the correct lang code ('uz', 'ru') is passed directly.
    # For now, let's assume it works as intended.
    if " " in lang:
         lang = lang.split(" ")[1]

    payload = {
        "phone_number": phone,
        "first_name": fio,
        "telegram_id": telegram_id,
        "user_lang": lang
    }

    try:
        response = requests.post(url=url, data=payload)

        if response.status_code == 201:
            print("User created successfully.")
            return (True, "User created.")

        # Check for the specific validation error
        if response.status_code == 400:
            error_data = response.json()
            if 'telegram_id' in error_data and "already exist" in error_data['telegram_id'][0]:
                print("User already exists.")
                # You might want to log the user in or retrieve their data here instead.
                return (False, "User already exists.")
            else:
                # Handle other possible 400 errors
                print(f"Bad Request: {error_data}")
                return (False, f"Invalid data: {error_data}")

        # Handle other HTTP errors
        print(f"An error occurred: {response.status_code}")
        return (False, f"Server error: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"A network error occurred: {e}")
        return (False, "Network error.")



def update_user_lang(telegram_id, new_lang):
    """
    Updates the language of a user by their Telegram ID.
    Returns a tuple: (success, message)
    """
    url = f"{BASE_URL}/api/auth/update_lang/{telegram_id}/"


    if " " in new_lang:
        new_lang = new_lang.split(" ")[1]

    payload = {
        "user_lang": new_lang
    }
    try:
        response = requests.patch(url, json=payload)
        if response.status_code in [200, 202]:
            return True, "User language updated successfully."
        else:
            return False, f"Failed to update language. Status: {response.status_code}, Response: {response.text}"
    except Exception as e:
        return False, f"Request failed with exception: {str(e)}"



def get_user_by_telegram_id():
    """
    Checks if a user with the given Telegram ID exists.
    Returns a dictionary: {'exists': bool, 'data': user_data or message}
    """
    url = f"{BASE_URL}/api/auth/users/"  # Telegram ID ni url-ga qo'shamiz

    try:
        response = requests.get(url)
        if response.status_code == 200:
            user_data = response.json()
            users = {}
            for i in user_data:
                users[int(i["telegram_id"])] = i["user_lang"]
            return users
        elif response.status_code == 404:
            return {
                'exists': False,
                'data': 'User not found'  # Foydalanuvchi topilmadi
            }
        else:
            return {
                'exists': False,
                'data': f"Unexpected response: {response.status_code} - {response.text}"  # Xato javobni qaytarish
            }
    except Exception as e:
        return {
            'exists': False,
            'data': f"Request failed: {str(e)}"
        }


def current_day():
    url = f"{BASE_URL}/api/bookings/available-slots/?date={datetime.today().date()}&service_id={1}"
    response = requests.get(url=url)
    res = response.json()
    return res["slots"]



def booked_time(tg_id, time, service):
    url = f"{BASE_URL}/api/bookings/"
    payload = {
        "telegram_id": tg_id,
        "start_time": time,
        "service": service
    }
    headers = {"Content-Type": "application/json"}  # qo‘shib ko‘ring

    # print("Payload:", payload)

    try:
        response = requests.post(url, json=payload, headers=headers)
        # print("Response status:", response.status_code)
        # print("Response text:", response.text)

        if response.status_code == 201:
            return True
        elif response.status_code == 404:
            return {'exists': False, 'data': 'User not found'}
        else:
            return {
                'exists': False,
                'data': f"Unexpected response: {response.status_code} - {response.text}"
            }
    except Exception as e:
        return {'exists': False, 'data': f"Request failed: {str(e)}"}




def get_brons_all():
    url = f"{BASE_URL}/api/bookings/"
    response = requests.get(url)
    bron_base = {}

    if response.status_code == 200:
        for booking in response.json():
            start_time = booking.get("start_time")
            if not start_time:
                continue

            start_dt = datetime.fromisoformat(start_time)
            date_str = start_dt.strftime("%d-%m")
            time_str = start_dt.strftime("%H:%M")

            user_info = booking.get("user", "")
            if " - " in user_info:
                name, phone, tg_id = user_info.split(" - ")
            else:
                name, phone = user_info, ""

            bron_base[booking["id"]] = {
                "name": name.strip(),
                "phone": phone.strip(),
                "tg_id": tg_id.strip(),
                "date": date_str,
                "time": time_str,
                "summa": int(float(booking["service"]["price"])),
                "status": 0 if booking["status"] == "CONFIRMED" else 1
            }
    else:
        print(f"❌ Failed to get bookings: {response.status_code}")
    return bron_base




def booking_history_user(tg_id):
    url = f"{BASE_URL}/api/bookings/booking-history/?telegram_id={tg_id}"
    response = requests.get(url)

    # Tekshiruvlar
    if response.status_code != 200:
        print(f"❌ Error: {response.status_code}")
        return []

    data = response.json()
    print(data)

    # Faqat 'start_time' larni olish
    total = [item['start_time'] for item in data if 'start_time' in item]

    # Vaqtlar bo‘yicha tartiblash
    total.sort(key=lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M"))

    return total

