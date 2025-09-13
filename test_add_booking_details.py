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
        return data["data"]["access_token"]
    else:
        raise Exception(f"Login gagal: {data}")


def add_booking_detail(token: str, booking_id: str):
    url = f"https://api.test.sindoferry.com.sg/Agent/Booking/Bookings/{booking_id}/Details"

    payload = {
        "identification": {
            "type": 0,
            "no": "A321125",
            "fullName": "ANDI",
            "gender": 0,  # 0 = Male, 1 = Female
            "dateOfBirth": "1991-01-01",
            "placeOfBirth": None,
            "issueDate": "2020-09-01",
            "expiryDate": "2027-09-01",
            "nationalityID": "0dbe8cd6-cb51-4e34-ff90-08d7934c8bf2",     # contoh GUID negara
            "issuanceCountryID": "0dbe8cd6-cb51-4e34-ff90-08d7934c8bf2"  # contoh GUID negara
        }
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.post(url, headers=headers, json=payload, timeout=10)
    print("Status:", response.status_code)
    try:
        print("Response JSON:", json.dumps(response.json(), indent=2))
    except Exception:
        print("Response Text:", response.text)


if __name__ == "__main__":
    token = login()
    print("✅ Login sukses, token berhasil didapat.")

    # contoh bookingID yang didapat dari create booking sebelumnya
    booking_id = "52ac9e1c-cc8e-49e9-4ce7-08ddf1eee351"

    add_booking_detail(token, booking_id)
