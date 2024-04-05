import requests

response = requests.post(
    'https://api.remove.bg/v1.0/removebg',
    files={'image_file': open('Mr.Mirmakhmudov logo.jpg', 'rb')},
    data={'size': 'auto'},
    headers={'X-Api-Key': 'PdrqPD5pgievjUhouJjhhf8v'},
)
if response.status_code == requests.codes.ok:
    with open('no-bg.png', 'wb') as out:
        out.write(response.content)
else:
    print("Error:", response.status_code, response.text)
