import urllib.request
import csv

data_indices = ['601328.XSHG', '600519.XSHG', '601688.XSHG', '601901.XSHG', '600030.XSHG', '601601.XSHG', '600016.XSHG', '601186.XSHG', '600485.XSHG', '601390.XSHG', '601800.XSHG', '601288.XSHG', '600606.XSHG', '600028.XSHG', '601318.XSHG', '600111.XSHG', '600048.XSHG', '601628.XSHG', '601818.XSHG', '600958.XSHG', '601766.XSHG', '600547.XSHG', '600036.XSHG', '601006.XSHG', '600000.XSHG', '601985.XSHG', '600999.XSHG', '601668.XSHG', '600887.XSHG', '601088.XSHG', '601198.XSHG', '601881.XSHG', '600104.XSHG', '601989.XSHG', '601398.XSHG', '600919.XSHG', '600029.XSHG', '601988.XSHG', '601857.XSHG', '600340.XSHG', '601169.XSHG', '600100.XSHG', '600518.XSHG', '600050.XSHG', '601166.XSHG', '601788.XSHG', '601229.XSHG', '601336.XSHG', '600837.XSHG', '601211.XSHG']


def save_csv(filename, content_str):
    with open('../data/sz50/{}.csv'.format(filename), 'w', newline='') as f:
        f.write(content_str)


headers = {"Accept":'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           "Accept-Language": "zh-CN,en-US;q=0.8,en;q=0.6,de-DE;q=0.4,de;q=0.2,zh;q=0.2",
           "Cache-Control": "max-age=0",
           "Connection": "keep-alive",
           "Cookie": "jupyter-hub-token-user_306589=\"2|1:0|10:1505374090|29:jupyter-hub-token-user_306589|44:ODRkN2QwOWY4ZjRlNDFlMWIyZWQ1Nzg1N2MxMTI3YTI=|48f93966c7ce950bff27e935ec994b77020388344f8b7affe215cf5333eb0315\"; gr_user_id=16ec036a-0bf8-45c0-bfd4-b6615672e98f; jupyter-hub-token-user_306589=\"2|1:0|10:1505368487|29:jupyter-hub-token-user_306589|44:ODRkN2QwOWY4ZjRlNDFlMWIyZWQ1Nzg1N2MxMTI3YTI=|baa71061c969c693fd62bb88756bc584e20e554135401d36a32e96a57ee3621a\"; jupyter-hub-token=\"2|1:0|10:1505368487|17:jupyter-hub-token|44:ODRkN2QwOWY4ZjRlNDFlMWIyZWQ1Nzg1N2MxMTI3YTI=|83517b83dd40909a9adf77adaa2a6a86440ac936268db067f44adee59c3ac691\"; connect.sid=s%3Ahx25Uvo0rtmPJ9lisZhZbheKHpbl1gVN.TesisdiuFcRnZZnCSwpSV%2BQREm4WztjfTeTOa%2BIptwg; tgw_l7_route=c54242301fc532aead997498daeb37fa; sid=b9baff27-a8e6-466b-8c83-a48160f9a04b|78a7ae8c016c35db67950ee6ac59055bc0e5f02966b09cba4c679423a31c9486ddb6ca47552210d5d1003352a0151fb03afc27c2863e1cc3f6043fe5ad37e5ba; Hm_lvt_cb81fd54150b99e25d085d58bbaf4a07=1504061859,1504148682,1505368426; Hm_lpvt_cb81fd54150b99e25d085d58bbaf4a07=1505378914; gr_session_id_9bc6807c25b59135=ceecf950-8401-4738-96f3-059a25e5bef2; gr_cs1_ceecf950-8401-4738-96f3-059a25e5bef2=user_id%3A306589",
           "DNT": "1",
           "Host": "www.ricequant.com",
           "Upgrade-Insecure-Requests": "1",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"}

for index in data_indices:
    url = 'https://www.ricequant.com/research/user/user_306589/files/data/{}_daily_price.csv'.format(index)
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as response:
        response_str = response.read().decode('gbk', 'ignore')
        print(response_str)
        save_csv(index, response_str)