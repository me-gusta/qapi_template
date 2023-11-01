from functools import lru_cache
from typing import Optional

from website.qapi.component import Component
from website.qapi.database import db


class Entity(dict):
    def __call__(self, component: Component):
        return self[component.name]

    @property
    def id(self):
        return self['_id']

    def update(self, properties=None, **kwargs):
        if properties is None:
            properties = dict(self).copy()
            del properties['_id']
        db.update_one({'_id': self.id}, {'$set': properties})

    def __setitem__(self, key, value):
        if type(key) == Component:
            dict.__setitem__(self, key.name, value)
            return
        dict.__setitem__(self, key, value)


@lru_cache()
def query_many(*components) -> list[Entity]:
    mongo_query = {x.name: {'$exists': True} for x in components}
    projection = {x.name: True for x in components}
    entities = [Entity(x) for x in db.find(mongo_query, projection)]
    return entities


@lru_cache()
def query_one(*components, **kwargs) -> Optional[Entity]:
    mongo_query = {x.name: {'$exists': True} for x in components}
    mongo_query.update(kwargs)
    projection = {x.name: True for x in components}
    result = db.find_one(mongo_query, projection)
    if not result:
        return None
    return Entity(result)


def clear_cache():
    query_one.cache_clear()
    query_many.cache_clear()


def my_query_to_mongodb(data: dict):
    return {x['name']: {'$exists': True} for x in data}
