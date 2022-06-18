import shutil
import time
import requests
import json
import os


# 爬取最新的ip地址信息
def get_latest_ip():
    url = 'https://www.***json.com/s.json'  #获取json数据的爬虫地址
    resp = requests.get(url)
    json_data = json.loads(resp.text)
    prefixes = json_data['prefixes']

    # 记录首次请求获取到的信息
    f = open('file_01', 'w+')
    for item in prefixes:
        if 'ipv4Prefix' in item.keys():
            f.write(item['ipv4Prefix'] + '\n')
    f.close()


# 对比两个文件不同之处，并返回结果
def compare_ip_list():
    message = ''
    if os.path.exists('file_02'):
        fp1 = open('file_01')
        fp2 = open('file_02')
        file_list1 = [i for i in fp1]
        file_list2 = [x for x in fp2]
        fp1.close()
        fp2.close()
        for item in file_list1:
            if item not in file_list2:
                message = (message + 'ip 新增：' + item)
        for item in file_list2:
            if item not in file_list1:
                message = (message + '减少：' + item)
    else:
        with open('file_02', 'w'):
            message = '首次数据已获取'
    return message


# 发送 webhook 请求
def webhook_request(message_content):
    webhook_url = 'https://open.feishu.cn/open-apis/bot/v2/hook/*****'
    headers = {'Content-Type': 'application/json'}
    webhook_message = '【ip地址变更告警】 \n【详细信息】：\n %s' % message_content
    payload = {'msg_type': 'text', 'content': {'text': webhook_message}}
    requests.post(webhook_url, headers=headers, json=payload)


if __name__ == '__main__':
    try:
        get_latest_ip()
        send_message = compare_ip_list()
        if len(send_message) == 0:
            print('数据一致')
        elif send_message == '首次数据已获取':
            webhook_request(send_message)
        else:
            # 备份旧数据
            backup_file = time.strftime("%Y%m%d_%H:%M", time.localtime()) + '.log'
            shutil.copyfile('file_02', backup_file)

            webhook_request(send_message)
        os.rename('file_01', 'file_02')
    except:
        print('数据检测失败！')
