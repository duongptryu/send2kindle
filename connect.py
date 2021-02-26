from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration

bot_configuration = BotConfiguration(
	name='PythonSampleBot',
	avatar='http://viber.com/avatar.jpg',
	auth_token='4cf24aa8c427dec0-fdf401a1da0b2abb-c74184dd9ac8b1c'
)
viber = Api(bot_configuration)
viber.set_webhook("https://d95ca7afc867.ngrok.io")


