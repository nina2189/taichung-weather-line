import json
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

CWA_API_KEY = "CWA-C2A9D003-668C-4B88-9A43-952B87902D00"
LINE_TOKEN = "ovPcLgBzyxMsqwLjx2d/AToVtViPzXgf1r0rcrwNpf/B9eJG6M92FI3a1LK7daQgftLWCQ22H6yq9AbTtiK6mIMnhVSq0ShOz7CRyh/SQx2nnQ94VTvQvkqqr9Uo/Y2H5Y1m6g57b+Ssc0I6bI1LwdB04t89/1O/w1cDnyilFU="
USER_ID = "U1536e6ab5269bfd96c67970dcb4092ef"

def main():
    url = f"https://opendata.cwa.gov.tw/api/v1/rest/datastores/F-C0032-001?Authorization=CWA-B969C6D1-AF9D-46C1-B2A2-8B3F25A3F7A1"
    response = requests.get(url, verify=False).json()

    all_locations = response["records"]["location"]
    taichung_data = next(item for item in all_locations if item["locationName"] == "臺中市")

    weather_elements = taichung_data["weatherElement"]
    pop_element = next(item for item in weather_elements if item["elementName"] == "PoP")
    rain_chance = int(pop_element["time"]["parameter"]["parameterName"])

    threshold = 0

    if rain_chance >= threshold:
        line_url = f"https://line.me/v2/bot/message/push"
        headers = {
            "Authorization": f"Bearer {LINE_TOKEN}",
            "Content-Type": "application/json"
        }
        payload = {
            "to": USER_ID,
            "messages": [{
                "type": "text",
                "text": f"🌧️【出門提醒】目前台中預報降雨機率達 {rain_chance}%，出門記得帶傘喔！"
            }]
        }
        res = requests.post(line_url, headers=headers, json=payload)
        print(f"Status Code: {res.status_code}")
    else:
        print(f"Chance: {rain_chance}%")

if __name__ == "__main__":
    main()
