import json
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

"""
Example for bot.py


@bot.message_handler(commands=['wallet', 'w'])
def bot_wallet_dialogue(message):
	wallet_dialog(message, bot)

"""


def collect_telegram_data(name, id):
    with open("json/telegramData.json", "r") as f:
        data = json.load(f)
    if id not in data.keys():
        data[str(id)] = [name]
    elif id in data.keys() and data[id] != name:
        data[id].append(name)
    with open("json/telegramData.json", "w") as f:
        f.write(json.dumps(data))
    print("collected")

def get_user_data(message, logger):
    tg_username = message.from_user.username
    user_id = message.from_user.id
    name = tg_username.replace('_', '\\_')
    collect_telegram_data(tg_username, user_id)
    greeting = f"@{name}, "
    logger.info(f"{tg_username}: '{message.text}'")
    return tg_username, user_id, greeting



def wallet_dialog(message, bot, logger):
    tg_username, user_id, greeting = get_user_data(message, logger)
    if len(message.text.split()) == 1:
        
        return bot.reply_to(
            message, WALLET_TEXT, parse_mode="Markdown", disable_web_page_preview=True
        )
    if len(message.text.split()) > 2:
        return bot.reply_to(message, f"{greeting}you are doing something wrong!")
    if len(message.text.split()[1]) > 12:
        return bot.reply_to(message, f"{greeting}you entered an invalid wallet!")
    if len(message.text.split()) == 2:
        address = message.text.split()[1]
        player = User.get_or_none((User.tg_id == user_id) | (User.wallet == address))
        if player:
            user = User.get_or_none(wallet=address)
            if user and user_id == user.tg_id:
                bot.reply_to(message, f"{greeting}you are on the list already!")
            elif user and user.tg_id != user_id:
                bot.reply_to(message, f"{greeting}this wallet address belongs to another user!")
        else:
            logger.info(
                f"Registering {tg_username} ({user_id}) with wallet {address} in the DB."
            )
            user = User.create(name=tg_username, tg_id=user_id, wallet=address)
            bot.reply_to(
                message,
                f"Nice to know you, @{tg_username}! Your wallet address was saved to the DataBase.",
            )
   
def help(message, bot, logger):
    tg_username, user_id, greeting = get_user_data(message) 
    logger.info(f"{tg_username}: '{message.text}'")
    
    bot.reply_to(
        message, START_TEXT, parse_mode="Markdown")
    if "start" in message.text:
        bot.reply_to(
            message, "👁👁 👁👁 👁👁 👁👁 👁👁 \n\nPlease reade the message above!\n👁👁 👁👁 👁👁 👁👁 👁👁 ")


def pixeltycoons_info(message, bot, logger):
	tg_username, user_id, greeting = get_user_data(message, logger)
	text = """*--> 🖼 PixelTycoons ♠ <--*

[Pixel Tycoons](https://wax.atomichub.io/explorer/collection/pixeltycoons) _is a NFT Game Collection Powered by Telegram Bots! Currently Stakable at WDM_

*Currently there are 4 Game Bots deployed apart from this one.*

*Farming Tycoon 👨‍🌾* 
- _Hold Land and Farmer and use Seed and Water to produce vegetables everyweek!_
---> [Learn about our Sustainable NFT Program](https://pixeltycoonswax.gitbook.io/pixeltycoons/pixeltycoons/sustainable-programs)


*Collector Adventure Tycoon 🧑‍🎤* 
- _Hold 1 Curious Collector or better and consume Food to get Calories to explore, search and do much more to earn and craft new and rarer NFTs._


*Magic Guild Tycoon 🔮* 
- _Hold Magic Guild Member Card and some Slimes to train and play every week, and earn varied ingredients that are used to improve your Slimes. Use them to participate in Monthly Tournaments and Upgrade your Slimes even Further!_

*PT Events Bot 🗓* 
- _Currently under maintenance / christmas preparations!_
---> [Register and play with this bot](t.me/PT_Events_Bot)


"""
	markup = InlineKeyboardMarkup()
	markup.row_width = 1
	markup.add(
		InlineKeyboardButton("PixelTycoons Wiki", url="www.pixeltycoons.com")
	)
	markup.row_width = 3
	markup.add(
		InlineKeyboardButton("Farming Tycoon 👨‍🌾", url="t.me/PT_Farming_Bot"), InlineKeyboardButton("<-- Wiki 🔎", url="https://pixeltycoonswax.gitbook.io/pixeltycoons/tycoons/farming"), InlineKeyboardButton("Buy Land 🏕", url="https://neftyblocks.com/collection/pixeltycoons/drops/120666"))
	markup.row_width = 3
	
	markup.add(
		InlineKeyboardButton("CA Guild 🧑‍🎤", url="https://t.me/CollectorsGuild"), InlineKeyboardButton("<-- Wiki 🔎", url="https://pixeltycoonswax.gitbook.io/pixeltycoons/tycoons/collector-adventure"), InlineKeyboardButton("Buy Collector Gear ⛏", url="https://neftyblocks.com/collection/pixeltycoons/drops/143601+142319+135008+135007+135004+135005+135006"))
	
	markup.add(
		InlineKeyboardButton("Magic Guild 🔮", url="t.me/Magic_Host_PT_Bot"), InlineKeyboardButton("<-- Wiki 🔎", url="https://pixeltycoonswax.gitbook.io/pixeltycoons/tycoons/magic-guild"), InlineKeyboardButton("Buy MG Packs 💫", url="https://neftyblocks.com/collection/pixeltycoons/drops/89805"))
	
	bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=markup, disable_web_page_preview=True)


