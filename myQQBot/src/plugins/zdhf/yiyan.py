from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot, Message, MessageSegment, Event
from nonebot.plugin.on import on_regex, on_keyword
from nonebot.matcher import Matcher
import httpx
from nonebot import logger
from nonebot.exception import IgnoredException

hitokoto_matcher = on_keyword({"yy"}, block=True, priority=8)


@hitokoto_matcher.handle()
async def hitokoto(matcher: Matcher, event: Event):
    originContent = str(event.get_message())
    if not originContent.startswith('yy'):
        raise IgnoredException("响应格式出错！")
    content = originContent.split(' ')
    x = {
        '动画': 'a',
        '漫画': 'b',
        '游戏': 'c',
        '文学': 'd',
        '原创': 'e',
        '网络': 'f',
        '其他': 'g',
        '影视': 'h',
        '诗词': 'i',
        '网易云': 'j',
        '哲学': 'k',
    }
    if len(content) == 2 and content[1] in x:
        URL = f"https://v1.hitokoto.cn?c={x[content[1]]}"
    elif len(content) == 2 and content[1] == "分类":
        ll = tuple(x.keys())
        message = "随机一言的分类如下:\n"
        for i in ll:
            message += (f'[{i}]' + ',')
        URL = " "
        await hitokoto_matcher.finish(message)
    else:
        URL = "https://v1.hitokoto.cn?c=a&c=b&c=c&c=d&c=e&c=f&c=g&c=h&c=i&c=j&c=k"
    async with httpx.AsyncClient() as client:
        response = await client.get(url=URL)
    if response.is_error:
        logger.error("获取一言失败")
        return
    data = response.json()
    msg = data["hitokoto"]
    add = ""
    if works := data["from"]:
        add += f"《{works}》"
    if from_who := data["from_who"]:
        add += f"{from_who}"
    if add:
        msg += f"\n——{add}"
    await matcher.finish(msg)
