import this


class Config:
    # 记录不在哪些群组中使用
    used_in_group = ["00000000"]
    # 插件执行优先级
    priority = 10
    # 接话冷却时间（秒），在这段时间内不会连续两次接话
    chat_cd = 0
    # 戳一戳冷却时间（秒）
    notice_cd = 0
    # 机器人QQ号
    bot_id = "2534354342"
    # 管理员QQ号，管理员无视冷却cd和触发概率
    super_uid = ["1623658271"]
    # 聊天回复概率，用百分比表示，0-100%
    p_chat_response = 100
    # 戳一戳回复概率，用百分比表示，0-100%
    p_poke_response = 20
    # 默认禁言时间，每多戳一次会在默认禁言时间上翻倍
    default_ban_time = 60

    def add(self, a):
        file = open("C:\\Users\\浪客飞\\Desktop\\黑名单.txt", "a+", encoding="utf-8")
        file.writelines(str(a) + '\n')
        file.close()

    def delete(self, a):
        file = open("C:\\Users\\浪客飞\\Desktop\\黑名单.txt", "r+", encoding="utf-8")
        content = file.read().splitlines()
        for i in content:
            if str(a) == str(i):
                content.remove(str(a))
                break
        file.close()
        file = open("C:\\Users\\浪客飞\\Desktop\\黑名单.txt", "w+", encoding="utf-8")
        if content is not None:
            string = ""
            for k in content:
                string += k + '\n'
            file.write(string)
        file.close()

    def getBlack(self):
        file = open("C:\\Users\\浪客飞\\Desktop\\黑名单.txt", "r", encoding="utf-8")
        content = file.read().splitlines()
        file.close()
        return content
