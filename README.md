# Бот для телеграм для уведомления о выполненых задачах

Данный бот уведомляет об ответах преподавателя, когда работа сдана. В зависимости от ответа приходит сообщения либо о
найденых ошибках, либо о успешном завершении задачи и переходу к новой.

## Как установить локально на компьютере
Доступны 3 переменных окружения:

`DEVMAN_TOKEN` - токен вашего акаунта на ресурсе [dvmn.org](https://dvmn.org/).

`TELEGRAM_TOKEN` - токен от бота на платформе телеграм.

`TG_USER_ID` - id пользователя.
#### Первый способ активации переменных
Переменные окружения необходимо упаковать в файл `.env`. Считывание происходит посредством библиотеки 
[python dotenv](https://pypi.org/project/python-dotenv/).
#### Второй способ активации переменных
Перед запуском скрипта в терминале выполняем команды:
```.env
export DEVMAN_TOKEN=your_token
export TELEGRAM_TOKEN=your_token
export TG_USER_ID=your_tg_id
```
#### Третий способ активации переменных
Использование библиотеки [direnv](https://github.com/direnv/direnv). Установку и активацию 
библиотеки необходимо провести согласно инструкции для своей оболочки. 
В файл `.envrc` который должен находится в папке проекта нужно поместить переменные окружения.
После этого, при входе в папку и запуске скрипта `check_task_bot.py` переменные будут подгружаться автоматически.
***
Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:
```
pip3 install -r requirements.txt
```
Запуск проекта осуществляется из командной строки:
```python
~ python3 check_task_bot.py
```

## Как задеплоить проект на сервис [heroku](https://dashboard.heroku.com/apps)
Необходимо создать новое приложение на сервисе и подключить Github с репозиторием, где находится бот. Переменные 
окружения поместить в [settings](https://dashboard.heroku.com/apps/devman-telegram-bot/settings) `Config var`.
После этого на вкладке ресурсы запустить скрипт `check_task_bot.py`.

## Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).