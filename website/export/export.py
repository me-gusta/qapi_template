from website.ecw.database import db
from bson import json_util


def main():
    entities = list(db.find())
    with open('entities.json', 'w+', encoding='utf-8') as f:
        f.write(json_util.dumps(entities, ensure_ascii=False))


if __name__ == '__main__':
    main()
