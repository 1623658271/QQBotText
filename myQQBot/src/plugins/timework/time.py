import random

from nonebot import on_command, require, get_bots
from nonebot.adapters.onebot.v11 import MessageSegment, Message
import asyncio
import os
from random import randint
from .config import Config

__plugin_name__ = 'timework'

img_path = 'file:///' + os.path.split(os.path.realpath(__file__))[0] + '/img/'

n = 0


# 发送图片时用到的函数, 返回发送图片所用的编码字符串
def send_img(img_name):
    global img_path
    return MessageSegment.image(img_path + img_name)


# 设置一个定时器
timing = require("nonebot_plugin_apscheduler").scheduler
timing2 = require("nonebot_plugin_apscheduler").scheduler


# 设置在23:30发送信息
@timing.scheduled_job("cron", hour='23', minute='40', id="night")
async def drink_tea():
    bot, = get_bots().values()
    contentNight = Config().getNightText()
    i = random.randint(1, 12)
    night_name = f'goodNight{i}.jpg'
    groups = Config().getUserInGroup()
    # 发送一条群聊信息
    for number in range(len(groups)):
        await bot.send_msg(
            message_type="group",
            # 群号
            group_id=groups[number],
            message=contentNight + send_img(night_name)
        )
    # 随机休眠2-5秒
    # await asyncio.sleep(randint(2, 5))
    # 发送一条私聊信息


# 设置在07:00发送信息
@timing2.scheduled_job("cron", hour='7', minute='00', id="morning")
async def good_morning():
    bot, = get_bots().values()
    contentMorning = Config().getMorningText()
    i = random.randint(1, 12)
    morning_name = f'goodMorning{i}.jpg'
    groups = Config().getUserInGroup()
    # 发送一条群聊信息
    for number in range(len(groups)):
        await bot.send_msg(
            message_type="group",
            # 群号
            group_id=groups[number],
            message=contentMorning + send_img(morning_name)
        )
