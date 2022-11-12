MARKET = 'Sulpak'

URL = 'https://api.sulpak.kz/v0/kz/3/3'
URL_IMAGE = 'https://object.pscloud.io/cms/cms/Photo/'

HEADER = {
    'Accept-Charset': 'UTF-8',
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1Lz'
                     'A1L2lkZW50aXR5L2NsYWltcy9uYW1lIjoiZ2xvYmFsLWN1c3RvbWVyLWFwcC1jb25zdW1lciIsImVtYWlsIjoiZ2xvYmFs'
                     'LWN1c3RvbWVyLWFwcC1jb25zdW1lckBhcGkuc3VscGFrLmt6IiwiYXVkIjoiYXBpQ29uc3VtZXIiLCJpc3MiOiJhcGkuc3'
                     'VscGFrLmt6IiwiZXhwIjoiMTY2ODMzNTQxMyIsIm5iZiI6IjE2NjgyNDkwMTMiLCJodHRwOi8vc2NoZW1hcy5taWNyb3Nv'
                     'ZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3JvbGUiOiJnbG9iYWwtY3VzdG9tZXItYXBwIn0.NJoPqL4_Y_'
                     'Dk4TMVMxVGxnXv7aIdw7av4ojlVCNJ9qw',
    'NetworkConsumer': 'mobile-app',
    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 12; 21081111RG Build/SP1A.210812.016)',
    'Host': 'api.sulpak.kz',
}

JSON_DATA = {
    'page': 1,
    'classId': 83,
    'goodsPerPage': 8,
    'orderBy': 5,
    'priceFrom': 0,
    'priceTo': 2147483647,
    'catalogObjectFilter': {
        'itemsCount': 0,
        'minPrice': 0,
        'maxPrice': 0,
        'tagsIds': None,
        'availability': None,
        'signs': None,
        'rating': None,
        'filtersAvailabilitiesAndSignsCounts': None,
        'stocks': None,
        'tags': None,
        'properties': None,
        'selectedProperties': None,
        'ratings': None,
        'handAddedLinks': None,
    },
    'commentsCount': None,
    'query': None,
}