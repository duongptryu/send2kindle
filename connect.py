from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
bot_configuration = BotConfiguration(
	name="Send2Kindle",
	avatar="https://botostore.com/netcat_files/6/7/preview_148877_1587232924.jpg",
	auth_token="4cf23444dd27d24e-4705c501d4209f35-dc9c3007b40de69b"
)
viber = Api(bot_configuration)
viber.set_webhook("https://3ea5bfafb6bb.ngrok.io")
