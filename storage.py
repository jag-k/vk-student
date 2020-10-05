import time as py_time

from firebase_admin import credentials, initialize_app, firestore
from google.cloud.firestore_v1 import DocumentReference

from config import FIREBASE_APP_CONFIG, FIREBASE_APP_NAME
from models.party import PLAN_FREE, Party

credential = credentials.Certificate(FIREBASE_APP_CONFIG)
token = credential.get_access_token().access_token

app = initialize_app(name=FIREBASE_APP_NAME, credential=credential)
db = firestore.client(app)

TIME = "time"
DATA = "str"

COLLECTION_PARTIES = "parties"

party_collection = db.collection(COLLECTION_PARTIES)


def add_data(collection: str, data: str, subcollection="root"):
    # TODO: add various exception catching
    doc_ref = get_document_reference(collection, subcollection)

    add_new_data(doc_ref, data)

    return "ok"


def get_data(collection: str, subcollection="root", time: int = None):
    doc_ref = get_document_reference(collection, subcollection)
    objects = get_document_data(doc_ref)

    if time is None:
        return get_last_object(objects)
    else:
        return get_time_filtered_objects(objects, time)


def add_party(party: str, plan=PLAN_FREE):
    set_party(Party(party, plan))

    return "ok"


def get_party(party: str = None, chat: str = None):
    if party is not None:
        ref = get_party_reference(party)
        return get_party_model(ref)
    elif chat is not None:
        ref = get_party_by_chat(chat)
        return Party.from_dict(ref.to_dict())  # TODO: refactor
    else:
        raise Exception()


def set_party(party: Party):
    doc_ref = get_party_reference(party.name)
    doc_ref.set(
        party.to_dict()
    )

    return "ok"


def add_new_data(doc_ref, data: str):
    _data = get_document_data(doc_ref)

    doc_ref.set({
        DATA: _data + [{
            TIME: get_current_time(),
            DATA: data
        }]},
        merge=True
    )


def get_last_object(objects: list):
    try:
        return [max(objects, key=lambda obj: obj[TIME])]
    except ValueError:
        return []


def get_time_filtered_objects(objects: list, time: int):
    return list(filter(
            lambda obj: obj[TIME] >= time,
            objects
        ))


def get_document_data(doc_ref):
    # noinspection PyBroadException
    try:
        return doc_ref.get().to_dict()[DATA]
    except Exception:
        return []


def get_document_reference(collection, subcollection):
    return db\
        .collection(collection)\
        .document(subcollection)


def get_current_time():
    return int(round(py_time.time()))


def get_party_model(party_reference) -> Party:
    doc = party_reference.get().to_dict()

    return Party.from_dict(doc)


def get_party_reference(party_name) -> DocumentReference:
    return party_collection.document(party_name)


def get_party_by_chat(chat):
    return party_collection.where("chats", "array_contains", chat).limit(1).get()[0]
