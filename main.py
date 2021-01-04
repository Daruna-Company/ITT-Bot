import vk_api, vk
from vk_api.utils import get_random_id
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from config import info, data, progects, users, commands
import func as f

class Bot:
    def __init__(self, i):
        self.token = i["token"]
        self.group_id = i["group_id"]
        self.key = i["key"]
        self.server = i["server"]
        self.ts = i["ts"]

        self.vk_session = vk_api.VkApi(token=self.token)
        self.longpoll = VkLongPoll(self.vk_session)
        self.vk = self.vk_session.get_api()

    def send_msg(self, text, peer):
        self.vk.messages.send(
            user_id = peer,
            random_id = get_random_id(),
            message = text
            )

    def start(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text and event.user_id not in data["ban"]:
                """simple command"""
                if event.text.lower() == "/оборудование":
                    text = ""
                    for i in data["tech"]:
                        text += f"{i}\n"
                    self.send_msg(text, event.user_id)

                elif event.text.lower() == "/бюджет компании":
                    self.send_msg("бюджет компании состовляет {0} рублей".format(data["money"]), event.user_id)
                elif event.text.lower() == "/сайт":
                    self.send_msg(data["web-site"], event.user_id)
                elif event.text.lower() == "/бот":
                    self.send_msg("бот был сделан на заказ компанией Daruna", event.user_id)
                elif event.text.lower() == "/проекты в разработке":
                    text = ""

                    for i in progects["dev"]:
                        text += i
                    if text == "":
                        self.send_msg("не один проект в данный момент не разрабатывается", event.user_id)
                    else:
                        self.send_msg(text, event.user_id)
                elif event.text.lower() == "/оконченные проекты":
                    text = ""

                    for i in progects["ready"]:
                        text += i
                    if text == "":
                        self.send_msg("не один проект в данный момент не готов", event.user_id)
                    else:
                        self.send_msg(text, event.user_id)
                elif event.text.lower() == "/приостановленные проекты":
                    text = ""

                    for i in progects["stoped"]:
                        text += i
                    if text == "":
                        self.send_msg("в данный момент приостановленных проектов нет", event.user_id)
                    else:
                        self.send_msg(text, event.user_id)
                elif event.text.lower() == "/лучшие проекты":
                    text = ""

                    for i in progects["best"]:
                        text += i
                    if text == "":
                        self.send_msg("в данный момент лучших проектов нет", event.user_id)
                    else:
                        self.send_msg(text, event.user_id)
                elif event.text.lower() == "/профиль":
                    profile = f.getProfileInfo(event.user_id)
                    if profile != None:
                        self.send_msg("имя - {0}\nid - {1}\nуровень технологии - {2}".format(profile[0], profile[1], profile[2]), event.user_id)
                    else:
                        self.send_msg("вы ещё не зарегистрированны", event.user_id)
                elif event.text.lower().find("/зарегистрироваться") != -1:
                    t = event.text.split(" ")
                    if f.getProfileInfo(event.user_id) == None:
                        data["users_id"].append(int(event.user_id))
                        f.register(t[1], event.user_id)
                        self.send_msg("вы зарегистрированны под именем {0}".format(t[1]), event.user_id)
                    else:
                        self.send_msg("вы уже зарегистрированны", event.user_id)
                elif event.text.lower() == "/пользователи":
                    self.send_msg(len(f.getUsers()), event.user_id)
                elif event.text.lower() == "/время компании":
                    self.send_msg("компания ITT была создана 25 ноября 2020 года", event.user_id)
                elif event.text.lower() == "/команды":
                    self.send_msg(commands, event.user_id)
                elif event.text.lower() == "/инфо":
                    self.send_msg("Дарова, сейчас ты находишься в самом крутом IT сообществе IT Techlogies(ITT). \
Здесь наша команда создаёт проекты, делает игры и постит информацию об IT.\n! ПОДПИШИСЬ !", event.user_id)
                elif event.text.lower() == "/vip":
                    if event.user_id in data["vip"]:
                        self.send_msg("у вас есть подписка vip", event.user_id)
                    else:
                        self.send_msg("у вас нет подписки vip", event.user_id)
                """for VIP"""
                if event.user_id in data["vip"]:
                    if event.text.lower().find("$give") != -1:
                        msg = event.text.split(" ")
                        if int(msg[1]) >= 1 and int(msg[1]) <= 10:
                            print(f.add(int(msg[2]), event.user_id))
                            if f.add(int(msg[1]), event.user_id) == 0:
                                self.send_msg("у пользователя(https://vk.com/id{0}) нет аккаунта".format(event.user_id), event.user_id)
                            else:
                                self.send_msg("пользователю(https://vk.com/id{0}) было добавленно {1} уровней технологии".format(event.user_id, msg[1]), event.user_id)
                """for moder"""
                if event.user_id in data["admins"]:
                    if event.text.lower().find(":изменить бюджет") != -1:
                        data["money"] = event.text.split(" ")[2]
                        self.send_msg("теперь бюджет компании состовляет {0} рублей".format(data["money"]), event.user_id)
                    elif event.text.lower().find(":вип") != -1:
                        data["vip"].append(int(event.text.split(" ")[1]))
                        self.send_msg("пользователю(https://vk.com/id{0}) был выдан статус вип".format(event.text.split(" ")[1]), event.user_id)
                    elif event.text.lower().find(":бан") != -1:
                        data["ban"].append(int(event.text.split(" ")[1]))
                        self.send_msg("пользователю(https://vk.com/id{0}) был выдан бан".format(event.text.split(" ")[1]), event.user_id)
                    elif event.text.lower().find(":новый лучший:") != -1:
                        s = event.text.split(":")
                        progects["best"].append(s[2])
                    elif event.text.lower().find(":новый готовый:") != -1:
                        s = event.text.split(":")
                        progects["ready"].append(s[2])
                    elif event.text.lower().find(":новый разрабатываемый:") != -1:
                        s = event.text.split(":")
                        progects["dev"].append(s[2])
                    elif event.text.lower().find(":новый приостановленный:") != -1:
                        s = event.text.split(":")
                        progects["stoped"].append(s[2])
                    elif event.text.lower().find(":удалить лучший:") != -1:
                        s = event.text.split(":")
                        try:
                            progects["best"].remove(s[2])
                        except:
                            pass
                    elif event.text.lower().find(":удалить готовый:") != -1:
                        s = event.text.split(":")
                        try:
                            progects["ready"].remove(s[2])
                        except:
                            pass
                    elif event.text.lower().find(":удалить разрабатываемый:") != -1:
                        s = event.text.split(":")
                        try:
                            progects["dev"].remove(s[2])
                        except:
                            pass
                    elif event.text.lower().find(":удалить приостановленный:") != -1:
                        s = event.text.split(":")
                        try:
                            progects["stoped"].remove(s[2])
                        except:
                            pass

if __name__ == "__main__":
    x = Bot(info)
    x.start()
