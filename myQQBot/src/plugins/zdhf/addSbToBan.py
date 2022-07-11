import nonebot
from nonebot import on_command, logger, on_keyword
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, Event, MessageEvent
from nonebot.permission import SUPERUSER
from nonebot.message import event_preprocessor
from nonebot.exception import IgnoredException
from .utils import At
from .config2 import Config

ban = on_keyword({'加入黑名单'}, priority=1, block=True, permission=SUPERUSER)
unban = on_keyword({'移出黑名单'}, priority=1, block=True, permission=SUPERUSER)
check = on_keyword({'查看黑名单'}, priority=1, block=True, permission=SUPERUSER)


# ban = on_command('禁', priority=1, block=True, permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER)

@ban.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    """
    /禁 @user 禁言
    """
    msg = str(event.get_message()).removeprefix("加入黑名单")
    sb = At(event.json())
    if len(sb) > 0:
        sb = str(sb[0])
    else:
        await ban.finish(f"未知错误")

    if sb not in Config().getBlack():
        Config().add(sb)
        await ban.finish(f"将{sb}加入黑名单成功！")
    else:
        await ban.finish(f"{sb}已在黑名单中！")


@unban.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    """
    /解 @user 解禁
    """
    msg = str(event.get_message()).removeprefix("移出黑名单")
    sb = At(event.json())
    if len(sb) > 0:
        sb = str(sb[0])
    else:
        await ban.finish(f"未知错误")

    if sb in Config().getBlack():
        Config().delete(sb)
        await ban.finish(f"将{sb}移出黑名单成功！")
    else:
        await ban.finish(f"{sb}不在黑名单中！")


@check.handle()
async def _(bot: Bot, event: Event):
    """
    查看黑名单
    """
    content = Config().getBlack()
    if len(content) > 0:
        final = "当前黑名单中的QQ号如下："
        for i in content:
            final += ('\n' + i)
    else:
        final = "当前黑名单中没有任何QQ号"
    await check.finish(final)


@event_preprocessor
def namelist_processor(event: MessageEvent):
    uid = str(event.user_id)
    if uid in Config().getBlack():
        logger.debug(f"用户 {uid} 在黑名单中, 忽略本次消息")
        raise IgnoredException("黑名单用户")
