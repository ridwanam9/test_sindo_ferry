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


# --- STEP 2: Get Available Sectors ---
def get_available_sectors(token: str):
    url = "https://api.test.sindoferry.com.sg/Agent/Booking/Sectors/Available"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("status") == "Ok":
            records = data["data"]["records"]
            df = pd.DataFrame(records)
            print("📍 Available Sectors:")
            print(df[["id", "code", "name"]])
            return df
        else:
            print("❌ Error response:", data)
            return pd.DataFrame()

    except Exception as e:
        print("❌ Error ambil available sectors:", e)
        return pd.DataFrame()


# --- MAIN ---
if __name__ == "__main__":
    token = login()
    get_available_sectors(token)
