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

    try:
        response = requests.post(login_url, json=login_payload, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get("status") == "Ok":
            token = data["data"]["access_token"]
            print("✅ Login sukses, token berhasil didapat.")
            return token
        else:
            print("❌ Login gagal:", data)
            return None
    except requests.exceptions.RequestException as e:
        print("❌ Error login:", e)
        return None


def create_booking(token: str):
    url = "https://api.test.sindoferry.com.sg/Agent/Booking/Bookings"

    payload = {
        "isRoundTrip": False,
        "isReturnTripOpen": True,
        "departureCoreApiTrip": {
            "date": "2025-09-14", # yyyy-mm-dd
            "routeID": "07adda23-56e2-475d-15ac-08d7934ea487",  # dari GET Routes
            # "routeID": "a128434c-fe0e-4792-8695-10f4b3ab80eb",  # dari GET Routes
            "id": "398",       # ini Trip ID (contoh dari GetTrips, bukan tripSchedID)
            "time": "0825",
            "gateOpen": "0740",
            "gateClose": "0810"
        },
        "returnCoreApiTrip": None
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        print("Status code:", response.status_code)
        if response.text.strip():
            try:
                print("Response JSON:", json.dumps(response.json(), indent=2))
            except Exception:
                print("Response Text:", response.text)
        else:
            print("⚠️ Empty response body")
    except requests.exceptions.RequestException as e:
        print("❌ Error booking:", e)


if __name__ == "__main__":
    token = login()
    if token:
        create_booking(token)
