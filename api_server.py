from fastapi import FastAPI
import requests
import uvicorn

app = FastAPI()


SMILEONE_COOKIE = "l4edbbk4lcifbj2osd5vt9ee6j"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Cookie": SMILEONE_COOKIE,
    "X-Requested-With": "XMLHttpRequest"
}

@app.get("/")
def home():
    return {"status": "Server is running perfectly!"}

@app.get("/api/v1/check")
def check_user(player_id: str, zone_id: str):
    url = "https://www.smile.one/merchant/mobilelegends/checkrole"
    payload = {
        "user_id": player_id,
        "zone_id": zone_id,
        "pid": "22",
        "checkrole": "1"
    }
    try:
        response = requests.post(url, headers=headers, data=payload, timeout=15)
        res_json = response.json()
        if "username" in res_json:
            return {"status": "success", "username": res_json["username"]}
        elif "failing" in res_json:
            return {"status": "error", "message": res_json.get("failing")}
        else:
            return {"status": "success", "username": res_json.get("role", "Unknown")}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/v1/balance")
def check_balance():
    url = "https://www.google.com/ccm/collect?rcb=7&frm=0&ae=g&auid=1418056186.1782296841&dt=Smile.One%20-%20(Brazil)%20%7C%20Cr%C3%A9ditos%20de%20Jogos%20e%20Servi%C3%A7os&en=page_view&dl=https%3A%2F%2Fwww.smile.one%2F&scrsrc=www.googletagmanager.com&rnd=488253308.1784636109&navt=r&npa=0&ep.ads_data_redaction=0&gtm=45He67h1v812213746za200zd812213746xea&gcd=13l3l3l3l1l1&dma=0&tag_exp=115938465~115938469~118897920~118897930~119732171&apve=1&apvf=f&apvc=1&tft=1784636109325&tfd=1281&fmt=8"
    
    try:
        response = requests.post(url, headers=headers, timeout=15)
        
        print("--- [SmileOne Raw Response Start] ---")
        print(response.text[:500])
        print("--- [SmileOne Raw Response End] ---")

        if response.status_code == 200:
            try:
                res_json = response.json()
                data = res_json.get("data", res_json)
                money = data.get("money") or data.get("balance") or data.get("credit")
                currency = data.get("currency", "PH")
                
                if money is not None:
                    return {"status": "success", "money": str(money), "currency": str(currency)}
                else:
                    return {"status": "error", "message": f"Response structure: {res_json}"}
            except Exception:
                return {"status": "error", "message": "SmileOne returned HTML instead of JSON. Check Terminal output."}
        else:
            return {"status": "error", "message": f"HTTP {response.status_code}"}
            
    except Exception as e:
        return {"status": "error", "message": str(e)}