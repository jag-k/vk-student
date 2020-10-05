import storage
from models.party import PLAN_FREE, Party

ACCESS_DENIED_RESULT = "Вы не можете сделать этого, лимиты исчерпаны"


def add_data(collection: str, data: str, subcollection=storage.ROOT_SUBCOLLECTION, party: str = ''):
    if check_access(party):
        update_party_usage_amount(party, 1, len(data))

        return storage.add_data(
            build_collection_name(party, collection),
            data,
            subcollection
        )
    else:
        return ACCESS_DENIED_RESULT


def get_data(collection: str, subcollection=storage.ROOT_SUBCOLLECTION, time: int = None, party: str = ''):
    if check_access(party):
        update_party_usage_amount(party, 1, 0)

        return storage.get_data(
            build_collection_name(party, collection),
            subcollection,
            time
        )
    else:
        return [{"str": ACCESS_DENIED_RESULT}]


def add_party(party: str, plan=PLAN_FREE):
    return storage.add_party(party, plan)


def get_party(party: str = None, chat: str = None):
    return storage.get_party(party=party, chat=chat)


def set_party(party: Party):
    return storage.set_party(party)


def update_party_usage_amount(name: str, request_count=0, usage=0):
    party = get_party(party=name)
    party.request_count += request_count
    party.usage += usage

    storage.set_party(party)

    return party


def check_access(party_name) -> bool:
    party = storage.get_party(party_name)

    return not party.is_something_reached


def build_collection_name(party: str, collection: str):
    return party+'_'+collection
