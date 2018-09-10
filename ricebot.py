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
sadgreet = ["spill", "trip", "eat", "bite", "tips", "tips over"]
killgreet = ["unplug", "bang", "kill", "rip"]
randomgreet = ["Hello", "Hi", "Greetings", "Good day", "How are ya?", "Yes", "No", "What's up?"]
assumptgreet = ["akala ko si rice", "akala ko si ricecooker", "akala ko si @ricecooker", "kala ko si rice", "kala ko si @ricecooker", "kala ko si ricecooker"]
werewolfcommands = ["/werewolf@riceCookerisnotAbot", "/startchaos@werewolfbot", "/nextgame@werewolfbot", "/start@werewolfbot",]
unpluggif = "CgADBQADNwADtjzaDXzFsIuaINkHAg"
landigif = ["CgADBQADHQAD6QuQV_mxPdwxj0s2Ag", "CgADBQADKQADvG2JVi4mEJDnylDvAg"]
landichance = 0

def handle(msg):
	content_type, chat_type, chat_id, msg_date, msg_id = telepot.glance(msg, flavor="chat", long="True")


	if content_type == "text":
		#gc specific autoreply

		if chat_id == -234762812:
			print("chat id is " + msg["chat"]["title"])

		elif (chat_id == -1001043875036):
			#give 25% chance for Jerome landigif, 75% chance for generic landigif
			landichance = random.randint(1,4) % 4
			#werewolf command invite autoreply
			if (any(x in msg["text"] for x in werewolfcommands)):
				ricebot.sendMessage(chat_id, "Hi, you may join this GC's werewolf game channel at https://t.me/joinchat/" + wwgc, parse_mode="Markdown", disable_web_page_preview=None, disable_notification=True, reply_to_message_id=msg_id)
			#assumptions autoreply
			elif (any(x in msg["text"].lower() for x in assumptgreet)):
				time.sleep(1)			
				ricebot.sendMessage(chat_id, "Di ako yun", parse_mode="Markdown", disable_web_page_preview=None, disable_notification=True, reply_to_message_id=msg_id)
			#autoreply for hipo messages
			elif (msg["text"].lower() == "hipo"):
				if (landichance == 0):
					ricebot.sendDocument(chat_id, landigif[1], caption=None, parse_mode="Markdown", disable_notification=True, reply_to_message_id=msg_id)
				else:
					ricebot.sendDocument(chat_id, landigif[0], caption=None, parse_mode="Markdown", disable_notification=True, reply_to_message_id=msg_id)
			#autoreply for landi mo reply
			elif (("reply_to_message" in msg) and (msg["text"].lower() == "landi mo")):
				if (landichance == 0):
					ricebot.sendDocument(chat_id, landigif[1], caption=None, parse_mode="Markdown", disable_notification=True, reply_to_message_id=msg["reply_to_message"]["message_id"])
				else:
					ricebot.sendDocument(chat_id, landigif[0], caption=None, parse_mode="Markdown", disable_notification=True, reply_to_message_id=msg["reply_to_message"]["message_id"])
			
			

		
		#non-gc specific autoreply
		#sad greetings autoreply
		if (any(x in msg["text"].lower() for x in sadgreet) and "ricecooker" in msg["text"].lower()):
			ricebot.sendMessage(chat_id,"<.<", parse_mode="Markdown", disable_web_page_preview=None, disable_notification=True, reply_to_message_id=msg_id)
			time.sleep(1)
			ricebot.sendMessage(chat_id, ">.>", parse_mode="Markdown")
			ricebot.sendMessage(chat_id, "_spills rice_", parse_mode="Markdown")
		#send unplug GIF if a kill greeting has been sent 
		elif (any(x in msg["text"].lower() for x in killgreet) and "ricecooker" in msg["text"].lower()): 
			ricebot.sendDocument(chat_id, unpluggif)		
		#send greetings
		elif (msg["text"].lower() == "hi" or msg["text"].lower() == "hi rice"):
			time.sleep(1)
			ricebot.sendMessage(chat_id, random.choice(randomgreet), parse_mode="Markdown", disable_web_page_preview=None, disable_notification=True, reply_to_message_id=msg_id)


MessageLoop(ricebot, handle).run_as_thread()

while 1:
	time.sleep(10)
