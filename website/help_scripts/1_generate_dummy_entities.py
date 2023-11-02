from random import choice, randint

import lorem

from website.bits import bits_category, bits_sub_category
from website.qapi.database import db
from website.transliterate import make_slug


def gen_name(length_name=randint(5, 10), capitalize=True):
    init = randint(0, 1)

    def gen_letter(i: int):
        if i % 2 == init:
            return choice('аеиоуыя')
        else:
            return choice('мнтлднжвцм')

    name = [gen_letter(x) for x in range(length_name)]
    if name[0] == 'ы':
        name[0] = 'и'
    for i in range(len(name) - 1):
        if name[i] == 'ц' and name[i + 1] == 'я':
            name[i + 1] = 'а'
        if name[i] == 'ж' and name[i + 1] == 'ы':
            name[i + 1] = 'и'
    name = ''.join(name)
    if capitalize:
        return name.capitalize()
    else:
        return name


def gen_paragraph():
    sentences = []
    for sentence in lorem.paragraph().split('. '):
        words = []
        for word in sentence.split(' '):
            word_ru = gen_name(len(word), False)
            words.append(word_ru)
        sentences.append(' '.join(words).capitalize())

    return '. '.join(sentences)


def main():
    db.delete_many({})
    c_order = 1
    template = {
        "slug": "",
        "title": "",
        "description": "",
        "category": choice(bits_category),
        "sub_category": choice(bits_sub_category),
        "order": c_order,
    }

    for i in range(100):
        ent = template.copy()
        ent['title'] = gen_name()
        ent['slug'] = make_slug(ent['title'])
        ent['description'] = gen_paragraph()
        if i == 0:
            ent['path'] = '/'
            ent['template'] = 'index'
        db.insert_one(ent)
        c_order += 1


main()
