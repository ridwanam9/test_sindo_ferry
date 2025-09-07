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


# --- STEP 2: Delete Booking Detail ---
def delete_booking_detail(token: str, booking_id: str, booking_detail_id: str):
    url = f"https://api.test.sindoferry.com.sg/Agent/Booking/Bookings/{booking_id}/Details/{booking_detail_id}"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.delete(url, headers=headers, timeout=10)
        print("Status:", response.status_code)
        if response.text.strip():
            try:
                print("Response JSON:", json.dumps(response.json(), indent=2))
            except Exception:
                print("Response Text:", response.text)
        else:
            print("⚠️ Empty response body")
    except Exception as e:
        print("❌ Error delete booking detail:", e)


# --- MAIN ---
if __name__ == "__main__":
    token = login()

    # Ganti dengan bookingID & bookingDetailID yang valid
    booking_id = "d3958de3-0360-40cf-1398-08ddeaba690d"
    booking_detail_id = "ab41743b-a1e9-4d3c-6399-08ddeaba69c4"

    delete_booking_detail(token, booking_id, booking_detail_id)
