import requests
from config import API_KEY

response = requests.post(
    'https://api.remove.bg/v1.0/removebg',
    data={
        'image_url': '',
        'size': 'auto'
    },
    headers={'X-Api-Key': API_KEY},
)
if response.status_code == requests.codes.ok:
    with open('no-bg.png', 'wb') as out:
        out.write(response.content)
else:
    print("Error:", response.status_code, response.text)
