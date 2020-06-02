import requests
from dotenv import load_dotenv
import os
import logging
import time
import urllib
from textwrap import dedent
from telegram import Bot
from telegram import ParseMode

logger = logging.getLogger('Bot logger')
logger.setLevel(logging.INFO)


class TelegramLogsHandler(logging.Handler):
    
    def __init__(self, bot, user_id):
        super().__init__()
        self.chat_id = user_id
        self.tg_bot = bot
    
    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def get_response(token, url, timestamp_to_request):
    headers = {
        'Authorization': f'Token {token}'
    }
    payload = {'timestamp': timestamp_to_request}
    response = requests.get(url, headers=headers, params=payload, timeout=90)
    response.raise_for_status()
    return response.json()


def get_timestamp(response):
    if 'last_attempt_timestamp' in response:
        return response['last_attempt_timestamp']
    if 'timestamp_to_request' in response:
        return response['timestamp_to_request']
    return time.time()


def task_message(result, user_id, bot):
    main_url = 'https://dvmn.org/modules/'
    is_negative = result['is_negative']
    lesson_title = result['lesson_title']
    lesson_url = urllib.parse.urljoin(main_url, result['lesson_url'])
    if is_negative:
        mistake_text = dedent(f'''В работе обнаружены ошибки. Преподаватель прислал замечания к исправлению.
        {lesson_url}''')
    else:
        mistake_text = dedent(f'''В работе ошибок не обнаружено! Приступайте к следующей задаче.
        {lesson_url}''')
    
    result_text = dedent(f'''\
        Преподаватель проверил Вашу работу по задаче:
        *{lesson_title}*

        {mistake_text}''')
    bot.send_message(chat_id=user_id, text=result_text, parse_mode=ParseMode.MARKDOWN)


def main():
    load_dotenv()
    
    url_api = 'https://dvmn.org/api/long_polling/'
    devman_token = os.getenv('DEVMAN_TOKEN')
    tgm_user_id = os.getenv('TG_USER_ID')
    telegram_token = os.getenv('TELEGRAM_TOKEN')
    bot = Bot(telegram_token)
    
    logger.addHandler(TelegramLogsHandler(bot, tgm_user_id))
    logger.info('Бот начал работу')
    timestamp_to_request = time.time()
    while True:
        try:
            response = get_response(devman_token, url_api, timestamp_to_request)
            if response['status'] == 'found':
                result = response['new_attempts'][0]
                task_message(result, tgm_user_id, bot)
            timestamp_to_request = get_timestamp(response)
        except requests.exceptions.ReadTimeout:
            continue
        except requests.exceptions.ConnectionError:
            logger.exception('Бот упал с ошибкой')
            time.sleep(1800)
            continue
        except Exception:
            logger.exception('Бот упал с ошибкой')


if __name__ == '__main__':
    main()
