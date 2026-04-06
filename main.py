import tkinter as tk
import requests

SERVER = "https://clipboardserver-production.up.railway.app/"  # change this


def send_text():
    text = send_box.get("1.0", tk.END).strip()

    if not text:
        result_label.config(text="Enter some text")
        return

    try:
        res = requests.post(
            SERVER + "/api/send",
            json={"data": text}
        )
        code = res.json().get("code")
        result_label.config(text=f"Code: {code}")
    except Exception as e:
        result_label.config(text=f"Error: {e}")


def get_text():
    code = code_entry.get().strip()

    if not code:
        result_label.config(text="Enter code")
        return

    try:
        res = requests.get(SERVER + f"/api/get/{code}")
        data = res.json()

        if "data" in data:
            receive_box.delete("1.0", tk.END)
            receive_box.insert(tk.END, data["data"])
            result_label.config(text="Received!")
        else:
            result_label.config(text=str(data))

    except Exception as e:
        result_label.config(text=f"Error: {e}")


# UI setup
root = tk.Tk()
root.title("Online Clipboard")

# SEND SECTION
tk.Label(root, text="Send Text").pack()
send_box = tk.Text(root, height=5, width=40)
send_box.pack()

tk.Button(root, text="Send", command=send_text).pack()

# RECEIVE SECTION
tk.Label(root, text="Enter Code").pack()
code_entry = tk.Entry(root)
code_entry.pack()

tk.Button(root, text="Receive", command=get_text).pack()

receive_box = tk.Text(root, height=5, width=40)
receive_box.pack()

result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()
