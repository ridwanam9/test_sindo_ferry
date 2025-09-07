import requests
import json

# --- STEP 1: Login dulu ---
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


# --- STEP 2: GET All Bookings ---
def get_all_bookings(token: str, search: str = None):
    url = "https://api.test.sindoferry.com.sg/Agent/Booking/Bookings"

    params = {
        "filter.searchString": search if search else None,
        "filter.sort": 2,  # sort by Name ASC
        "pagination.pageIndex": 0,
        "pagination.pageSize": 0  # ambil semua data
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)
        print("Status:", response.status_code)

        if response.status_code == 200:
            data = response.json()
            print("Response JSON:", json.dumps(data, indent=2))

            # contoh akses data
            records = data.get("data", {}).get("records", [])
            print(f"📌 Total records: {len(records)}")
            for rec in records[:3]:  # tampilkan maksimal 3 contoh
                print("Booking No:", rec.get("identification", {}).get("no"),
                      "| Name:", rec.get("identification", {}).get("fullName"))
        else:
            print("❌ Response Error:", response.text)

    except Exception as e:
        print("❌ Error ambil bookings:", e)


# --- MAIN ---
if __name__ == "__main__":
    token = login()
    get_all_bookings(token)
