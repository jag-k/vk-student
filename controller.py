import access
import storage


def add_data(collection: str, data: str, subcollection="root", party: str = ''):
    if access.check_access(party):
        return storage.add_data(
            build_collection_name(party, collection),
            data,
            subcollection
        )
    else:
        return "Access denied"


def get_data(collection: str, subcollection="root", time: int = None, party: str = ''):
    if access.check_access(party):
        return storage.get_data(
            build_collection_name(party, collection),
            subcollection,
            time
        )
    else:
        return "Access denied"


def build_collection_name(party: str, collection: str):
    return party+'_'+collection
