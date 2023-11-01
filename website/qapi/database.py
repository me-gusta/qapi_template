import pymongo

from website.constants import DB_NAME

db = pymongo.MongoClient()[DB_NAME].get_collection("entities")

db.create_index(
    [('slug', pymongo.DESCENDING)],
    unique=True
)
