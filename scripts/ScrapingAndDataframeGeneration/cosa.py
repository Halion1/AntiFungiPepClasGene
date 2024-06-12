import requests
import json

headers = {
    'authority': 'dbaasp.org',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'referer': 'https://dbaasp.org/search',
    'accept-language': 'es-ES,es;q=0.9,en;q=0.8',
    'cookie': '_ga=GA1.2.2057967460.1637161193; _gid=GA1.2.2090110016.1637268982; AWSALB=iBHwvnXJRuPaiYJ6kvmFIlrcgqoHbi+U834xCpZfpK8JKNnq9PKB5buQDX8hcaZahHPOHZc9uGrP0YGbmK0aUuALoMgVLtanTyjRZDrUx1b3k3XsuENOvT9g0krx; AWSALBCORS=iBHwvnXJRuPaiYJ6kvmFIlrcgqoHbi+U834xCpZfpK8JKNnq9PKB5buQDX8hcaZahHPOHZc9uGrP0YGbmK0aUuALoMgVLtanTyjRZDrUx1b3k3XsuENOvT9g0krx',
}

params = (
    ('id', '8'),
)

response = requests.get('https://dbaasp.org/peptide-card', headers=headers, params=params)

#a = json.loads(response)



print(response.json())

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://dbaasp.org/peptide-card?id=8', headers=headers)