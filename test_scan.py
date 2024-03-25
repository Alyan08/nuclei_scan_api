import requests


target = "http://127.0.0.1:5001"
severity = "medium"

url_scan = f'http://127.0.0.1:5001/api/scan/start?target={target}&severity={severity}'

req_headers = {
    'X-API-KEY': '123456'
}

resp = requests.post(url=url_scan, headers=req_headers, verify=False)

print(resp.status_code)
print(resp.text)

