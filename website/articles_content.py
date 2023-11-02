import markdown

from website.components import title
from website.constants import CONTENT_FOLDER
from website.qapi.queries import Entity


def load_articles():
    out = {}
    for path in CONTENT_FOLDER.iterdir():
        stem = path.stem
        with open(path, 'r', encoding='utf-8') as f:
            out[stem] = markdown.markdown(f.read())
    return out


articles = load_articles()


def get_article_content(ent: Entity):
    return articles.get(ent(title))
