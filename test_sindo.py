import requests
import pandas as pd

# --- STEP 1: Login & ambil token ---
login_url = "https://api.test.sindoferry.com.sg/agent/Agent/Login"

login_payload = {
    "agentCode": "T900T63",
    "username": "testparistvl",
    "password": "j&o99?Pm2#Uj",
    # "rememberMe": True
}

headers = {
    "Content-Type": "application/json"
}

try:
    login_response = requests.post(login_url, json=login_payload, headers=headers, timeout=10)
    login_response.raise_for_status()
    login_data = login_response.json()

    if login_data.get("status") == "Ok":
        token = login_data["data"]["access_token"]
        print("✅ Login sukses, token berhasil didapat.")
    else:
        print("❌ Login gagal:", login_data)
        exit()

except requests.exceptions.RequestException as e:
    print("Error login:", e)
    exit()


# # --- STEP 2: Get Ferry Schedule ---
# schedule_url = "https://api.test.sindoferry.com.sg/TA/TAFerrySchedule"

# schedule_payload = {
#     "DepartureTerminal": "HFC",
#     "ArrivalTerminal": "BTC",
#     "DepartureDate": "2025-09-01",
#     "ReturnDate": "",
#     "TripType": "O",
#     "Nationality": "ID",
#     "Adult": 1,
#     "Child": 0,
#     "Infant": 0,
#     "PromoCode": ""
# }


# schedule_headers = {
#     "Content-Type": "application/json",
#     "Authorization": f"Bearer {token}"
# }

# try:
#     schedule_response = requests.post(schedule_url, json=schedule_payload, headers=schedule_headers, timeout=10)
#     schedule_response.raise_for_status()
#     print("📅 Jadwal Ferry:")
#     print(schedule_response.json())
# except requests.exceptions.RequestException as e:
#     print("Error get schedule:", e)


url = "https://core.test.sindoferry.com.sg/api/Trips/GetTripWeb"
params = {
    "embarkation": "HFC",   # HarbourFront
    "destination": "BTC",   # Batam Centre
    "tripdate": "20250901"  # format YYYYMMDD
}

response = requests.get(url, params=params, timeout=10)
data = response.json()

# Convert ke DataFrame biar enak dibaca
df = pd.DataFrame(data)
print(df[["tripID", "departureTime", "arrivalTime", "status", "usedSeat", "gateOpen", "gateClose"]])



def get_schedules(embarkation: str, destination: str, tripdate: str):
    """
    Ambil jadwal ferry dari Sindo Ferry API (GetTripWeb).
    
    :param embarkation: Kode pelabuhan keberangkatan (contoh: "HFC")
    :param destination: Kode pelabuhan tujuan (contoh: "BTC")
    :param tripdate: Tanggal perjalanan dalam format YYYYMMDD (contoh: "20250901")
    :return: DataFrame jadwal ferry
    """
    url = "https://core.test.sindoferry.com.sg/api/Trips/GetTripWeb"
    params = {
        "embarkation": embarkation,
        "destination": destination,
        "tripdate": tripdate
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Konversi ke DataFrame
        df = pd.DataFrame(data)
        if not df.empty:
            return df[["tripID", "departureTime", "arrivalTime", "status", "usedSeat", "gateOpen", "gateClose"]]
        else:
            print("⚠️ Tidak ada jadwal ditemukan.")
            return pd.DataFrame()

    except requests.exceptions.RequestException as e:
        print("❌ Error ambil jadwal:", e)
        return pd.DataFrame()


# --- Contoh pemakaian ---
if __name__ == "__main__":
    schedules = get_schedules("HFC", "BTC", "20250901")
    print(schedules)


get_schedules("HFC", "BTC", "20250901")
get_schedules("BTC", "HFC", "20250905")


def get_routes(token: str, search: str = None):
    """
    Ambil daftar routes ferry dari API Sindo Ferry.
    """
    url = "https://api.test.sindoferry.com.sg/Agent/Master/Routes"

    params = {
        "filter": f'{{"searchString":{f"""\"{search}\"""" if search else "null"}}}',
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
        return df[["code", "name"]]

    except Exception as e:
        print("❌ Error ambil routes:", e)
        return pd.DataFrame()


# --- Contoh pemakaian setelah login ---
if __name__ == "__main__":
    # pakai token hasil login
    token = "ISI_TOKEN_HASIL_LOGIN"
    routes = get_routes(token)
    print(routes)