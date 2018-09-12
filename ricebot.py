import json
import time
import os
import sys
import telepot
import telepot.text
import random

from telepot.loop import MessageLoop


ricebot = telepot.Bot(os.environ["BOT_TOKEN"])
wwgc = os.environ["WW_GC"]
riceID = ricebot.getMe()
ricecontent = 0
all_content_types = ["text", "audio", "document", "game", "photo", "sticker", "video", "voice", "video_note","contact", "location", "venue", "new_chat_member", "left_chat_member", "new_chat_title","new_chat_photo",  "delete_chat_photo", "group_chat_created", "supergroup_chat_created","channel_chat_created", "migrate_to_chat_id", "migrate_from_chat_id", "pinned_message","new_chat_members", "invoice", "successful_payment"]
sadgreet = ["spill", "trip", "eat", "bite", "tips", "tips over"]
killgreet = ["unplug", "bang", "kill", "rip"]
randomgreet = ["Hello", "Hi", "Greetings", "Good day", "How are ya?", "Yes", "No", "What's up?"]
assumptgreet = ["akala ko si rice", "akala ko si ricecooker", "akala ko si @ricecooker", "kala ko si rice", "kala ko si @ricecooker", "kala ko si ricecooker"]
werewolfcommands = ["/werewolf@riceCookerisnotAbot", "/startchaos@werewolfbot", "/nextgame@werewolfbot", "/start@werewolfbot",]
unpluggif = "CgADBQADNwADtjzaDXzFsIuaINkHAg"
landigif = ["CgADBQADHQAD6QuQV_mxPdwxj0s2Ag", "CgADBQADKQADvG2JVi4mEJDnylDvAg"]
landichance = 0


#get content type
def _find_first_key(d, keys):
    for k in keys:
        if k in d:
            return k
    raise KeyError("No suggested keys %s in %s" % (str(keys), str(d)))

def handle(msg):
	#content_type, chat_type, chat_id = telepot.glance(msg, flavor="chat", long="False")
	content_type = _find_first_key(msg, all_content_types)
	msg_id = msg["message_id"]
	chat_id = msg["chat"]["id"]

	if content_type == "text":
		msg_text = msg["text"].lower()
		#gc specific autoreply

		#check if GC is for testing
		if chat_id == -234762812:
			print("chat id is " + msg["chat"]["title"])
			if (("reply_to_message" in msg) and (msg_text == "landi mo") and (msg["from"]["id"] == msg["reply_to_message"]["from"]["id"])):
				print("same user ID")
		#check if GC is production
		elif (chat_id == -1001043875036):
			#give 20% chance for Jerome landigif, 80% chance for generic landigif
			landichance = random.randint(1,5) % 5
			#autoreply for hipo messages
			if (msg_text == "hipo"):
				if (landichance == 0):
					ricebot.sendDocument(chat_id, landigif[1], caption=None, parse_mode="Markdown", disable_notification=True, reply_to_message_id=msg_id)
				else:
					ricebot.sendDocument(chat_id, landigif[0], caption=None, parse_mode="Markdown", disable_notification=True, reply_to_message_id=msg_id)
			#autoreply for landi mo reply
			elif (("reply_to_message" in msg) and (msg_text == "landi mo") and (msg["from"]["id"] != msg["reply_to_message"]["from"]["id"])):
				if (landichance == 0):
					ricebot.sendDocument(chat_id, landigif[1], caption=None, parse_mode="Markdown", disable_notification=True, reply_to_message_id=msg["reply_to_message"]["message_id"])
				else:
					ricebot.sendDocument(chat_id, landigif[0], caption=None, parse_mode="Markdown", disable_notification=True, reply_to_message_id=msg["reply_to_message"]["message_id"])
			#werewolf command invite autoreply
			elif (any(x in msg["text"] for x in werewolfcommands)):
				ricebot.sendMessage(chat_id, "Hi, you may join this GC's werewolf game channel at https://t.me/joinchat/" + wwgc, parse_mode="Markdown", disable_web_page_preview=None, disable_notification=True, reply_to_message_id=msg_id)
			#assumptions autoreply
			elif (any(x in msg_text for x in assumptgreet)):
				time.sleep(1)			
				ricebot.sendMessage(chat_id, "Di ako yun", parse_mode="Markdown", disable_web_page_preview=None, disable_notification=True, reply_to_message_id=msg_id)
	
		
		#non-gc specific autoreply
		#send greetings
		if (msg_text == "hi" or msg_text == "hi rice"):
			time.sleep(1)
			ricebot.sendMessage(chat_id, random.choice(randomgreet), parse_mode="Markdown", disable_web_page_preview=None, disable_notification=True, reply_to_message_id=msg_id)
		#sad greetings autoreply
		elif (any(x in msg_text for x in sadgreet) and "ricecooker" in msg_text):
			ricebot.sendMessage(chat_id,"<.<", parse_mode="Markdown", disable_web_page_preview=None, disable_notification=True, reply_to_message_id=msg_id)
			time.sleep(1)
			ricebot.sendMessage(chat_id, ">.>", parse_mode="Markdown")
			ricebot.sendMessage(chat_id, "_spills rice_", parse_mode="Markdown")
		#send unplug GIF if a kill greeting has been sent 
		elif (any(x in msg_text for x in killgreet) and "ricecooker" in msg_text): 
			ricebot.sendDocument(chat_id, unpluggif)		
		
		


MessageLoop(ricebot, handle).run_as_thread()

while 1:
	time.sleep(10)


#Credits to Nick Lee for the telepot python framework for Telegram bot API