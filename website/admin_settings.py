from website.components import *


def create_admin_views():
    views = [
        {
            'title': 'main',
            'query': [slug, title, category, sub_category, order],
            'sort': [(category, 1), (order, 1)]
        },
    ]

    def transform_component(c: Component):
        data = {
            'name': c.name,
            't': 'str'
        }
        if isinstance(c.t, OneOf):
            data['t'] = 'one_of'
            data['values'] = c.t.values
        return data

    for view in views:
        view['query'] = [transform_component(x) for x in view['query']]
        view['sort'] = [(x.name, i) for x, i in view['sort']]

    return views


admin_views = create_admin_views()
