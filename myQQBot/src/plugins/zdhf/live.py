from nonebot import on_keyword, on_command,on_regex
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Message, Bot, Event, MessageSegment
import datetime
from .config2 import Config

# 输入关键字'ch'触发
Live = on_regex(pattern=r"^ch$", priority=7)


@Live.got('live', prompt='请回复你的出生日期\n如:2003 9 27\n可回复\'取消\'停止')
async def get_live_time(bot: Bot, state: T_State, event: Event):
    if len(event.get_session_id().split("_")) == 3:
        _, group_id, user_id = event.get_session_id().split("_")
    else:
        user_id = str(event.get_user_id())
    if user_id not in Config().getBlack():
        global monthList
        a = state['live']
        if str(a) == "取消":
            await Live.finish("已取消")
        if len(str(a).split(' ')) < 3 or not (
                str(a).split(" ")[0] + str(a).split(" ")[1] + str(a).split(" ")[2]).isdigit():
            await Live.reject("你是不是在逗我呀！")
        else:
            birth_time = str(a)
            t = datetime.date.today()
            birth_list = []
            for birth in str(birth_time).split(' '):
                birth_list.append(birth)
            year = int(t.year) - int(birth_list[0])
            birthYear = int(birth_list[0])
            sumMonth = 0
            sumDay = 0
            if int(birth_list[0]) <= 1900:
                await Live.reject("你逗我呢,这都多少岁了？我反正不信")
            if int(birth_list[0]) > t.year or (
                    int(birth_list[0]) == t.year and (
                    int(birth_list[1]) > t.month or (int(birth_list[1]) == t.month and int(birth_list[2]) > t.day))):
                await Live.reject("你逗我呢,从未来来的？我反正不信")
            monthListInit = [31, 29 if ((birthYear % 4 == 0 and birthYear % 100 != 0) or birthYear % 400 == 0) else 28,
                             31,
                             30, 31, 30, 31, 31, 30, 31, 30, 31]
            if int(birth_list[1]) not in range(1, 13):
                await Live.reject("日期输入错误")
            m = int(birth_list[1])
            if int(birth_list[2]) > monthListInit[m - 1]:
                await Live.reject("日期输入错误")

            # 计算逻辑部分
            while birthYear <= t.year:
                monthList = [31, 29 if ((birthYear % 4 == 0 and birthYear % 100 != 0) or birthYear % 400 == 0) else 28,
                             31,
                             30, 31, 30, 31, 31, 30, 31, 30, 31]
                if birthYear != t.year:
                    for i in monthList:
                        sumDay += i
                    sumMonth += 12
                else:
                    for j in range(0, t.month - 1):
                        sumDay += monthList[j]
                    sumMonth += t.month
                    sumDay += t.day
                birthYear += 1

            sumMonth -= int(birth_list[1])
            for k in range(0, int(birth_list[1]) - 1):
                sumDay -= monthListInit[k]
            sumDay -= int(birth_list[2]) - 1

            if t.year > int(birth_list[0]) and (
                    t.month < int(birth_list[1]) or (t.month == int(birth_list[1]) and t.day < int(birth_list[2]))):
                year -= 1
            second = datetime.datetime.now().second + datetime.datetime.now().hour * 60 * 60 + datetime.datetime.now().minute * 60

            # 组织语言
            send = f"\n你已经存在这个世界上:{year}年\n你在这个世界上存在了:{sumMonth}月\n今天是你存在这个世界上的第{sumDay}天\n" \
                   f"你已经存在这个世界上:{(sumDay - 1) * 86400 + second}秒\n好好珍惜在世上的每一天哦！"
            if t.month == int(birth_list[1]) and t.day == int(birth_list[2]):
                send += f"\n今天是你的生日呢！\n生日快乐！"

            # 发送
            await Live.finish(MessageSegment.at(str(event.get_user_id())) + f"{send}")
    else:
        await Live.finish(MessageSegment.at(str(user_id))+"不好意思，你在黑名单中哦！")
