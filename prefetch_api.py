from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import time,requests

app = FastAPI()

#自定义一个Pydantic模型
class Item(BaseModel):
   url_list: list


#获取需要预热的 url 列表，并写入文件
@app.post("/xuduojie/cdn_prefetch")
async def get_url_list(item: Item):
    url_list_file = open('url_file_list', 'w+', newline='')
    for i in item.url_list:
        url_list_file.write(i + '\n')
    url_list_file.close()

    i = 1
    while i < 3:
        for line in open('url_file_list'):
            # 删除字符串末尾的换行符
            rs = line.rstrip('\n')

            # 发送get请求
            a = requests.get(url=rs)
            status_code = str(a.status_code)

            # 创建日志文件并写入记录
            file_name = time.strftime('%Y%m%d', time.localtime()) + '_cdn_prefetch_log.txt'
            file = open(file_name, 'a+', newline='')
            file.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' ')
            file.write(str(a.elapsed.microseconds) + ' ')
            file.write(status_code + '  ')
            file.write(rs + '\n')
            file.close()
            time.sleep(1)
        i += 1

if __name__ == '__main__':
    uvicorn.run(app='prefetch_api:app', host='0.0.0.0', port=8811, proxy_headers=True, forwarded_allow_ips='*', reload=True)
