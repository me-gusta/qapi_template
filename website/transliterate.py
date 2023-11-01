import string
from collections import defaultdict

alphabet = {
    'А': 'A',
    'Б': 'B',
    'В': 'V',
    'Г': 'G',
    'Д': 'D',
    'Е': 'E',
    'Ё': 'E',
    'Ж': 'ZH',
    'З': 'Z',
    'И': 'I',
    'Й': 'J',
    'К': 'K',
    'Л': 'L',
    'М': 'M',
    'Н': 'N',
    'О': 'O',
    'П': 'P',
    'Р': 'R',
    'С': 'S',
    'Т': 'T',
    'У': 'U',
    'Ф': 'F',
    'Х': 'H',
    'Ц': 'C',
    'Ч': 'CH',
    'Ш': 'SH',
    'Щ': 'SH',
    'Ъ': "",
    'Ы': 'Y',
    'Ь': "",
    'Э': "E",
    'Ю': "YU",
    'Я': "JA",
    'а': 'a',
    'б': 'b',
    'в': 'v',
    'г': 'g',
    'д': 'd',
    'е': 'e',
    'ё': 'e',
    'ж': 'zh',
    'з': 'z',
    'и': 'i',
    'й': 'j',
    'к': 'k',
    'л': 'l',
    'м': 'm',
    'н': 'n',
    'о': 'o',
    'п': 'p',
    'р': 'r',
    'с': 's',
    'т': 't',
    'у': 'u',
    'ф': 'f',
    'х': 'h',
    'ц': 'c',
    'ч': 'ch',
    'ш': 'sh',
    'щ': 'sh',
    'ъ': "",
    'ы': 'y',
    'ь': "",
    'э': "e",
    'ю': "yu",
    'я': "ja",
    ' ': '-'
}
mapping = defaultdict(str, alphabet)


def translate_one(char: str) -> str:
    translated = mapping[char]
    if translated:
        return translated
    elif char in string.ascii_letters + string.digits:
        return char
    return ''


def make_slug(text: str) -> str:
    return ''.join([translate_one(x) for x in text.lower()])


def test():
    text = 'Это небольшой тест, чтобы проверить правильность работы функции'
    print(text)
    print(make_slug(text))


if __name__ == '__main__':
    test()
