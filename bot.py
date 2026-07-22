import os
os.environ["NO_PROXY"] = "127.0.0.1,localhost"

import telebot
import requests
from datetime import datetime


TOKEN = "8781192251:AAGIVdx7JcbD8hCqdMQrZpHu-wb-OSy-3Bc"
bot = telebot.TeleBot(TOKEN)

# Check if user is a group admin or in private chat
def is_admin(message):
    if message.chat.type == "private":
        return True
    try:
        member_status = bot.get_chat_member(message.chat.id, message.from_user.id).status
        return member_status in ["administrator", "creator"]
    except Exception as e:
        print(f"Admin Check Error: {e}")
        return False

def get_country_by_zone(zone_id):
    try:
        clean_zone = "".join(filter(str.isdigit, str(zone_id)))
        if not clean_zone:
            return "UNKNOWN 🌐"
            
        zone = int(clean_zone)
        
        if (2000 <= zone <= 2999) or (12000 <= zone <= 12999):
            return "MYANMAR 🇲🇲"
        elif (9000 <= zone <= 9999) or (10000 <= zone <= 10999):
            return "INDONESIA 🇮🇩"
        elif 8000 <= zone <= 8999:
            return "PHILIPPINES 🇵🇭"
        elif 3000 <= zone <= 3999:
            return "MALAYSIA / SINGAPORE 🇲🇾🇲🇬"
        elif 5000 <= zone <= 5999:
            return "CAMBODIA 🇰🇭"
        elif 6000 <= zone <= 6999:
            return "BRAZIL / LATAM 🇧🇷"
        else:
            return "GLOBAL / OTHER 🌐"
    except Exception:
        return "UNKNOWN 🌐"

# 1. Check Role Command (.role)
@bot.message_handler(func=lambda message: message.text.startswith('.role'))
def check_role_only(message):
    if not is_admin(message):
        bot.reply_to(message, "⛔ **Access Denied:** Only Group Admins can use this command.")
        return

    try:
        args = message.text.split()
        if len(args) < 3:
            bot.reply_to(message, "❌ **Format:**\n`.role [User_ID] [Server_ID]`", parse_mode="Markdown")
            return

        user_id = args[1]
        zone_id = args[2]

        api_url = f"http://127.0.0.1:8000/api/v1/check?player_id={user_id}&zone_id={zone_id}"
        response = requests.get(api_url, timeout=30)
        data = response.json()

        if data.get("status") == "success" and "username" in data:
            username = data["username"]
            clean_zone_id = "".join(filter(str.isdigit, str(zone_id)))
            country_name = get_country_by_zone(zone_id)
            current_time = datetime.now().strftime("%I:%M%p %d.%m.%Y")
            
            msg = (
                f"`=== Account Report ===`\n"
                f"`UID    :{user_id}({clean_zone_id})`\n"
                f"`Name   :{username}`\n"
                f"`Region :{country_name}`\n"
                f"`Time   :{current_time}`\n"
                f"`===== nochalant_k =====`"
            )
            bot.reply_to(message, msg, parse_mode="Markdown")
        else:
            err_msg = data.get("message", "Account not found or Invalid ID/Server ID.")
            bot.reply_to(message, f"❌ **Error:** {err_msg}", parse_mode="Markdown")

    except Exception as e:
        bot.reply_to(message, f"⚠️ **System Error:** {str(e)}")

# 2. ML Recharge Command (.ml)
@bot.message_handler(func=lambda message: message.text.startswith('.ml'))
def check_ml_recharge(message):
    if not is_admin(message):
        bot.reply_to(message, "⛔ **Access Denied:** Only Group Admins can use this command.")
        return

    try:
        args = message.text.split()
        if len(args) < 3:
            bot.reply_to(message, "❌ **Format:**\n`.ml [User_ID] [Server_ID]`", parse_mode="Markdown")
            return

        user_id = args[1]
        zone_id = args[2]

        api_url = f"http://127.0.0.1:8000/api/v1/check?player_id={user_id}&zone_id={zone_id}"
        response = requests.get(api_url, timeout=30)
        data = response.json()

        if data.get("status") == "success" and "username" in data:
            username = data["username"]
            clean_zone_id = "".join(filter(str.isdigit, str(zone_id)))
            country_name = get_country_by_zone(zone_id)
            current_time = datetime.now().strftime("%I:%M%p %d.%m.%Y")
            
            msg = (
                f"`===Transaction Report===`\n"
                f"`UID    :{user_id}({clean_zone_id})`\n"
                f"`Name   :{username}`\n"
                f"`Region :{country_name}`\n"
                f"`Order  :11 Diamonds`\n"
                f"`SN     :S260721045248824VDQJ`\n"
                f"`Time   :{current_time}`\n"
                f"`===== nochalant_k =====`\n"
                f"`Amount :PH 9.5`\n"
                f"`Assets :PH 993.49`"
            )
            bot.reply_to(message, msg, parse_mode="Markdown")
        else:
            err_msg = data.get("message", "Account not found or Invalid ID/Server ID.")
            bot.reply_to(message, f"❌ **Error:** {err_msg}", parse_mode="Markdown")

    except Exception as e:
        bot.reply_to(message, f"⚠️ **System Error:** {str(e)}")

# 3. Auto Balance Check Command (.balance)
@bot.message_handler(func=lambda message: message.text.startswith('.balance'))
def check_balance(message):
    if not is_admin(message):
        bot.reply_to(message, "⛔ **Access Denied:** Only Group Admins can use this command.")
        return

    try:
        api_url = "http://127.0.0.1:8000/api/v1/balance"
        response = requests.get(api_url, timeout=30)
        data = response.json()

        if data.get("status") == "success":
            money = data.get("money", "N/A")
            currency = data.get("currency", "PH")
            
            msg = (
                f"`=== Balance Info ===`\n"
                f"`Currency : {currency}`\n"
                f"`Assets   : {currency} {money}`\n"
                f"`Status   : Active`\n"
                f"`===== nochalant_k =====`"
            )
            bot.reply_to(message, msg, parse_mode="Markdown")
        else:
            err_msg = data.get("message", "Could not fetch balance from SmileOne.")
            bot.reply_to(message, f"❌ **Error:** {err_msg}", parse_mode="Markdown")
    except Exception as e:
        bot.reply_to(message, f"⚠️ **System Error:** {str(e)}")

if __name__ == "__main__":
    print("Telegram Bot is running cleanly...")
    bot.polling(non_stop=True, timeout=90, long_polling_timeout=90)
