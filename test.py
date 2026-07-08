import requests

WEBHOOK = "https://discord.com/api/webhooks/1524391012582031522/VglUKsC5wKvPVzuJVdYtf6OY6babLp2XEEgD4fwy-6MAW-ksrJTzvTtg_VM3cO07Gon6"

payload = {
    "content": "Hello from Python"
}

r = requests.post(WEBHOOK, json=payload)

print(r.status_code)
print(r.text)