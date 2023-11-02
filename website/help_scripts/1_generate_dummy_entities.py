from random import choice, randint

import lorem

from website.bits import bits_category, bits_sub_category
from website.constants import CONTENT_FOLDER
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


def translate_to_rulorem(text):
    sentences = []
    for sentence in text.split('. '):
        words = []
        for word in sentence.split(' '):
            word_ru = gen_name(len(word), False)
            words.append(word_ru)
        sentences.append(' '.join(words).capitalize())

    return '. '.join(sentences) + '.'


def gen_md_text():
    def random_mark():
        return choice(['.', '!', '?'])

    sentences = translate_to_rulorem(lorem.text()).split('. ')
    sentences[-1] = sentences[-1][:-1]  # remove a dot at the end

    heading1 = '## ' + sentences[0] + random_mark()
    heading2 = '## ' + sentences[1] + random_mark()
    sentences = sentences[2::]

    p1 = '. '.join(sentences[:len(sentences) // 2]) + '.'
    p2 = '. '.join(sentences[len(sentences) // 2:]) + '.'
    return f'{heading1}\n\n' \
           f'{p1}\n\n' \
           f'{heading2}\n\n' \
           f'{p2}'


def main():
    db.delete_many({})
    for path in CONTENT_FOLDER.iterdir():
        path.unlink()

    c_order = 1
    template = {
        "slug": "",
        "title": "",
        "description": "",
        "category": "",
        "sub_category": "",
        "order": c_order,
    }

    for i in range(100):
        ent = template.copy()
        name = gen_name()
        ent['title'] = name
        ent['slug'] = make_slug(ent['title'])
        ent['description'] = translate_to_rulorem(lorem.paragraph())

        ent['category'] = choice(bits_category)
        ent['sub_category'] = choice(bits_sub_category)

        if i == 0:
            ent['path'] = '/'
            ent['template'] = 'index'
        db.insert_one(ent)
        c_order += 1

        content = gen_md_text()
        with open(CONTENT_FOLDER / f'{name}.md', 'w+', encoding='utf-8') as f:
            f.write(content)


main()
