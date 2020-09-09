import storage
from models.party import PLAN_FREE, Party


def add_data(collection: str, data: str, subcollection="root", party: str = ''):
    if check_access(party):
        update_party_usage_amount(party, 1, len(data))

        return storage.add_data(
            build_collection_name(party, collection),
            data,
            subcollection
        )
    else:
        return "Access denied"


def get_data(collection: str, subcollection="root", time: int = None, party: str = ''):
    if check_access(party):
        update_party_usage_amount(party, 1, 0)

        return storage.get_data(
            build_collection_name(party, collection),
            subcollection,
            time
        )
    else:
        return "Access denied"


def add_party(party: str, plan=PLAN_FREE):
    return storage.add_party(party, plan)


def get_party(party: str):
    return storage.get_party(party)


def update_party_usage_amount(name: str, request_count=0, usage=0):
    party = get_party(name)
    new_party = Party(
        name,
        party.plan,
        party.request_count + request_count,
        party.usage + usage
    )

    storage.set_party(new_party)

    return new_party


def check_access(party_name) -> bool:
    party = storage.get_party(party_name)

    return not party.is_something_reached


def build_collection_name(party: str, collection: str):
    return party+'_'+collection
