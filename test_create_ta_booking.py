import requests
import json

def login_agent():
    url = "https://api.test.sindoferry.com.sg/agent/Agent/Login"
    payload = {
        "agentCode": "T900T63",
        "username": "testparistvl",
        "password": "j&o99?Pm2#Uj"
    }
    headers = {"Content-Type": "application/json"}
    r = requests.post(url, json=payload, headers=headers, timeout=10)
    data = r.json()
    if data.get("status") == "Ok":
        print("✅ Login sukses")
        return data["data"]["access_token"]
    else:
        raise Exception("Login gagal: " + str(data))

def create_b2b_booking(token: str):
    # url = "https://api.test.sindoferry.com.sg/Agent/TA/CreateBooking"
    url = "https://api.test.sindoferry.com.sg/Agent/TravelAgent/Bookings"

    payload = {
        "input": {
            "BookingDetails": [
                # {
                #     "adult": 1,
                #     "child": 0,
                #     "infant": 0,
                #     "contactPerson": {
                #         "firstName": "Ridwan",
                #         "lastName": "Maulana",
                #         "phone": "628123456789",
                #         "email": "ridwan@example.com"
                #     },
                #     "passengers": [
                #         {
                #             "firstName": "Ridwan",
                #             "lastName": "Maulana",
                #             "nationality": "ID",
                #             "idType": "PASSPORT",
                #             "idNumber": "A12345678",
                #             "gender": "M",
                #             "dob": "1995-01-01"
                #         }
                #     ],
                #     "segments": [
                #         {
                #             "tripID": "RFPE0825",     # ambil dari GetTripWeb
                #             "tripSchedID": 21145,     # ambil dari GetTripWeb
                #             "embarkation": "HFC",
                #             "destination": "BTC",
                #             "departureDate": "2025-09-01"
                #         }
                #     ]
                # }
                {
                    "productID": "26a56151-4a9c-4102-f8d6-08dd14d2d963",
                    "variantID": "1FC78F9F-A94C-4A85-9460-258F632027A7",
                    "startDate": "2024-12-31",
                    "quantity": 1
                },
                {
                    "productID": "891302a8-8b47-4aa7-f8d9-08dd14d2d963",
                    "variantID": "E3C51FE6-2D57-44C1-A33F-D2C49E3DA0EA",
                    "startDate": "2025-01-02",
                    "quantity": 1
                }

            ]
        }
    }



    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    r = requests.post(url, json=payload, headers=headers, timeout=10)
    print("Status:", r.status_code)
    try:
        print("Response JSON:", json.dumps(r.json(), indent=2))
    except Exception:
        print("Response Text:", r.text)


if __name__ == "__main__":
    token = login_agent()
    create_b2b_booking(token)
