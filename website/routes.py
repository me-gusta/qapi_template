import re
from pathlib import Path
from random import shuffle

import requests as requests
from flask import render_template, make_response, url_for, request, jsonify

from server import app
from website.articles_content import get_article_content
from website.components import *
from website.constants import *

from website.qapi.queries import query_many, query_one, Entity


def build_menu():
    menu = {}

    for ent in query_many(title, category, sub_category, slug, order):
        if not ent(category):
            continue

        try:
            sub_menu = menu[ent(category)]
        except KeyError:
            sub_menu = menu[ent(category)] = {}

        try:
            items = sub_menu[ent(sub_category)]
        except KeyError:
            items = sub_menu[ent(sub_category)] = []
        items.append(ent)
    return menu


def build_general_context():
    articles = query_many(slug, title, description)
    shuffle(articles)
    return {
               'menu': build_menu(),
               'articles': articles
           } | get_global_info()


def build_article_context(slug_str: str):
    article = query_one(
        title,
        slug=slug_str
    )

    # blocks = query_one(
    #     block_reba,
    #     block_brown,
    #     block_faq,
    #     block_reviews,
    #     block_form,
    #     block_prices,
    #     slug=slug_str
    # )
    print()
    return {
        'content': get_article_content(article),
        'article': article,
        # 'blocks': blocks,
    }


special_context = {
    'about-us': {
    },
}


def build_context(ent_slug):
    context_general = build_general_context()
    context_article = build_article_context(ent_slug)

    context_special = special_context.get(ent_slug)

    return context_general | context_article | (context_special or {})


def create_routes():
    with_path = query_many(slug, path, template)
    for entity in with_path:
        def route(ent: Entity):
            def a():
                context = build_context(ent(slug))
                # print(context.keys())
                template_name = ent(template) + '.html'
                return render_template('pages/' + template_name, **context)

            return a

        try:
            app.add_url_rule(entity(path), entity(slug), route(entity))
        except ValueError:
            print('ERROR MAKING URL for', entity)


create_routes()


@app.route("/article/<slug>/")
def article_view(slug: str):
    with_path = query_one(
        path,
        slug=slug
    )

    if with_path:
        return make_response('Страница не найдена', 404)

    context = build_context(slug)

    return render_template('pages/article.html', **context)


def send_email(text: str):
    api = 'https://api.telegram.org/bot{token}/sendMessage'.format(token=TELEGRAM_OT_TOKEN)
    requests.post(
        url=api,
        data={'chat_id': 6843061580, 'text': text, 'parse_mode': 'html'}
    ).json()


@app.route("/callback", methods=['POST'])
def callback_view():
    try:
        data = request.json
        name = data.get('name') or 'Анонимный пользователь'
        phone = data['phone']
        message = data.get('message')
        if not (name or phone):
            raise ValueError('Нет имени или телефона')
        text = f'<b>Сообщение с сайта "{WEBSITE_NAME}"</b>\n\n' \
               f'<u>Имя</u>: {name}\n' \
               f'<u>Телефон</u>: <pre>{phone}</pre>'
        if message:
            text += f'\n<u>Сообщение</u>: {message}'
        text += '\n\n\n<em>Скопировать телефон можно долгим нажатием на него</em>'
        send_email(text)
        # send E_MAIL
        return jsonify({'status': 'ok'})
    except Exception as e:
        print('Error while sending email', type(e), e.args)
        return jsonify({'status': 'error'})


@app.route('/robots.txt')
def view_robots():
    text = f'User-agent: *\n' \
           f'Host: {DOMAIN}\n' \
           f'Sitemap: {DOMAIN}/sitemap.xml\n\n' \
           f'Disallow: /qapi/admin\n' \
           f'Disallow: /callback/\n\n' \
           f'Clean-param: utm_referer&utm_ya_campaign&yabizcmpgn&utm_candidate'
    response = make_response(text, 200)
    response.mimetype = 'text/plain'
    return response


@app.route("/sitemap.xml")
def sitemap_view():
    def gen_xml_entry(link: str):
        if link:
            return f'<url>\n' \
                   f'  <loc>{DOMAIN}/{link}/</loc>\n' \
                   f'</url>'
        else:
            return f'<url>\n' \
                   f'  <loc>{DOMAIN}/</loc>\n' \
                   f'</url>'

    articles_all = query_many(slug)
    dict_with_path = {x(slug): x(path) for x in query_many(slug, path)}

    entries = []

    for slg, pth in dict_with_path.items():
        pth = pth.replace('/', '')
        entries.append(gen_xml_entry(pth))

    for e in query_many(slug):
        p = dict_with_path.get(e(slug))
        if p:
            continue
        link = f'article/{e(slug)}'
        entries.append(gen_xml_entry(link))

    urlset = '\n'.join(entries)
    template_xml = app.jinja_env.get_or_select_template('rss/item.html')
    response = make_response(template_xml.render({'urlset': urlset}), 200)

    response.mimetype = "application/xml"
    return response
