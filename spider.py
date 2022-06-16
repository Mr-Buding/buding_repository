import requests
import json

resp = requests.get('https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId=59307779813&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1')
content = resp.text
rest = content.replace('fetchJSON_comment98(', '').replace(');', '')
json_data = json.loads(rest)
comments = json_data['comments']

for item in comments:
  referenceTime = item['referenceTime']
  integral = item['integral']
  print(referenceTime)
  print(integral)