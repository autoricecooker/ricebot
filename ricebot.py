import json
import time
import os
import sys
import telepot
import telepot.text
import random

from telepot.loop import MessageLoop


ricebot = telepot.Bot(os.environ["BOT_TOKEN"])
wwgc = telepot.Bot(os.environ["WW_GC"])
riceID = ricebot.getMe()
ricecontent = 0
sadgreet = ["spill", "trip", "eat", "bite", "tips", "tips over"]
killgreet = ["unplug", "bang", "kill", "rip"]
randomgreet = ["Hello", "Hi", "Greetings", "Good day", "How are ya?", "Yes", "No", "What's up?"]
unpluggif = "CgADBQADNwADtjzaDXzFsIuaINkHAg"

def handle(msg):
    content_type, chat_type, chat_id, msg_date, msg_id = telepot.glance(msg, flavor="chat", long="True")


    if content_type == "text":
        print(chat_id)
        if (any(x in msg["text"].lower() for x in sadgreet) and "ricecooker" in msg["text"].lower()):
            ricebot.sendMessage(chat_id,"<.<", parse_mode="Markdown", disable_web_page_preview=None, disable_notification=True, reply_to_message_id=msg_id)
            time.sleep(1)
            ricebot.sendMessage(chat_id, ">.>", parse_mode="Markdown")
            ricebot.sendMessage(chat_id, "_spills rice_", parse_mode="Markdown")
        #send WW GC invite link in main GC
        elif (("werewolf" in msg["text"]) or ("nextgame@werewolfbot" in msg["text"])) and (chat_id == "-234762812"):
            ricebot.sendMessage(chat_id, "Hi, you may join this GC's werewolf game channel at https://t.me/joinchat/" + wwgc, parse_mode="Markdown", disable_web_page_preview=None, disable_notification=True, reply_to_message_id=msg_id)
        #send unplug GIF if a kill greeting has been sent        
        elif (any(x in msg["text"].lower() for x in killgreet) and "ricecooker" in msg["text"].lower()): 
            ricebot.sendDocument(chat_id, unpluggif)
        #send reply based on parameters
        #elif ((msg["from"]["username"] is not None) and (msg["from"]["username"] != "riceCooker") and (msg["text"].lower() == "hi")):
        elif ((msg["from"]["username"] != "riceCooker") and (msg["text"].lower() == "hi")):
            #print (msg["from"]["username"])
            time.sleep(1)
            ricebot.sendMessage(chat_id, random.choice(randomgreet), parse_mode="Markdown", disable_web_page_preview=None, disable_notification=True, reply_to_message_id=msg_id)


MessageLoop(ricebot, handle).run_as_thread()

while 1:
    time.sleep(10)
