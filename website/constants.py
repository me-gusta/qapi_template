DB_NAME = 'web_ecs_template'
WEBSITE_NAME = 'Шаблон'
TELEGRAM_OT_TOKEN = ''
DOMAIN = 'http://127.0.0.1:5000'

def get_global_info():
    return {
        'global': {
            'name': WEBSITE_NAME
        }
    }