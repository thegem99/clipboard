import requests

SERVER = "https://your-app.up.railway.app"


def send_text(text):
    res = requests.post(
        SERVER + "/api/send",
        json={"data": text}
    )

    if res.status_code == 200:
        code = res.json()["code"]
        print("✅ Code:", code)
        return code
    else:
        print("❌ Error:", res.text)


def get_text(code):
    res = requests.get(SERVER + f"/api/get/{code}")

    if res.status_code == 200:
        data = res.json()["data"]
        print("📋 Data:", data)
        return data
    else:
        print("❌ Error:", res.text)


# Example usage
if __name__ == "__main__":
    choice = input("1 = Send | 2 = Receive: ")

    if choice == "1":
        text = input("Enter text: ")
        send_text(text)

    elif choice == "2":
        code = input("Enter code: ")
        get_text(code)
