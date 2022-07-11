import os
import random


class Config:
    # 插件执行优先级
    priority = 5

    # 记录在哪些群组中使用
    def getUserInGroup(self):
        file = open("C:\\Users\\浪客飞\\Desktop\\早晚安文案开启群.txt", "r+", encoding="utf-8")
        content = file.read().splitlines()
        file.close()
        return content

    def getMorningText(self):
        file = open("C:\\Users\\浪客飞\\Desktop\\早安文案.txt", "r", encoding="utf-8")
        content = file.readlines()
        i = random.randint(0, len(content) - 1)
        num = 1
        for x in content[i]:
            if x.isdigit():
                num += 1
            else:
                break
        file.close()
        return content[i][num:].replace('\n', '')

    def getNightText(self):
        file = open("C:\\Users\\浪客飞\\Desktop\\晚安文案.txt", "r", encoding="utf-8")
        content = file.readlines()
        i = random.randint(0, len(content) - 1)
        num = 1
        for x in content[i]:
            if x.isdigit():
                num += 1
            else:
                break
        file.close()
        return content[i][num:].replace('\n', '')

    def add(self, a):
        file = open("C:\\Users\\浪客飞\\Desktop\\早晚安文案开启群.txt", "a+", encoding="utf-8")
        file.writelines(str(a) + '\n')
        file.close()

    def delete(self, a):
        file = open("C:\\Users\\浪客飞\\Desktop\\早晚安文案开启群.txt", "r+", encoding="utf-8")
        content = file.read().splitlines()
        for i in content:
            if str(a) == str(i):
                content.remove(str(a))
                break
        file.close()
        file = open("C:\\Users\\浪客飞\\Desktop\\早晚安文案开启群.txt", "w+", encoding="utf-8")
        if content is not None:
            string = ""
            for k in content:
                string += k + '\n'
            file.write(string)
        file.close()