import json
from pathlib import Path

from bson import ObjectId

from website.qapi.database import db


def import_entities():
    folder = Path(__file__).parent
    with open(folder / 'entities.json', 'r', encoding='utf-8') as f:
        text = f.read()

    entities = json.loads(text)
    db.drop()
    for ent_dict in entities:
        uid = ObjectId(ent_dict['_id']['$oid'])
        ent_dict['_id'] = uid
        db.insert_one(ent_dict)

if __name__ == '__main__':
    import_entities()