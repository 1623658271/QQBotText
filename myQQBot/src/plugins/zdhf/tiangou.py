from nonebot import on_keyword,on_regex
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot, Message, MessageSegment, Event
import requests
from .config2 import Config

tgrj = on_regex(r"^tg$", priority=7)


# GroupMessageEvent

@tgrj.handle()
async def lj(bot: Bot, event: Event, state: T_State):
    if len(event.get_session_id().split("_")) == 3:
        _, group_id, user_id = event.get_session_id().split("_")
    else:
        user_id = str(event.get_user_id())
    if user_id not in Config().getBlack():
        lovelive_send = await xi()
        # at_ = f"[CQ:at,qq={event.get_user_id()}]"
        await tgrj.send(Message(lovelive_send))
    else:
        await tgrj.finish(MessageSegment.at(str(user_id)) + "不好意思，你在黑名单中哦！")


async def xi():
    url = 'http://api.yanxi520.cn/api/tiangou.php'
    hua = requests.get(url=url)
    # print(hua)
    data = hua.text
    # print(data)
    return data
