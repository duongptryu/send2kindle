from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
bot_configuration = BotConfiguration(
	name="Send2Kindle",
	avatar="https://botostore.com/netcat_files/6/7/preview_148877_1587232924.jpg",
	auth_token="4cf75ed4c6e7d113-871283930a94f231-6fb287e6e603dfca"
)
viber = Api(bot_configuration)
viber.set_webhook("https://send2kindle-ncsc.herokuapp.com/")
