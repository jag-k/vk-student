import time as py_time

from firebase_admin import credentials, initialize_app, firestore

from config import FIREBASE_APP_CONFIG, FIREBASE_APP_NAME


credential = credentials.Certificate(FIREBASE_APP_CONFIG)
token = credential.get_access_token().access_token

app = initialize_app(name=FIREBASE_APP_NAME, credential=credential)
db = firestore.client(app)

TIME = "time"
DATA = "str"


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
    return [max(objects, key=lambda obj: obj[TIME])]


def get_time_filtered_objects(objects: list, time: int):
    return list(filter(
            lambda obj: obj[TIME] >= time,
            objects
        ))


def get_document_data(doc_ref):
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
