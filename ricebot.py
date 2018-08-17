import json
import time
import os
import sys
import telepot
import telepot.text
import random

from telepot.loop import MessageLoop

ricebot = telepot.Bot("629508118:AAFCWu7nZRfHw_iOhy_xA488x5Qe6XGZHMc")
riceID = ricebot.getMe()
ricecontent = 0
sadgreet = ["spills", "trips", "eats", "bites", "tips", "tips over"]
killgreet = ["unplug", "bang", "kill", "rip"]
randomgreet = ["Hello", "Hi", "Greetings", "Good day", "How are ya?", "Yes", "No"]
unpluggif = "CgADBQADNwADtjzaDXzFsIuaINkHAg"

def handle(msg):
    content_type, chat_type, chat_id, msg_date, msg_id = telepot.glance(msg, flavor="chat", long="True")


    if content_type == "text":
        if (any(x in msg["text"].lower() for x in sadgreet) and "ricecooker" in msg["text"].lower()):
            ricebot.sendMessage(chat_id,"<.<", parse_mode="Markdown", disable_web_page_preview=None, disable_notification=True, reply_to_message_id=msg_id)
            time.sleep(1)
            ricebot.sendMessage(chat_id, ">.>", parse_mode="Markdown")
            ricebot.sendMessage(chat_id, "_spills rice_", parse_mode="Markdown")
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
