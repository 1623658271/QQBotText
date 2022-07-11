from nonebot import on_keyword,on_regex
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot, Message, Event, MessageSegment
import requests
from .config2 import Config

xljt = on_regex(r"^jt$", priority=7)


@xljt.handle()
async def lj(bot: Bot, event: Event, state: T_State):
    if len(event.get_session_id().split("_")) == 3:
        _, group_id, user_id = event.get_session_id().split("_")
    else:
        user_id = str(event.get_user_id())
    if user_id not in Config().getBlack():
        lovelive_send = await xi()
        at_ = str(event.get_user_id())
        await xljt.send(MessageSegment.at(at_) + Message(lovelive_send))
    else:
        await xljt.finish(MessageSegment.at(str(user_id))+"不好意思，你在黑名单中哦！")


async def xi():
    url = 'http://api.yanxi520.cn/api/xljtwr.php?charset=utf-8http://api.yanxi520.cn/api/xljtwr.php?encode=txt'
    hua = requests.get(url=url)
    # print(hua)
    data = hua.text
    # print(data)
    return data
