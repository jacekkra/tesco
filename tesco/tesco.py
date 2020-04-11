#!/usr/bin/env python3

import json
import requests

import firefox

DELIVERY_SLOTS_URL = "https://ezakupy.tesco.pl/groceries/pl-PL/slots/delivery"

def fetch_slots(cookies):
    headers = {"Accept": "application/json"}
    response = requests.get(
        DELIVERY_SLOTS_URL, headers=headers, cookies=cookies)
    return response.json()["slots"]


def probably_not_logged_in():
    msg = "Incoming data is not a valid JSON. "\
        f"Visit {DELIVERY_SLOTS_URL} in your browser and make sure you are logged in."
    print(msg)


def are_slots_available(slots):
    for slot in slots:
        status = slot["status"]
        if status == "Available":
            return True
        assert status == "UnAvailable", f"Unexpected status: {status}. Adjust the script."
    return False


def main():
    cookies = firefox.load_cookies()

    try:
        slots = fetch_slots(cookies)
    except json.decoder.JSONDecodeError:
        probably_not_logged_in()
    else:
        if are_slots_available(slots):
            print(f"Slots found! Visit {DELIVERY_SLOTS_URL} now!")
        else:
            print("No available slots.")


if __name__ == "__main__":
    main()
