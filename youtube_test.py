import requests

API_KEY = "YOUR_API_KEY_HERE"
channel_id = "UC_x5XG1OV2P6uZZ5FSM9Ttw"  # Example: Google Developers

url = f"https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&id={channel_id}&key={API_KEY}"

response = requests.get(url)
data = response.json()

print(data)
