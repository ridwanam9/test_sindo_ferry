import requests
import json

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


# --- STEP 2: Submit Booking ---
def submit_booking(token: str, booking_id: str, email: str, remarks: str):
    url = "https://api.test.sindoferry.com.sg/Agent/Booking/Bookings/Submit"

    payload = {
        "id": booking_id,
        "emailConfirmation": email,
        "remarks": remarks
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        print("Status:", response.status_code)
        if response.text.strip():
            try:
                print("Response JSON:", json.dumps(response.json(), indent=2))
            except Exception:
                print("Response Text:", response.text)
        else:
            print("⚠️ Empty response body")
    except Exception as e:
        print("❌ Error submit booking:", e)


# --- MAIN ---
if __name__ == "__main__":
    token = login()

    # Ganti dengan BookingID hasil create booking
    booking_id = "7c1de748-a8a2-4773-9512-08ddeb9aadab"
    email = "andi@sindoferry.com.sg"
    remarks = "Booking for Andi"

    submit_booking(token, booking_id, email, remarks)
