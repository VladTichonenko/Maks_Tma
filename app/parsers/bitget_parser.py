# parsers/bitget_parser.py
from .base_parser import BaseParser
import requests
import json

class BitgetParser(BaseParser):
    def get_staking_info(self, coin: str) -> dict:
        try:
            normalized_coin = self.normalize_coin_name(coin)
            
            
            cookies = {
        'theme': 'white',
        'fingerprint-1740922752419-45917-0.0061586564075784': 'true',
        'terminalCode-1740922752420-45918.60000000009-0.37192332077880597': 'true',
        'BITGET_LOCAL_COOKIE': '{%22bitget_lang%22:%22ru%22%2C%22bitget_unit%22:%22USD%22%2C%22bitget_showasset%22:false%2C%22bitget_theme%22:%22dark%22%2C%22bitget_valuationunit_new%22:1%2C%22bitget_layout%22:%22right%22}',
        '_dx_kvani5r': 'be97bea55d20570b35df0c3cff6f4cf9df084a6f84ba9b50dcc7b4e59b28bf22d007ef90',
        'OptanonAlertBoxClosed': 'Sun%20Mar%2002%202025%2016:44:40%20GMT+0300%20(%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%2C%20%D1%81%D1%82%D0%B0%D0%BD%D0%B4%D0%B0%D1%80%D1%82%D0%BD%D0%BE%D0%B5%20%D0%B2%D1%80%D0%B5%D0%BC%D1%8F)',
        'OptanonConsent': 'isMarketing=1&isStatistic=1',
        'dy_token': '67c582d99SMXY7HaWrPJVvL0aIYoicMJTL2iotk1',
        }

            headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7,de-DE;q=0.6,de;q=0.5',
        'baggage': 'sentry-environment=online,sentry-release=git%20rev-parse%20HEAD,sentry-public_key=d8b5c66bfb5c4f11a4aa8a755525bc70,sentry-trace_id=06a6e5719024429db5c245035bb95021,sentry-sample_rate=0,sentry-transaction=%2Fearning%2Fstaking,sentry-sampled=false',
        'content-type': 'application/json;charset=UTF-8',
        'deviceid': '303a3a349d4e29697aa91355c84ae796',
        'dy-token': '67c582d99SMXY7HaWrPJVvL0aIYoicMJTL2iotk1',
        'language': 'ru_RU',
        'locale': 'ru_RU',
        'origin': 'https://www.bitget.fit',
        'priority': 'u=1, i',
        'referer': 'https://www.bitget.fit/ru/earning/staking',
        'sec-ch-ua': '"Not(A:Brand";v="99", "Microsoft Edge";v="133", "Chromium";v="133"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sentry-trace': '06a6e5719024429db5c245035bb95021-9fdd4a432bd7d3e1-0',
        'terminalcode': 'b0c877f4b04e6e2fe3cf6901208ad1b9',
        'terminaltype': '1',
        'tm': '1741009732048',
        'uhti': 'w174100973204851c46d05d17',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0',
        }

            response = requests.post(
                'https://www.bitget.fit/v1/finance/pos/cardList',
                cookies=cookies,
                headers=headers,
                json={'locale': 'ru', 'matchUserAssets': False},
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                return self.parse_response(data, normalized_coin)
            
            self.logger.error(f"Bitget API error: {response.status_code}")
            return None
            
        except Exception as e:
            self.logger.error(f"Bitget parser error: {str(e)}")
            return None

    def parse_response(self, data: dict, coin: str) -> dict:
        for item in data.get('data', []):
            if item.get('productCoinName') == coin:
                return {
                    'exchange': 'Bitget',
                    'min_apy': float(item.get('minApy', 0)),
                    'max_apy': float(item.get('maxApy', 0))
                }
        return None