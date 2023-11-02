from pathlib import Path

DB_NAME = 'web_ecs_template'
WEBSITE_NAME = 'Шаблон'
TELEGRAM_OT_TOKEN = ''
DOMAIN = 'http://127.0.0.1:5000'
CONTENT_FOLDER = Path(__file__).parent.parent / 'content'
CONTENT_FOLDER.mkdir(exist_ok=True)

def get_global_info():
    return {
        'global': {
            'name': WEBSITE_NAME
        }
    }