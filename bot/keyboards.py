from datetime import date, datetime

from aiogram import Bot
from aiogram.types import (
    BotCommand,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


async def set_main_menu(bot: Bot):

    main_menu_commands = [
        BotCommand(command="/start", description="Запуск бота"),
        BotCommand(command="/id", description="Получить свой ID"),
        BotCommand(command="/new", description="Сделать запись"),
        BotCommand(command="/link", description="Моя персональная ссылка"),
        BotCommand(command="/connect", description="Подключить Telegram к сайту"),
        BotCommand(command="/clients", description="Мои ближайшие клиенты"),
        BotCommand(
            command="/date", description="Посмотреть занятое время на выбранную дату"
        ),
        BotCommand(command="/help", description="Все команды"),
        BotCommand(command="/cancel", description="Отменить действие"),
    ]

    await bot.set_my_commands(main_menu_commands)


def create_inline_button(
    selected_times: list[str], booking_id: int, user_id: int, date: str
) -> InlineKeyboardBuilder:
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    for item in selected_times:
        builder.add(
            InlineKeyboardButton(
                text=item[0],
                callback_data=f"cancel:{booking_id}:{user_id}:{date}:{item[0]}",
            )
        )
    builder.adjust(5)
    return builder.as_markup()


def confirmation_markup(
    booking_id: int, user_id: int, date_: str, hour: str, minute: str
) -> InlineKeyboardMarkup:
    markup: InlineKeyboardMarkup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Подтвердить",
                    callback_data=f"confirm_cancel:{booking_id}:{user_id}:{date_}:{hour}:{minute}",
                )
            ],
            [InlineKeyboardButton(text="Отменить", callback_data="action_cancel")],
        ]
    )
    return markup


def create_inline_button_times(
    times: list[str], booking_id: int, user_id: int, date: str
) -> InlineKeyboardBuilder:
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    for item in times:
        builder.add(
            InlineKeyboardButton(
                text=item, callback_data=f"select:{booking_id}:{user_id}:{date}:{item}"
            )
        )
    builder.adjust(5)
    return builder.as_markup()


def create_inline_button_connect_tg(token: str):
    url: str = (
        f"https://scheduler-bgly.onrender.com/user/connect_telegram/?token={token}"
    )
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Привязать", url=url)]]
    )
