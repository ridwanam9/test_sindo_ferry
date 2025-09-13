import requests
import json

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


def get_booking_details(token: str, booking_id: str, search: str = None):
    url = f"https://api.test.sindoferry.com.sg/Agent/Booking/Bookings/{booking_id}/Details"

    # param dikirim dalam bentuk string JSON (bukan key-value terpisah)
    params = {
        "filter": json.dumps({
            "searchString": search if search else None,
            "sort": 2  # Name ASC
        }),
        "pagination": json.dumps({
            "pageIndex": 0,
            "pageSize": 0   # ambil semua
        })
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers, params=params, timeout=10)
    print("Status:", response.status_code)
    try:
        print("Response JSON:", json.dumps(response.json(), indent=2))
    except Exception:
        print("Response Text:", response.text)


if __name__ == "__main__":
    token = login()

    # ⚠️ Ganti dengan bookingID hasil create booking kamu
    booking_id = "19f6c0f8-e505-44e2-37fa-08ddf10795b8"

    get_booking_details(token, booking_id, search="ANDI")
