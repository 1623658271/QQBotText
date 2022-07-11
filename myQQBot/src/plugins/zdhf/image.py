import random, os
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot, Message, MessageSegment, Event
from nonebot import on_keyword
from nonebot.typing import T_State
import requests
from aiohttp.client_exceptions import ClientError
from .config2 import Config

pic = on_keyword({'二次元', '二刺螈'}, block=True, priority=7)


@pic.handle()
async def _(bot: Bot, event: Event, state: T_State):
    if len(event.get_session_id().split("_")) == 3:
        _, group_id, user_id = event.get_session_id().split("_")
    else:
        user_id = str(event.get_user_id())
    if user_id not in Config().getBlack():
        url = await suijitu()
        msg = f"[CQ:image,file={url}]"
        try:
            await pic.send(Message(msg))
            download_img(url)
        except (IndexError, ClientError):
            await pic.send(Message("error"))
    else:
        await pic.finish(MessageSegment.at(str(user_id)) + "不好意思，你在黑名单中哦！")


async def suijitu():
    setuUrl = 'https://api.lolicon.app/setu'
    url = ['https://api.yimian.xyz/img', 'https://api.ghser.com/random/api.php']

    i = random.randint(0, 1)
    picture = requests.get(url[i])
    return picture.url


def download_img(img_url):
    r = requests.get(img_url, stream=True)
    i = 0
    if r.status_code == 200:
        while os.path.exists(f'C:\\Users\\浪客飞\\Desktop\\二次元图片\\二次元{i}.png'):
            i += 1
        open(f'C:\\Users\\浪客飞\\Desktop\\二次元图片\\二次元{i}.png', 'wb').write(r.content)  # 将内容写入图片
    del r
