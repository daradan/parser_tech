MARKET = 'Mechta'
URL = 'https://www.mechta.kz/api/new/catalog'
# https://www.mechta.kz/api/new/catalog?section=noutbuki&page=1&properties=&page_limit=24&cache_city=s1
URL_PRICES = 'https://www.mechta.kz/api/new/mindbox/actions/catalog'
URL_REFERER = 'https://www.mechta.kz/section/'
URL_CATEGORY = 'https://www.mechta.kz/api/new/header/menu'

HEADER = {
    'sec-ch-ua': '"Chromium";v="106", "Not.A/Brand";v="24", "Opera";v="92"',
    'X-XSRF-TOKEN': 'eyJpdiI6IitZblJhT3NoTzlDZHpDK2JIN0dIbnc9PSIsInZhbHVlIjoieElzWGIrNDNjb2dkcTZJYWprcHMwRlVGOFkr'
                    'QTlMdWZkTTkxTTlSRWlSTlJHNFVIRVhlZXlleG56T0QrOUlEL084TXpnNHBnRytFSGJDbjEzY2JCZ29ubExObG5kd0Na'
                    'ZlRBRS94ZnR4MW11QVU2MGVlTEFUNG1yTExpQmdSZisiLCJtYWMiOiI2NzQ5NTliN2Y2ODRmNTU4MDdmMDZjMWNmMTRk'
                    'ZWI3MGJhMDllMjM0YmY2MjMzODEzMjdiMmMxNTQwMzNlMTRiIiwidGFnIjoiIn0=',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/106.0.0.0 Safari/537.36 OPR/92.0.0.0',
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'https://www.mechta.kz/',
    'x-city-code': 's1',
    'sec-ch-ua-platform': '"Linux"',
}

PARAMS = {
    'section': 'noutbuki',
    'page': '1',
    'properties': '',
    'page_limit': '24',
    'cache_city': 's1',
}

HEADERS_PRICES = {
    'authority': 'www.mechta.kz',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'multipart/form-data; boundary=----WebKitFormBoundaryAA0pDZttI4J3Yrsj',
    'origin': 'https://www.mechta.kz',
    'referer': 'https://www.mechta.kz/section/noutbuki/',
    'sec-ch-ua': '"Chromium";v="106", "Not.A/Brand";v="24", "Opera";v="92"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/106.0.0.0 Safari/537.36 OPR/92.0.0.0',
    'x-city-code': 's1',
    'x-xsrf-token': 'eyJpdiI6IitZblJhT3NoTzlDZHpDK2JIN0dIbnc9PSIsInZhbHVlIjoieElzWGIrNDNjb2dkcTZJYWprcHMwRlVGOFkrQTl'
                    'MdWZkTTkxTTlSRWlSTlJHNFVIRVhlZXlleG56T0QrOUlEL084TXpnNHBnRytFSGJDbjEzY2JCZ29ubExObG5kd0NaZlRBRS'
                    '94ZnR4MW11QVU2MGVlTEFUNG1yTExpQmdSZisiLCJtYWMiOiI2NzQ5NTliN2Y2ODRmNTU4MDdmMDZjMWNmMTRkZWI3MGJhM'
                    'DllMjM0YmY2MjMzODEzMjdiMmMxNTQwMzNlMTRiIiwidGFnIjoiIn0=',
}

DATA_1 = '------WebKitFormBoundaryAA0pDZttI4J3Yrsj\r\nContent-Disposition: form-data; name="product_ids"\r\n\r\n'
DATA_2 = '\r\n------WebKitFormBoundaryAA0pDZttI4J3Yrsj--\r\n'
# data = '------WebKitFormBoundaryAA0pDZttI4J3Yrsj\r\nContent-Disposition: form-data; name="product_ids"\r\n\r\n
# 72287,4951,70933,71698,20591,70030,71050,71769,71539,70843,71458,71243,69024,71611,8692,70905,71045,51255,45176,
# 71364,70901,4033,71977,69763\r\n------WebKitFormBoundaryAA0pDZttI4J3Yrsj--\r\n'
