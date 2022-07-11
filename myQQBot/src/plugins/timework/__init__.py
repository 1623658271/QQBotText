from .time import *
from nonebot import on_command, logger, on_keyword
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, Event, MessageEvent
from nonebot.permission import SUPERUSER
from .config import Config

addToGroup = on_keyword({'开启早晚安文案'}, priority=1, block=True, permission=SUPERUSER)
deleteFromGrop = on_keyword({'关闭早晚安文案'}, priority=1, block=True, permission=SUPERUSER)


@addToGroup.handle()
async def _(event: Event):
    _, group_id, user_id = event.get_session_id().split("_")
    if group_id in Config().getUserInGroup():
        await addToGroup.finish(f"群{group_id}已开启!")
    else:
        Config().add(str(group_id))
        await addToGroup.finish(f"已开启群{group_id}的早晚安文案推送")


@deleteFromGrop.handle()
async def _(event: Event):
    _, group_id, user_id = event.get_session_id().split("_")
    if group_id in Config().getUserInGroup():
        Config().delete(str(group_id))
        await deleteFromGrop.finish(f"已关闭群{group_id}的早晚安文案推送")
    else:
        await deleteFromGrop.finish(f"群{group_id}未开启!")
