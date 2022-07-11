import json
import random
import re
import time
from nonebot.rule import to_me
import requests
from nonebot.typing import T_State
from nonebot import on_command, on_keyword, on_notice
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot, Message, MessageSegment, Event
from nonebot.plugin.on import on_regex
from nonebot.params import EventToMe
from nonebot.permission import SUPERUSER
from .config2 import Config

weather = on_keyword({'emo', 'wy'}, block=True, priority=7)
cici = on_keyword({''}, rule=to_me(), block=True, priority=6)
qh = on_regex(pattern=r"^qh$", priority=7)
help = on_regex(pattern=r"^功能$", rule=to_me, priority=1)


@weather.handle()
async def handle_first_receive(event: Event):
    if len(event.get_session_id().split("_")) == 3:
        _, group_id, user_id = event.get_session_id().split("_")
    else:
        user_id = str(event.get_user_id())
    if user_id not in Config().getBlack():
        plain_text = str(event.get_message())
        if plain_text == 'wy':
            city_weather = await get_emo()
            await weather.finish(city_weather)
        if plain_text == 'emo':
            hour = int(time.strftime("%H"))
            if hour in {23, 0, 1, 2, 3, 4, 5}:
                city_weather = await get_emo2()
                await weather.finish(city_weather)
            else:
                await weather.finish(f"当前不在emo时段(23:00——5:00),好好学习哦!")
    else:
        await weather.finish(MessageSegment.at(str(user_id)) + "不好意思，你在黑名单中哦！")


@cici.handle()
async def sj(event: Event):
    if len(event.get_session_id().split("_")) == 3:
        _, group_id, user_id = event.get_session_id().split("_")
    else:
        user_id = str(event.get_user_id())
    if user_id not in Config().getBlack():
        ansek = str(event.get_message())
        yuyin = False
        if ansek.startswith("语音"):
            yuyin = True
            ansek = ansek.replace("语音", "")
        if '天道' in ansek:
            ansek = ansek.replace('天道', '菲菲')
        if r'[CQ:face,id=' in ansek:
            p1 = re.compile(r'[\[](.*?)[\]]', re.S)
            h = re.findall(p1, ansek)
            if len(h[0]) == 12:
                ansek = ansek.replace('[' + h[0] + ']', '{' + f'face:{h[0][11]}' + '}')
            elif len(h[0]) == 13:
                ansek = ansek.replace('[' + h[0] + ']', '{' + f'face:{h[0][11]}{h[0][12]}' + '}')
            elif len(h[0]) == 14:
                ansek = ansek.replace('[' + h[0] + ']', '{' + f'face:{h[0][11]}{h[0][12]}{h[0][13]}' + '}')

        url = f'http://api.qingyunke.com/api.php?key=free&appid=0&msg={ansek}'
        k = requests.get(url)
        hua = json.loads(k.text)
        #  获取返回json数据中回复的部分(content)
        ans = hua['content']
        if '{face:' in ans:
            yuyin = False
            p1 = re.compile(r'[{](.*?)[}]', re.S)
            h = re.findall(p1, ans)
            if len(h[0]) == 6:
                ans = ans.replace('{' + h[0] + '}', f'[CQ:face,id={h[0][5]}]')
            elif len(h[0]) == 7:
                ans = ans.replace('{' + h[0] + '}', f'[CQ:face,id={h[0][5]}{h[0][6]}]')
            elif len(h[0]) == 8:
                ans = ans.replace('{' + h[0] + '}', f'[CQ:face,id={h[0][5]}{h[0][6]}{h[0][7]}]')

        l = '菲菲'
        m = '{br}'
        at_ = str(event.get_user_id())
        if ans == '未获取到相关信息':
            ans = '未获取到相关信息,你可以@我并发送功能查看我目前拥有的功能'
        if l in ans:
            ansl = ans.replace('菲菲', '天道')
            if m in ansl:
                ansl = ansl.replace('{br}', '\n')
            if yuyin:
                await cici.finish(Message(f'[CQ:tts,text={ansl}]'))
            else:
                await cici.finish(MessageSegment.at(at_) + Message(f'{ansl}'))
        elif m in ans:
            ansm = ans.replace('{br}', '\n')
            if yuyin:
                await cici.finish(Message(f'[CQ:tts,text={ansm}]'))
            else:
                await cici.finish(MessageSegment.at(at_) + Message(f'{ansm}'))
        else:
            if yuyin:
                await cici.finish(Message(f'[CQ:tts,text={ans}]'))
            else:
                await cici.finish(MessageSegment.at(at_) + Message(f'{ans}'))
    else:
        await cici.finish(MessageSegment.at(str(user_id)) + "不好意思，你在黑名单中哦！")


@qh.handle()
async def lj(bot: Bot, event: GroupMessageEvent, state: T_State):
    if len(event.get_session_id().split("_")) == 3:
        _, group_id, user_id = event.get_session_id().split("_")
    else:
        user_id = str(event.get_user_id())
    if user_id not in Config().getBlack():
        lovelive_send = await xi()
        at_ = str(event.get_user_id())
        await qh.send(MessageSegment.at(at_) + Message(lovelive_send))
    else:
        await qh.finish(MessageSegment.at(str(user_id)) + "不好意思，你在黑名单中哦！")


@help.handle()
async def helped(bot: Bot, event: Event, state: T_State):
    if len(event.get_session_id().split("_")) == 3:
        _, group_id, user_id = event.get_session_id().split("_")
    else:
        user_id = str(event.get_user_id())
    if user_id not in Config().getBlack():
        h = "天道目前的功能如下:\n1.emo/wy 可随机读取网易云热评进行推送\n2.qh 推送土味情话\n3.@我+要说的话我就可以回复你(" \
            "或发送help获得帮助)【前面加上'语音'则会回复语音消息】\n4.点歌\n5.二次元/二刺螈 " \
            "随机发送小清新图片\n6.tg 推送一篇天狗日记\n7.ch 帮助查看你在世上的存活时间(绝对精确,不服打我)\n8.jt 推送心灵鸡汤\n" \
            "9.yy 推送随机一言(可加分类属性如'yy 动画'，输入'yy 分类'查看一言的分类)"
        await help.send(Message(h))
    else:
        await help.finish(MessageSegment.at(str(user_id)) + "不好意思，你在黑名单中哦！")


async def xi():
    url = 'https://api.uomg.com/api/rand.qinghua?format=json'
    hua1 = requests.get(url=url)
    # print(hua)
    hua = json.loads(hua1.text)
    data = hua['content']
    # print(data)
    return data


# 在这里编写获取emo信息的函数
async def get_emo() -> str:
    with open("C:\\Users\\浪客飞\\Desktop\\python\\song_comments.json", 'r', encoding='utf8') as fp:
        json_data = json.load(fp)
    a = random.randint(0, 199)
    name = json_data['data'][a]['songName']
    b = random.randint(1, 14)
    x = f'content{b}'
    content = json_data['data'][a][x]

    return f"{content}\n———网易云热评《{name}》"


# 在这里编写获取emo2信息的函数
async def get_emo2() -> str:
    with open("C:\\Users\\浪客飞\\Desktop\\python\\song_comments2.json", 'r', encoding='utf8') as fp:
        json_data = json.load(fp)
    a = random.randint(0, 199)
    name = json_data['data'][a]['songName']
    b = random.randint(1, 14)
    x = f'content{b}'
    content = json_data['data'][a][x]

    return f"{content}\n———网易云热评《{name}》"
