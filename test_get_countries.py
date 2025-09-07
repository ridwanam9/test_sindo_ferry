import requests
import json
import pandas as pd

# --- STEP 1: LOGIN ---
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


# --- STEP 2: GET COUNTRIES ---
def get_countries(token: str, search: str = None):
    url = "https://api.test.sindoferry.com.sg/Agent/Master/Countries"

    # Sesuai dokumentasi, filter & pagination harus berupa JSON string
    filter_param = {
        "searchString": search if search else None,
        "sort": 0
    }
    pagination_param = {
        "pageIndex": 0,
        "pageSize": 0
    }

    params = {
        "filter": json.dumps(filter_param),
        "pagination": json.dumps(pagination_param)
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        records = data["data"]["records"]

        df = pd.DataFrame(records)
        if not df.empty:
            print("📌 Daftar negara ditemukan:")
            print(df[["id", "code", "name", "nationality"]].head(10))
            return df
        else:
            print("⚠️ Tidak ada country ditemukan.")
            return pd.DataFrame()

    except Exception as e:
        print("❌ Error ambil countries:", e)
        return pd.DataFrame()


# --- STEP 3: GET INDONESIA ID ---
def get_indonesia_id(token: str):
    countries = get_countries(token, search="ID")
    if not countries.empty:
        indo = countries[countries["code"] == "ID"]
        if not indo.empty:
            indo_id = indo.iloc[0]["id"]
            print(f"🇮🇩 Indonesia ID: {indo_id}")
            return indo_id
    print("⚠️ Indonesia tidak ditemukan.")
    return None


# --- MAIN ---
if __name__ == "__main__":
    token = login()
    if token:
        # ambil semua countries
        get_countries(token)

        # khusus ambil Indonesia
        get_indonesia_id(token)
