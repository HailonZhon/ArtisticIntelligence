import os.path
from typing import Union

from pathlib import Path
import requests
import base64

import nonebot
from nonebot import get_driver, on_command
from nonebot.adapters.onebot.v11 import (
    Bot,
    GroupMessageEvent,
    PrivateMessageEvent,
    MessageSegment,
    LifecycleMetaEvent
)
from .config import Config

global_config = get_driver().config
config = Config.parse_obj(global_config)

_sub_plugins = set()
_sub_plugins |= nonebot.load_plugins(
    str((Path(__file__).parent / "plugins").resolve())
)


async def txt_2_img(keyword):
    url = "http://172.18.3.1:7861/sdapi/v1/txt2img"
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


txt2img = on_command("//")


@txt2img.handle()
async def _(event: Union[GroupMessageEvent, PrivateMessageEvent]):
    message = event.message
    keyword = str(message).split('//')
    img_file = await txt_2_img(keyword=keyword)
    await txt2img.finish(MessageSegment.image(img_file), at_sender=True)
