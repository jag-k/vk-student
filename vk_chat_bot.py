import random

import vk_api
from vk_api.bot_longpoll import VkBotEventType as VkEventType
from vk_api.bot_longpoll import VkBotLongPoll as VkLongPoll

from config import VK_CHAT_API_KEY, VK_GROUP_ID
from controller import add_data, get_data

# TODO: add localisation
DATA_SET = ["#запиши"]
DATA_GET = ["#дай"]
DATA_EDITING_METHODS = DATA_SET + DATA_GET

WRONG_TASK = "wt"  # wtf


def write_msg(chat_id, message):
    vk.method('messages.send', {'random_id': random.randint(1, 2147483647), 'chat_id': chat_id, 'message': message})


def is_setting_data(message):
    return any(map(
        lambda word: word in DATA_SET,
        message.split()
    ))


def is_getting_data(message):
    return any(map(
        lambda word: word in DATA_GET,
        message.split()
    ))


def is_using_data(message):
    return any(map(
        lambda word: word in DATA_EDITING_METHODS,
        message.split()
    ))


def on_new_task(message, party, chat_id):
    if is_using_data(message):
        on_using_data(message, party, chat_id)
    else:
        on_error(WRONG_TASK)


def on_using_data(message, party, chat_id):
    if is_setting_data(message):
        on_setting_data(message, party, chat_id)
    elif is_getting_data(message):
        on_getting_data(message, party, chat_id)


def on_setting_data(message, party, chat_id):
    collections, data = parse_task(message)

    if len(collections) >= 2:
        write_msg(chat_id, add_data(collections[0], data, "".join(collections[1:]), party=party))
    else:
        write_msg(chat_id, add_data(collections[0], data, party=party))


def on_getting_data(message, party, chat_id):  # TODO: add time
    collections, other = parse_task(message)

    if len(collections) >= 2:
        data = get_data(collections[0], "".join(collections[1:]), party=party)
    else:
        data = get_data(collections[0], party=party)

    if len(data) > 0:
        write_msg(chat_id, data[0]["str"])
    else:
        write_msg(chat_id, "пусто")


def on_error(error_name: str):
    if error_name == WRONG_TASK:
        pass


def parse_task(task):
    i = 0
    split = task.split(DATA_GET[i])

    while len(split) == 1:
        i += 1
        split = task.split(DATA_GET[i])

    task = split[1].split()
    collections = task[0].split("-")
    other = " ".join(task[1:])

    return collections, other


# TODO: create singleton MainLooper?
def start_main_loop(longpoll):
    while True:
        try:
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW:
                    on_new_task(event.object["text"], "test_party", event.chat_id)
        except Exception:  # TODO: add exception catching
            pass


if __name__ == '__main__':
    vk = vk_api.VkApi(token=VK_CHAT_API_KEY)

    start_main_loop(VkLongPoll(vk, group_id=VK_GROUP_ID))
