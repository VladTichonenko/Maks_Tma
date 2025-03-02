# Open the file with UTF-8 encoding

import requests

headers = {
    'sec-ch-ua-platform': '"Android"',
    'Referer': 'https://www.binance.com/',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Mobile Safari/537.36',
    'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
    'sec-ch-ua-mobile': '?1',
}

response = requests.get('https://public.bnbstatic.com/unpkg/common-widget/data@1.3.621.min.js', headers=headers)
with open('result.html', 'w', encoding='utf-8') as file:
    file.write(response.text)