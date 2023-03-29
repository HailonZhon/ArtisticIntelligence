import base64

import requests


def txt_2_img(keyword):
    url = "http://172.18.3.1:7860/sdapi/v1/txt2img"
    data = {
        'prompt': f'{keyword}'}
    headers = {
        'Content-Type': 'application/json'
    }

    # 将 params 作为 json 数据传递给 post 请求的 data 参数
    resp = requests.post(url, json=data, headers=headers, timeout=60)
    img = resp.json()['images'][0]
    # 以二进制模式打开文件并写入响应内容
    return base64.b64decode(img)


if __name__ == '__main__':
    data = txt_2_img('girl')
    with open('test.png', 'wb') as f:
        f.write(data)
