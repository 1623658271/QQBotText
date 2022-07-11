from nonebot import on_message, on_notice
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from time import time
import os
from nonebot.adapters.onebot.v11 import MessageSegment, Message
import json
from collections import Counter
from random import randint
from .config2 import Config

# 针对戳一戳
chat_notice = on_notice()

poke_ban_list = {""}


# 初始化
# for group_id in Config.used_in_group:
#   poke_ban_list[group_id] = {}
@chat_notice.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    global last_notice_response
    global last_notice_nickname
    global response
    try:
        ids = event.get_session_id()
    except:
        pass
    # 如果读取正常没有出错，因为有些notice格式不支持session
    else:
        # 如果这是一条群聊信息
        if ids.startswith("group"):
            if len(event.get_session_id().split("_")) == 3:
                _, group_id, user_id = event.get_session_id().split("_")
            else:
                user_id = str(event.get_user_id())
                group_id = '0'
            # 不对列表中的群使用
            if group_id not in Config.used_in_group:
                description = event.get_event_description()
                values = json.loads(description.replace("'", '"'))
                # 如果被戳的是机器人
                if values['notice_type'] == 'notify' and values['sub_type'] == 'poke' and str(
                        values['target_id']) == Config.bot_id:

                    # 如果是超级管理员戳的
                    # if user_id in Config.super_uid:
                    #   await chat_notice.send(f"[CQ:poke,qq={str(user_id)}")
                    #  await chat_notice.finish(MessageSegment.at(str(user_id)) + Message("如果是你的话，想戳多少次都可以哦~"))
                    # 如果不在响应cd
                    # elif time() - last_notice_response[group_id] >= Config.notice_cd:
                    # if randint(0, 99) < Config.p_poke_response:
                    #    last_notice_response[group_id] = time()
                    #    infos = str(await bot.get_stranger_info(user_id=values['user_id']))
                    #    nickname = json.loads(infos.replace("'", '"'))['nickname'] + '(' + str(
                    #       values['user_id']) + ')'
                    #   last_notice_nickname[group_id] = nickname
                    #   response = 0
                    #   # 清空ban列表
                    #   poke_ban_list[group_id] == {}
                    #   await chat_notice.finish(
                    #    nickname + "谢谢你戳了我，我自由了，现在你是新的群机器人了~" + MessageSegment.image(img_path + '坏心思.jpg'))
                    # else:
                    #   if response == 0:
                    if randint(0, 99) < Config.p_poke_response:
                        # response += 1
                        await chat_notice.send(MessageSegment.at(str(user_id)) + "不要随便戳我啦！")
                    await chat_notice.finish(f"[CQ:poke,qq={str(user_id)}]")
                    # elif response == 1:
                #    if randint(0, 99) < Config.p_poke_response:
                #       response += 1
                #      if user_id in poke_ban_list[group_id]:
                #         poke_ban_list[group_id][user_id] += 1
                #    else:
                #       poke_ban_list[group_id][user_id] = 1
                #  await chat_notice.finish("再这样就不理你了！")
                # elif response == 2:
                #   if randint(0, 99) < Config.p_poke_response:
                #      response += 1
                #     # 如果戳过了，那么每戳一次就把禁言时间翻倍
                #    if user_id in poke_ban_list[group_id]:
                #       poke_ban_list[group_id][user_id] += 1
                #  else:
                #      poke_ban_list[group_id][user_id] = 1
                #  try:
                #      await bot.set_group_ban(group_id=group_id, user_id=user_id,
                #                              duration=Config.default_ban_time * (
                #                                      2 ** (poke_ban_list[group_id][user_id] - 1)))
                #  except:
                #      pass
                #  await chat_notice.finish("mdzz！再戳我报警了！" + MessageSegment.image(img_path + '报警.jpg'))
                #  else:
                #     # 如果戳过了，那么每戳一次就把禁言时间翻倍
                #    if user_id in poke_ban_list[group_id]:
                #       poke_ban_list[group_id][user_id] += 1
                #  else:
                #     poke_ban_list[group_id][user_id] = 1
                # try:
                #     await bot.set_group_ban(group_id=group_id, user_id=user_id,
                #                             duration=Config.default_ban_time * (
                #                                     2 ** (poke_ban_list[group_id][user_id] - 1)))
                # except:
                #     pass
