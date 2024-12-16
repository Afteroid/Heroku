from asyncio import sleep
from .. import loader, utils
import asyncio
from telethon.tl.types import Message, ChatAdminRights
from telethon import functions, TelegramClient, errors
from ..inline.types import InlineCall
import inspect
import re
import logging

@loader.tds
class SHelp(loader.Module):
    """Основные команды Хикки"""
    strings = {
        "name": "SHelp",
    }
    @loader.command()
    async def shhelp(self, message):
        """Гайд по Хикке"""
        await self.inline.form(
            text=f"<b>🌘 Основные команды Хикки:</b>\n\n<i>.cfg - Настройка модулей хикки как и системных так и установленных\n.lm - Непосредственно сам установщик модулей, используется в ответ к файлу с расширением .py, также нужно соблюдать осторонжность с установками ведь некоторые модули могут удалить ваш аккаунт\n.ulm - Удаление модуля. Пример использования: .ulm test, где test - название удаляемого модуля\n.info - Показывает информацию хикки, потребление ОЗУ, нагрузка и т.п.\n.help - Показывает полный список модулей\n.ml - Позволяет поделиться устаеовленным модулем. Пример использования: .ml test, где test - название установленного модуля</i>",
            message=message,
            reply_markup=[
                [
                    {
                        'text' : '🔸 Далее',
                        'callback' : self.zam1,
                    },
                    {
                        'text' : '🔻 Закрыть',
                        'action' : 'close'
                    }
                ]
            ]
        )
    async def zam1(self, call:InlineCall):
        await call.edit(
            text=f"🌘 <b>Каналы с модулями:</b>\n@hikarimods\n@morisummermods\n@nalinormods\n@AstroModules\n@vsecoder_m\n@mm_mods\n@apodiktum_modules\n@shadow_modules\n@DorotoroMods\n@HikkaFTGmods\n@nercymods\n@sqlmerr_m\n@AuroraModules\n@famods\n@codrago_m",
            reply_markup=[
                [
                    {
                        'text' : '🔸 Назад',
                        'callback' : self.zam2,
                    },
                    {
                        'text' : '🔸 Далее',
                        'callback' : self.zam3,
                    },
                ],
                [
                    {
                        'text' : '🔻 Закрыть',
                        'action' : 'close'
                    }
                ]
            ]
        )
    async def zam2(self, call:InlineCall):
        await call.edit(
            text=f"<b>🌘 Основные команды Хикки:</b>\n\n<i>.cfg - Настройка модулей хикки как и системных так и установленных\n.lm - Непосредственно сам установщик модулей, используется в ответ к файлу с расширением .py, также нужно соблюдать осторонжность с установками ведь некоторые модули могут удалить ваш аккаунт\n.ulm - Удаление модуля. Пример использования: .ulm test, где test - название удаляемого модуля\n.info - Показывает информацию хикки, потребление ОЗУ, нагрузка и т.п.\n.help - Показывает полный список модулей\n.ml - Позволяет поделиться устаеовленным модулем. Пример использования: .ml test, где test - название установленного модуля</i>",
            reply_markup=[
                [
                    {
                        'text' : '🔸 Далее',
                        'callback' : self.zam1,
                    },
                    {
                        'text' : '🔻 Закрыть',
                        'action' : 'close'
                    }
                ]
            ]
        )
    async def zam3(self, call:InlineCall):
        await call.edit(
            text=f"🌘 <b>Полезные ссылки:</b>\nОфициальный саппорт чат t.me/hikka_talks",
            reply_markup=[
                [
                    {
                        'text' : '🔸 Назад',
                        'callback' : self.zam1,
                    },
                    {
                        'text' : '🔻 Закрыть',
                        'action' : 'close'
                    }
                ]
            ]
        )
        