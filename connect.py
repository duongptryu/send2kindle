from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
import config

bot_configuration = BotConfiguration(
	name=config.BOT_NAME,
	avatar=config.AVATAR,
	auth_token=config.TOKEN
)
viber = Api(bot_configuration)
viber.set_webhook("https://22837baafeb9.ngrok.io")
