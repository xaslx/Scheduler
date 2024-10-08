# Scheduler (FastAPI + Aiogram3)


## Описание проекта

**Scheduler** — это веб-приложение, созданное для управления записями и клиентами. 
Ваши клиенты могут легко и быстро записаться на удобное для них время.

Имеется пользовательский интерфейс, можно протестировать - https://scheduler-bgly.onrender.com/

https://t.me/scheduler_help_bot - Телеграм Бот

(так как задеплоен на render.com , при открытии ссылки нужно подождать около минуты)

### Основной функционал:

- **Регистрация и авторизация**: Использовал JWT токен
- **Возможность восстановить пароль на случай если забыли**
- **Профиль пользователя**:
  - Получение уникальной ссылки для записи клиентов.
  - Редактирование информации о себе, изменение пароля, удаление профиля.
  - Настройки профиля: управление доступностью для записи, настройка рабочего времени и интервала.
  - Просмотр списка клиентов и возможность отменить запись.
- **Роли пользователей**:
  - **user**: Обычный пользователь с доступом к основному функционалу.
  - **admin**: Может блокировать пользователей, просматривать весь список пользователей, создавать уведомления и рассылать их по email.
  - **dev**: Имеет все права администратора, а также может удалять профили и изменять роли пользователей.
- **Уведомления**: Email-уведомления при регистрации, (записи на прием, отмене записи **отправляется как клиентам так и пользователю**), изменении пароля.
  Для фоновых задач использовал два варианта Celery и BackgroundTask из FastAPI
- **Обратная связь**: Пользователи могут отправлять сообщения через форму обратной связи.

## Стек

- FastAPI
- SQLAlchemy + PostgreSQL
- Redis
- Celery
- Grafana + Prometheus
- Docker
- Sentry
- Alembic
- Black, isort, flake8, autoflake
- HTML, CSS, JS
- Aiogram3
