import requests
import pandas as pd



# --- STEP 1: Login & ambil token ---
def login():
    login_url = "https://api.test.sindoferry.com.sg/agent/Agent/Login"

    login_payload = {
        "agentCode": "T900T63",
        "username": "testparistvl",
        "password": "j&o99?Pm2#Uj",
        # "rememberMe": True
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


# --- STEP 2: Get Routes ---
def get_routes(token: str, search: str = None):
    url = "https://api.test.sindoferry.com.sg/Agent/Master/Routes"

    # param filter & pagination sesuai dokumentasi
    params = {
        "filter": f'{{"searchString":"{search}"}}' if search else '{"searchString":null}',
        "pagination": '{"pageIndex":0,"pageSize":0}'
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
            return df[["code", "name"]]
        else:
            print("⚠️ Tidak ada route ditemukan.")
            return pd.DataFrame()

    except Exception as e:
        print("❌ Error ambil routes:", e)
        return pd.DataFrame()


# --- MAIN ---
if __name__ == "__main__":
    token = login()
    if token:
        routes = get_routes(token)
        print("📍 Daftar Routes:")
        print(routes)

