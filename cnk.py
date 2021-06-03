

import requests
from datetime import datetime, timedelta

base_cowin_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"
now =datetime.now()
print("date :", now.strftime("%d-%m-%Y"))
today_date = now.strftime("%d-%m-%Y")
api_url_telegram = "https://api.telegram.org/(yourbootid)/sendMessage?chat_id=@__groupid__&text="
group_id= "your group id"
kerala_district_ids =[ 295, 296, 297, 298, 299, 300, 301, 302,303]

def fetch_data_from_cowin(district_id):
    query_params = "?district_id={}&date={}".format(district_id, today_date)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
    final_url = base_cowin_url+query_params
    response = requests.get(final_url, headers=headers)
    extract_availability_data(response)
    #print(response.text)

def fetch_data_for_state(district_ids):
    for district_id in district_ids:
        fetch_data_from_cowin(district_id)

def extract_availability_data(response):
    response_json =response.json()
    for center in response_json["centers"]:
        for session in center["sessions"]:
            if session["available_capacity_dose1"] > 0  or session["available_capacity_dose2"] > 0:
                if session["min_age_limit"]==45: #or 18
                    message = "Date: {}, Pincode: {}, Name: {}, Dose1: {}, Dose2: {}, Vaccine: {}, Minimum Age: {}".format(
                        session["date"], center["pincode"], center["name"],
                        session["available_capacity_dose1"], session["available_capacity_dose2"], session["vaccine"],
                        session["min_age_limit"]
                    )
                    send_message_telegram(message)

def send_message_telegram(message):
    final_telegram_url=api_url_telegram.replace("__groupid__", group_id)
    final_telegram_url=final_telegram_url + message
    response = requests.get(final_telegram_url)
    print(response.text)

if __name__=="__main__":
    fetch_data_for_state(kerala_district_ids)
