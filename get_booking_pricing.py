import requests
import json
import pandas as pd

# --- STEP 1: Login ---
def login():
    login_url = "https://api.test.sindoferry.com.sg/agent/Agent/Login"

    login_payload = {
        "agentCode": "T900T63",
        "username": "testparistvl",
        "password": "j&o99?Pm2#Uj",
    }

    headers = {"Content-Type": "application/json"}
    response = requests.post(login_url, json=login_payload, headers=headers, timeout=10)
    response.raise_for_status()
    data = response.json()

    if data.get("status") == "Ok":
        print("✅ Login sukses, token berhasil didapat.")
        return data["data"]["access_token"]
    else:
        raise Exception(f"❌ Login gagal: {data}")


# --- STEP 2: Get Booking Type Pricings ---
def get_booking_type_pricings(token: str, search: str = None):
    url = "https://api.test.sindoferry.com.sg/Agent/Booking/BookingTypePricings"

    params = {
        "filter": json.dumps({
            "searchString": search if search else None,
            "sort": 0,
            "currentActive": True
        }),
        "pagination": json.dumps({
            "pageIndex": 0,
            "pageSize": 0
        })
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    try:
        print("🔎 URL:", url)
        print("🔎 Params:", params)

        response = requests.get(url, headers=headers, params=params, timeout=10)

        print("🔎 Final Request URL:", response.url)
        print("🔎 Raw Response:", response.text)

        response.raise_for_status()
        data = response.json()

        if data.get("status") == "Ok":
            records = data["data"]["records"]
            print("✅ Records didapat:", len(records))
            return records
        else:
            print("❌ Error response:", data)
            return []

    except Exception as e:
        print("❌ Error ambil booking type pricings:", e)
        return []



# --- MAIN ---
if __name__ == "__main__":
    token = login()
    get_booking_type_pricings(token)
