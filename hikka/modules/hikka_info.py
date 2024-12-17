# ©️ Dan Gazizullin, 2021-2023
# This file is a part of Hikka Userbot
# 🌐 https://github.com/hikariatama/Hikka
# You can redistribute it and/or modify it under the terms of the GNU AGPLv3
# 🔑 https://www.gnu.org/licenses/agpl-3.0.html

import git
import time
import random
from hikkatl.tl.types import Message
from hikkatl.utils import get_display_name

from .. import loader, utils, version
from ..inline.types import InlineQuery


@loader.tds
class HikkaInfoMod(loader.Module):
    """Show userbot info"""

    strings = {"name": "HikkaInfo"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "custom_message",
                doc=lambda: self.strings("_cfg_cst_msg"),
            ),
            loader.ConfigValue(
                "custom_button",
                ["🌘 Support chat", "https://t.me/heroku_talks"],
                lambda: self.strings("_cfg_cst_btn"),
                validator=loader.validators.Union(
                    loader.validators.Series(fixed_len=2),
                    loader.validators.NoneType(),
                ),
            ),
            loader.ConfigValue(
                "banner_url",
                "https://imgur.com/a/aMB7J0S.png",
                lambda: self.strings("_cfg_banner"),
                validator=loader.validators.Link(),
            ),
        )

    def _measure_ping(self) -> float:
        """Measure the ping time."""
        start_time = time.perf_counter()
        # Perform a simple operation to measure time
        _ = utils.get_cpu_usage()  # You can replace this with a more relevant operation
        return round((time.perf_counter() - start_time) * 1000, 2)  # Convert to ms

    def _render_info(self, inline: bool, message: Message) -> str:
    try:
        repo = git.Repo(search_parent_directories=True)
        diff = repo.git.log([f"HEAD..origin/{version.branch}", "--oneline"])
        upd = (
            self.strings("update_required") if diff else self.strings("up-to-date")
        )
    except Exception:
        upd = ""

    me = '<b><a href="tg://user?id={}">{}</a></b>'.format(
        self._client.hikka_me.id,
        utils.escape_html(get_display_name(self._client.hikka_me)),
    )
    build = utils.get_commit_url()
    _version = f'<i>{".".join(list(map(str, list(version.__version__))))}</i>'
    prefix = f"«<code>{utils.escape_html(self.get_prefix())}</code>»"
    platform = utils.get_named_platform()
    ping = self._measure_ping()  # Get the ping value

    # Replace emojis as before
    for emoji, icon in [
        ("🍊", "<emoji document_id=5449599833973203438>🧡</emoji>"),
        # Add other emojis here...
    ]:
        platform = platform.replace(emoji, icon)

    if self.config["custom_message"]:
        return self.config["custom_message"].format(
            messagep=message,
            me=me,
            version=_version,
            build=build,
            prefix=prefix,
            platform=platform,
            upd=upd,
            uptime=utils.formatted_uptime(),
            cpu_usage=utils.get_cpu_usage(),
            ram_usage=f"{utils.get_ram_usage()} MB",
            branch=version.branch,
            ping=ping,  # Include ping in the format
        )
    else:
        return (
            f'<b>{{}}</b>\n\n<b>{{}} {self.strings("owner")}:</b> {me}\n\n<b>{{}}'
            f' {self.strings("version")}:</b> {_version} {build}\n<b>{{}}'
            f' {self.strings("branch")}:'
            f"</b> <code>{version.branch}</code>\n{upd}\n\n<b>{{}}"
            f' {self.strings("prefix")}:</b> {prefix}\n<b>{{}}'
            f' {self.strings("uptime")}:'
            f"</b> {utils.formatted_uptime()}\n\n<b>{{}}"
            f' {self.strings("cpu_usage")}:'
            f"</b> <i>~{utils.get_cpu_usage()} %</i>\n<b>{{}}"
            f' {self.strings("ram_usage")}:'
            f"</b> <i>~{utils.get_ram_usage()} MB</i>\n<b>{{}} {self.strings('ping')}:</b> <i>{ping} ms</i>\n<b>{{}}</b>"
        ).format(
            *map(
                lambda x: utils.remove_html(x) if inline else x,
                (
                    (
                        utils.get_platform_emoji()
                        if self._client.hikka_me.premium and not inline
                        else "🌘 Hikka"
                    ),
                    "<emoji document_id=5373141891321699086>😎</emoji>",
                    "<emoji document_id=5469741319330996757>💫</emoji>",
                    "<emoji document_id=5449918202718985124>🌳</emoji>",
                    platform,
                ),
            )
        )

        

    def _get_mark(self):
        return (
            {
                "text": self.config["custom_button"][0],
                "url": self.config["custom_button"][1],
            }
            if self.config["custom_button"]
            else None
        )

    @loader.inline_handler(
        thumb_url="https://img.icons8.com/external-others-inmotus-design/344/external-Moon-round-icons-others-inmotus-design-2.png"
    )
    @loader.inline_everyone
    async def info(self, _: InlineQuery) -> dict:
        """Send userbot info"""

        return {
            "title": self.strings("send_info"),
            "description": self.strings("description"),
            **(
                {"photo": self.config["banner_url"], "caption": self._render_info(True)}
                if self.config["banner_url"]
                else {"message": self._render_info(True)}
            ),
            "thumb": (
                "https://github.com/hikariatama/Hikka/raw/master/assets/hikka_pfp.png"
            ),
            "reply_markup": self._get_mark(),
        }

    @loader.command()
    async def infocmd(self, message: Message):
        if self.config["custom_button"]:
            await self.inline.form(
                message=message,
                text=self._render_info(True, message),
                reply_markup=self._get_mark(),
                **(
                    {"photo": self.config["banner_url"]}
                    if self.config["banner_url"]
                    else {}
                ),
            )
        else:
            await utils.answer_file(
                message,
                self.config["banner_url"],
                self._render_info(False),
            )

    @loader.command()
    async def hikkainfo(self, message: Message):
        await utils.answer(message, self.strings("desc"))

    @loader.command()
    async def setinfo(self, message: Message):
        if not (args := utils.get_args_html(message)):
            return await utils.answer(message, self.strings("setinfo_no_args"))

        self.config["custom_message"] = args
        await utils.answer(message, self.strings("setinfo_success"))
