import urllib.request, json

payload = {
    "action": {
        "type": "commentCard",
        "memberCreator": {"fullName": "Mike"},
        "data": {
            "text": "@jarvis direct test from python",
            "card": {"name": "Test Card", "shortLink": "abc123"}
        }
    }
}

data = json.dumps(payload).encode()
req = urllib.request.Request(
    "http://127.0.0.1:8078/",
    data=data,
    headers={"Content-Type": "application/json"},
    method="POST"
)
r = urllib.request.urlopen(req)
print("Response:", r.read().decode())
