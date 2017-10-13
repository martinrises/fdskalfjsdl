import urllib.request
import csv

data_indices = ['AG1306', 'AG1701', 'AG1603', 'AG1507', 'AG1808', 'AG1210', 'AG888', 'AG1801', 'AG1607', 'AG1411', 'AG1809', 'AG1305', 'AG1706', 'AG1307', 'AG1703', 'AG1802', 'AG1303', 'AG1606', 'AG1609', 'AG1404', 'AG1612', 'AG1509', 'AG1508', 'AG1608', 'AG1702', 'AG1501', 'AG1311', 'AG1602', 'AG1709', 'AG1408', 'AG1412', 'AG1610', 'AG1707', 'AG1804', 'AG1711', 'AG1512', 'AG1302', 'AG1601', 'AG1410', 'AG1805', 'AG1503', 'AG1312', 'AG1211', 'AG1407', 'AG1301', 'AG1504', 'AG1502', 'AG1209', 'AG1405', 'AG1705', 'AG99', 'AG1505', 'AG1605', 'AG1803', 'AG1304', 'AG1708', 'AG1401', 'AG1310', 'AG1403', 'AG1212', 'AG1402', 'AG88', 'AG1611', 'AG1406', 'AG1510', 'AG1807', 'AG1712', 'AG1308', 'AG1704', 'AG1309', 'AG1710', 'AG1506', 'AG1806', 'AG1604', 'AG1409', 'AG1511']


def save_csv(filename, content_str):
    with open('../data/future/by/{}.csv'.format(filename), 'w', newline='') as f:
        f.write(content_str)



for index in data_indices:
    headers = {"Host":'www.ricequant.com',
           "Upgrade-Insecure-Requests": "1",
           "Save-Data": "on",
           "User-Agent": "Mozilla/5.0 (Linux; Android 7.0; SM-G9280 Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.98 Mobile Safari/537.36",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
           "DNT": "1",
           "Referer": "https://www.ricequant.com/research/user/user_306589/edit/data/future/by/{}_daily_price.csv".format(index),
           "Accept-Language": "zh-CN,en-US;q=0.8,en;q=0.6,de-DE;q=0.4,de;q=0.2,zh;q=0.2",
           "Cookie": "jupyter-hub-token-user_306589=\"2|1:0|10:1507780502|29:jupyter-hub-token-user_306589|44:OWUzZjcxNmM5MGQ3NDViZWJlZmYyNDQyNjlmYjUxNWQ=|e5cd46be711b217b0899a5db0e8fe8ebe0e31629e033c06f8a1c73615630e87b\"; tgw_l7_route=d0bf4a9ab78d53762b596c0a48da8e7f; gr_user_id=5bfc743c-4b79-404c-8311-20cdf671e1e0; jupyter-hub-token=\"2|1:0|10:1507780502|17:jupyter-hub-token|44:OWUzZjcxNmM5MGQ3NDViZWJlZmYyNDQyNjlmYjUxNWQ=|b6335ed6cf4c19ad6146b06320cdf1d9d62d951de8b4c31884b08935a81611b9\"; jupyter-hub-token-user_306589=\"2|1:0|10:1507780502|29:jupyter-hub-token-user_306589|44:OWUzZjcxNmM5MGQ3NDViZWJlZmYyNDQyNjlmYjUxNWQ=|e5cd46be711b217b0899a5db0e8fe8ebe0e31629e033c06f8a1c73615630e87b\"; sid=6098a390-6e5b-452b-9f5c-fa17e4eebc2a|746a0a57664067d9a775f8172818e293fddf51966d61b5c88c5e1571e4732fe267c292ff20ce3678bc6160d8ec860dc8d5a5eb30d349840d537d559924387f3e; Hm_lvt_cb81fd54150b99e25d085d58bbaf4a07=1507780478; Hm_lpvt_cb81fd54150b99e25d085d58bbaf4a07=1507780541; gr_session_id_9bc6807c25b59135=8c241e1c-805d-460f-9d28-397eea3d2a22; gr_cs1_8c241e1c-805d-460f-9d28-397eea3d2a22=user_id%3A306589' --compressed 'https://www.ricequant.com/research/user/user_306589/files/data/future/by/AG1209_daily_price.csv?download=1"}
    url = 'https://www.ricequant.com/research/user/user_306589/files/data/future/by/{}_daily_price.csv?download=1'.format(index)
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as response:
        response_str = response.read().decode('gbk', 'ignore')
        print(response_str)
        save_csv(index, response_str)