import random

import vk_api
from vk_api.longpoll import VkEventType
from vk_api.longpoll import VkLongPoll

from config import VK_GROUP_API_KEY, VK_GROUP_ID
from controller import add_party

# TODO: add localisation
REGISTRATION_INIT = ["/рег"]

WRONG_TASK = "wt"  # wtf


def write_msg(user_id, message):
    vk.method('messages.send', {'random_id': random.randint(1, 2147483647), 'user_id': user_id, 'message': message})


def is_adding_party(message):
    return any(map(
        lambda word: word in REGISTRATION_INIT,
        message.split()
    ))


def on_new_task(message, user_id):
    if is_adding_party(message):
        write_msg(user_id, add_party(str(user_id)))
    else:
        on_error(WRONG_TASK)


def on_error(error_name: str):
    if error_name == WRONG_TASK:
        pass


# TODO: create singleton MainLooper?
def start_main_loop(longpoll):
    while True:
        try:
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW:
                    on_new_task(event.message, event.user_id)
        except Exception:  # TODO: add exception catching
            pass


if __name__ == '__main__':
    vk = vk_api.VkApi(token=VK_GROUP_API_KEY)

    start_main_loop(VkLongPoll(vk, group_id=VK_GROUP_ID))
