from models.party import Party
from storage import db

COLLECTION_PARTIES = "parties"


def check_access(party_name):
    party = get_party(party_name)

    return not party.is_something_reached


def get_party(party_name):
    ref = get_party_reference(party_name)

    return get_party_model(ref)


def get_party_model(party_reference):
    doc = party_reference.get().to_dict()

    return Party.from_dict(doc)


def get_party_reference(party_name):
    return db\
        .collection(COLLECTION_PARTIES)\
        .document(party_name)
