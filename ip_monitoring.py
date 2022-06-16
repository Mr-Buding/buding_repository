import requests
import time,json
import os
#获取最新的ip地址信息
def get_latest_ip():
    url = 'https://www.gstatic.com/ipranges/goog.json'
    f2 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '.json'
    resp = requests.get(url)

    #记录首次请求获取到的信息
    f = open('f2.json', 'w+')
    #f.write(resp.text['prefixes'])
    #写入json格式
    f.write(str(eval(resp.text)['prefixes']))

#    for i in json_data:
#        if 'ipv4Prefix' == i.keys:
#            print('hahaha')



#对比两个文件不同之处，并返回结果


if __name__ == '__main__':
    get_latest_ip()

