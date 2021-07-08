#!/usr/bin/env python3

import json
import time
import datetime
import os
import re
import sys
import random
import telegram
import telegram.ext
from dotenv import load_dotenv, find_dotenv
from telegram.error import NetworkError, Unauthorized
from mediadata import *
from time import sleep
from telegram.ext.dispatcher import run_async

#big ol' blob of variables

load_dotenv(find_dotenv())

testGCID = int(os.getenv("TEST_GC"))
prodGCID = int(os.getenv("PROD_GC"))
cebGCID = int(os.getenv("CEB_GC"))
foodGCID = int(os.getenv("FOOD_GC"))
landichance = 0
angerychance = 0
atomchance = 0
leichance = 0
update_id = 0
testexpr = None
prodexpr = None

#Search if keywords in list are located in the string, based on regex pattern
def searchinString(keylist, msg, searchparam):
	found = 0
	matches = re.finditer(searchparam, msg)

	for matchNum, match in enumerate(matches):
		matchNum = matchNum + 1
		
		# print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
		for groupNum in range(0, len(match.groups())):
			groupNum = groupNum + 1
		
			# print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))
			#   print (match.group(groupNum))
			if (match.group(groupNum) in keylist):
				found = 1

	return found

#Delete message

def delmsg(context):
	msg = context.job
	msg.delete()


def pmhandle(update, context):
	#Initialize variables
	ricebot = context.bot
	msg_text = None
	msg_split = None
	angerychance = random.randint(1,4) % 4

	#Check if message has content
	if update.message:

		chat_id = update.message.chat_id
		msg_id = update.message.message_id

		if (update.message.text):
			msg_text = update.message.text.lower()
			msg_split = msg_text.split()	
			
			if (angerychance and ("hi" in msg_text)):
				time.sleep(1)
				ricebot.send_message(chat_id, random.choice(randomgreet), parse_mode="Markdown", disable_web_page_preview=None, disable_notification=True, reply_to_message_id=msg_id)
			#sad greetings autoreply
			elif (any(x in msg_split for x in sadgreet) and "rice" in msg_text):
				if searchinString(sadgreet, msg_text, searchparam=r"(\S+) @ricecooker"):
					ricebot.send_message(chat_id,"<.<", parse_mode="Markdown", disable_web_page_preview=None, disable_notification=True, reply_to_message_id=msg_id)
					time.sleep(1)
					ricebot.send_message(chat_id, ">.>", parse_mode="Markdown")
					ricebot.send_message(chat_id, "_spills rice_", parse_mode="Markdown")
				elif searchinString(sadgreet, msg_text, searchparam=r"(\S+) ricecooker"):
					ricebot.send_message(chat_id,"<.<", parse_mode="Markdown", disable_web_page_preview=None, disable_notification=True, reply_to_message_id=msg_id)
					time.sleep(1)
					ricebot.send_message(chat_id, ">.>", parse_mode="Markdown")
					ricebot.send_message(chat_id, "_spills rice_", parse_mode="Markdown")
				elif searchinString(sadgreet, msg_text, searchparam=r"(\S+) rice"):
					ricebot.send_message(chat_id,"<.<", parse_mode="Markdown", disable_web_page_preview=None, disable_notification=True, reply_to_message_id=msg_id)
					time.sleep(1)
					ricebot.send_message(chat_id, ">.>", parse_mode="Markdown")
					ricebot.send_message(chat_id, "_spills rice_", parse_mode="Markdown")
			#send unplug GIF if a kill greeting has been sent 
			elif (any(x in msg_split for x in killgreet) and "rice" in msg_text): 
				if searchinString(killgreet, msg_text, searchparam=r"(\S+) @ricecooker"):
					ricebot.send_animation(chat_id, unpluggif, reply_to_message_id=msg_id)
				elif searchinString(killgreet, msg_text, searchparam=r"(\S+) ricecooker"):
					ricebot.send_animation(chat_id, unpluggif, reply_to_message_id=msg_id)
				elif searchinString(killgreet, msg_text, searchparam=r"(\S+) rice"):
					ricebot.send_animation(chat_id, unpluggif, reply_to_message_id=msg_id)
			else:
				ricebot.send_message(testGCID, "Bot PM" + "\n" + update.message.from_user.name + "\n" + update.message.text, disable_notification=True)

def testGChandle(update, context):
	#Initialize variables
	ricebot = context.bot
	msg_text = None
	msg_split = None
	anm_id = None
	reply_user_id = None
	fwd_user_id = None
	sticker_id = None
	landichance = random.randint(1,6) % 5
	atomchance = random.randint(1,6) % 6
	leichance = random.randint(1,3) % 3
	
	#Check if message has content
	if (update.message):

		chat_id = update.message.chat_id
		msg_id = update.message.message_id
		user_id = update.message.from_user.id

		#Get original user ID from reply message
		if (update.message.reply_to_message):
			reply_user_id = update.message.reply_to_message.from_user.id
			reply_msg_id = update.message.reply_to_message.message_id
			reply_name = update.message.reply_to_message.from_user.mention_html(name=update.message.reply_to_message.from_user.full_name)
			ricebot.send_message(chat_id, "Reply user ID: \n" + str(reply_user_id))
			ricebot.send_message(chat_id, reply_name, parse_mode="HTML")
		#Get GIF file ID
		if (update.message.animation):
			anm_id = update.message.animation.file_id
			ricebot.send_message(chat_id, "GIF ID: \n" + anm_id)
		#Get user ID from forwarded messages
		if (update.message.forward_from):
			fwd_user_id = update.message.forward_from.id
			ricebot.send_message(chat_id, "Forwarded message user ID: " + str(fwd_user_id))
		#Get sticker file ID
		if (update.message.sticker):
			sticker_id = update.message.sticker.file_id
			ricebot.send_message(chat_id, "Sticker ID: \n" + sticker_id)
		#Get image file ID
		if (update.message.photo):
			ricebot.send_message(chat_id, "Photo File ID: \n" + update.message.photo[-1].file_id)
			ricebot.send_message(chat_id, update.message.caption)
			
		#Send motd when new members are added
		if (update.message.new_chat_members):
			ricebot.send_message(chat_id, "<code>All contents/events in this group chat are confidential. Disclosure is prohibited</code>", parse_mode="HTML", reply_to_message_id=msg_id)
			ricebot.send_message(chat_id, update.message.new_chat_members.first_name, disable_notification=True)
		#Check if message is text
		if (update.message.text):
			msg_text = update.message.text.lower()
			msg_split = msg_text.split()
			
			#Send message from testGC via riceBot
			#/chat:-chat_id textstring
			if ("/chat:" in msg_split[0]):
				new_chat_id = re.search(r"-\d+", msg_split[0]).group(0)
				lolstring = re.sub(r"/chat:-\d+\s", "", update.message.text)
				ricebot.send_message(new_chat_id, lolstring)
			#Send image from testGC via riceBot
			#/image:-chat_id img_id
			elif ("/image:" in msg_split[0]):
				new_chat_id = re.search(r"-\d+", msg_split[0]).group(0)
				lolimage = re.sub(r"/image:-\d+\s", "", update.message.text)
				ricebot.send_photo(new_chat_id, lolimage)
			#Send GIF from testGC via riceBot
			#/gif:-chat_id gif_id
			elif ("/gif:" in msg_split[0]):
				new_chat_id = re.search(r"-\d+", msg_split[0]).group(0)
				lolgif = re.sub(r"/gif:-\d+\s", "", update.message.text)
				ricebot.send_animation(new_chat_id, lolgif)
			#Send reply from testGC via riceBot
			#/reply:-chat_id msg_id textstring
			elif ("/reply:" in msg_split[0]):
				new_chat_id = re.search(r"-\d+", msg_split[0]).group(0)
				lolreply = re.sub(r"/reply:-\d+\s+\d+\s", "", update.message.text)
				ricebot.send_message(new_chat_id, lolreply, reply_to_message_id=msg_split[1])
			elif ("/adweedture" in msg_split[0]):
				ricebot.send_message(testGCID, random.choice(weedvid))
			#autoreply for gadon
			if (any(x in msg_text for x in gadongreet)):
				ricebot.send_animation(chat_id, random.choice(gadongif))
			#replace string test
			# elif ("pass" in msg_split):
			# 	print ("pass keyword found")
			# 	print (msg_text.replace("pass", "patawad"))
			# 	ricebot.send_message(chat_id, msg_text.replace("pass", "patawad"), reply_to_message_id=msg_id)
			#autoreply for bong revilla
			elif (any(x in msg_split for x in revillagreet) or "bong revilla" in msg_text):
				ricebot.send_animation(chat_id, revillagif, reply_to_message_id=msg_id)
			elif ("nothing at all" in msg_text):
				ricebot.send_animation(chat_id, flandersgif[0], reply_to_message_id=msg_id)
			#send 3 o' clock prayer pic
			elif ("3oclockpic" in msg_split):
				ricebot.send_photo(chat_id, "AgADBQADbagxG4ocsVfyRzCWKWz83cBQ9jIABFnbxMn-gKxBdGgBAAEC")
			#autoreply for thick thighs
			elif (msg_text == "send text test"):
				ricebot.send_message(chat_id, "<code>All contents/events in this group chat are confidential. \nDisclosure is prohibited</code>", parse_mode="HTML")
			elif (any(x in msg_split for x in tikigreet) and "thigh" in msg_text):
				if (searchinString(tikigreet, msg_text, searchparam=r"(\S+) thigh") or searchinString(tikigreet, msg_text, searchparam=r"(\S+) inner thigh")):
					ricebot.forward_message(chat_id, -1001255652659, 1496)
			#autoreply for genie ferdz gif
			elif (any(x in msg_split for x in ferdzgreet) and "ferdz" in msg_split):
				if searchinString(ferdzgreet, msg_text, searchparam=r"(\S+) ferdz"):
					ricebot.send_animation(chat_id, genieferdzgif)
			#autoreply for bless
			elif (any(x in msg_split for x in blessgreet) and random.randint(0,3)):
				if (update.message.reply_to_message):
					ricebot.send_animation(chat_id, random.choice(blessgif), reply_to_message_id=reply_msg_id)
				else:
					ricebot.send_animation(chat_id, random.choice(blessgif), reply_to_message_id=msg_id)
			#autoreply for drunk
			elif (any(x in msg_split for x in drunkgreet)):
				ricebot.send_photo(chat_id, random.choice(drunkpic), reply_to_message_id=msg_id)
			#autoreply for stress
			elif (any(x in msg_split for x in stressgreet) and random.randint(0,1)):
				ricebot.send_animation(chat_id, random.choice(stressgif), reply_to_message_id=msg_id)
			#autoreply for landi mo reply
			elif (update.message.reply_to_message and msg_text == "landi mo" and user_id != reply_user_id):
				ricebot.send_message(chat_id, "User ID: " + str(user_id) + " Reply user ID: " + str(reply_user_id), reply_to_message_id=reply_msg_id)
				print(landichance)
				if (landichance):
					ricebot.send_animation(chat_id, landigif[0], caption=None, parse_mode="Markdown", disable_notification=True, reply_to_message_id=reply_msg_id)
				else:
					ricebot.send_animation(chat_id, landigif[1], caption=None, parse_mode="Markdown", disable_notification=True, reply_to_message_id=reply_msg_id)
			#autoreply for luh with louise shrug
			elif ("luh" in msg_split and (random.randrange(0,100) < 40)):
				if (random.randint(0,15)):
					ricebot.send_animation(chat_id, louisegif[0], reply_to_message_id=msg_id)
				else:
					ricebot.send_animation(chat_id, louisegif[random.randint(1,4)], reply_to_message_id=msg_id)
			#autoreply for toasties
			elif ("toasties" in msg_split):
				ricebot.send_animation(chat_id, toastiesgif[0], reply_to_message_id=msg_id)
			#autoreply for assumption greetings
			elif (any(x in msg_text for x in assumptgreet)):
				time.sleep(1)			
				ricebot.send_message(chat_id, "Di ako yun", parse_mode="Markdown", disable_web_page_preview=None, disable_notification=True, reply_to_message_id=msg_id)
			#autoreply for weeaboos
			elif (any(x in msg_text for x in weebgreet)):
				ricebot.send_animation(chat_id, random.choice(weebgif))
			#autoreply for nice
			elif (update.message.reply_to_message and msg_text == "nice" and user_id != reply_user_id):
				ricebot.send_animation(chat_id, nicegif[0], reply_to_message_id=reply_msg_id)
			#autoreply for athens
			elif (user_id == 322520879 and any (x in msg_text for x in athensgreet)):
				if (random.randint(0,3)):
					ricebot.send_sticker(chat_id, "CAADBQADCQADL0c5E0v6frqfrAl0Ag", reply_to_message_id=msg_id)
				else:
					ricebot.send_animation(chat_id, "CgADBQADTQADUt_RVJBsyb0ugbBkAg", reply_to_message_id=msg_id)
			#autosend atom sticker
			elif ((any(x in msg_split for x in atomgreet)) and (atomchance != 0)):
				ricebot.send_sticker(chat_id, "CAADBQADHgADKGW-C2i6PBdd6c9ZAg", disable_notification=None, reply_to_message_id=msg_id)
			elif (any (x in msg_text for x in parrotgreet)):
				ricebot.send_animation(chat_id, random.choice(parrotgif), reply_to_message_id=msg_id)
			#Check if message is a certain GIF
			elif (anm_id and anm_id == "CgADBQADIQAD1PpYV9Q8SLVB8kHHAg"):
				if (leichance):
					ricebot.send_sticker(chat_id, random.choice(leisticker), reply_to_message_id=msg_id)
				else :
					ricebot.send_animation(chat_id, random.choice(leigif), reply_to_message_id=msg_id)
			elif (user_id == 456128183 and "hi" in msg_split):
				ricebot.send_message(chat_id, "<code>Negative</code>", parse_mode="HTML", reply_to_message_id=msg_id)
			elif ((user_id == 339707076 or user_id == 574787216) and (any(x in msg_split for x in justgreet))):
				ricebot.send_message(chat_id, "<code>Pass</code>", parse_mode="HTML")
			#weed jesus autoreply
			elif ("weed jesus" in msg_text):
				ricebot.send_animation(chat_id, weedjesusgif)
			#don't waste money autoreply
			elif (any(x in msg_text for x in saveupgreet)):
				if (random.randint(0,2)):
					if (update.message.reply_to_message):
						ricebot.send_photo(chat_id, saveuppic, reply_to_message_id=reply_msg_id)
					else:
						ricebot.send_photo(chat_id, saveuppic, reply_to_message_id=msg_id)
				else :
					if (update.message.reply_to_message):
						ricebot.send_animation(chat_id, random.choice(saveupgif), reply_to_message_id=reply_msg_id)
					else:
						ricebot.send_animation(chat_id, random.choice(saveupgif), reply_to_message_id=msg_id)
			#sad greetings autoreply
			elif (any(x in msg_split for x in sadgreet) and "rice" in msg_text):
				if searchinString(sadgreet, msg_text, searchparam=r"(\S+) @ricecooker"):
					ricebot.send_message(chat_id,"<.<", parse_mode="Markdown", disable_web_page_preview=None, disable_notification=True, reply_to_message_id=msg_id)
					time.sleep(1)
					ricebot.send_message(chat_id, ">.>", parse_mode="Markdown")
					ricebot.send_message(chat_id, "_spills rice_", parse_mode="Markdown")
				elif searchinString(sadgreet, msg_text, searchparam=r"(\S+) ricecooker"):
					ricebot.send_message(chat_id,"<.<", parse_mode="Markdown", disable_web_page_preview=None, disable_notification=True, reply_to_message_id=msg_id)
					time.sleep(1)
					ricebot.send_message(chat_id, ">.>", parse_mode="Markdown")
					ricebot.send_message(chat_id, "_spills rice_", parse_mode="Markdown")
				elif searchinString(sadgreet, msg_text, searchparam=r"(\S+) rice"):
					ricebot.send_message(chat_id,"<.<", parse_mode="Markdown", disable_web_page_preview=None, disable_notification=True, reply_to_message_id=msg_id)
					time.sleep(1)
					ricebot.send_message(chat_id, ">.>", parse_mode="Markdown")
					ricebot.send_message(chat_id, "_spills rice_", parse_mode="Markdown")
			#send unplug GIF if a kill greeting has been sent 
			elif (any(x in msg_split for x in killgreet) and "rice" in msg_text): 
				if searchinString(killgreet, msg_text, searchparam=r"(\S+) @ricecooker"):
					ricebot.send_animation(chat_id, unpluggif, reply_to_message_id=msg_id)
				elif searchinString(killgreet, msg_text, searchparam=r"(\S+) ricecooker"):
					ricebot.send_animation(chat_id, unpluggif, reply_to_message_id=msg_id)
				elif searchinString(killgreet, msg_text, searchparam=r"(\S+) rice"):
					ricebot.send_animation(chat_id, unpluggif, reply_to_message_id=msg_id)

def prodGChandle(update, context):
	#Initialize variables
	ricebot = context.bot
	msg_text = None
	msg_split = None
	anm_id = None
	atomchance = random.randint(1,6) % 6
	leichance = random.randint(1,3) % 3
	global prodexpr
	msgcontext = None

	#Check if message has content
	if (update.message):

		chat_id = update.message.chat_id
		msg_id = update.message.message_id
		user_id = update.message.from_user.id

		#Get original user ID from reply message
		if (update.message.reply_to_message):
			reply_user_id = update.message.reply_to_message.from_user.id
			reply_msg_id = update.message.reply_to_message.message_id

		if (update.message.text):
			msg_text = update.message.text.lower()
			msg_split = msg_text.split()	

			#autoreply for athens
			if (user_id == 322520879 and any (x in msg_text for x in athensgreet)):
				ricebot.send_sticker(chat_id, "CAADBQADCQADL0c5E0v6frqfrAl0Ag", reply_to_message_id=msg_id)
			# autoreply for landi mo 
			# elif (update.message.reply_to_message and msg_text == "landi mo" and user_id != reply_user_id):
			# 	if (landichance):
			# 		ricebot.send_animation(chat_id, landigif[0], caption=None, parse_mode="Markdown", disable_notification=True, reply_to_message_id=reply_msg_id)
			# 	else:
			# 		ricebot.send_animation(chat_id, landigif[1], caption=None, parse_mode="Markdown", disable_notification=True, reply_to_message_id=reply_msg_id)
			# elif ("pass" in msg_split):
			# 	print ("pass keyword found")
			# 	print (msg_text.replace("pass", "patawad"))
			# 	ricebot.send_message(chat_id, msg_text.replace("pass", "patawad"), reply_to_message_id=msg_id)
			#autoreply for hipo messages
			# elif (msg_text == "hipo" and user_id != 322520879):
			# 	if (landichance):
			# 		ricebot.send_document(chat_id, landigif[0], caption=None, parse_mode="Markdown", disable_notification=True, reply_to_message_id=msg_id)
			# 	else:
			# 		ricebot.send_document(chat_id, landigif[1], caption=None, parse_mode="Markdown", disable_notification=True, reply_to_message_id=msg_id)
			#autoreply for stress
			#autoreply for gadon
			if (any(x in msg_text for x in gadongreet)):
				ricebot.send_animation(chat_id, random.choice(gadongif))
			elif (any(x in msg_split for x in stressgreet) and random.randint(0,1)):
				ricebot.send_animation(chat_id, random.choice(stressgif), disable_notification=True, reply_to_message_id=msg_id)
			#autoreply for bless
			elif (any (x in msg_split for x in blessgreet) and random.randint(0,3)):
				if (update.message.reply_to_message):
					ricebot.send_animation(chat_id, random.choice(blessgif), reply_to_message_id=reply_msg_id)
				else:
					ricebot.send_animation(chat_id, random.choice(blessgif), reply_to_message_id=msg_id)
			#autoreply for lei's narcissism
			elif ((user_id == 477167517) and (any(x in msg_text for x in leigreetphrase) or any(y in msg_split for y in leigreetword))):
				if (leichance):
					ricebot.send_sticker(chat_id, random.choice(leisticker), reply_to_message_id=msg_id)
				else :
					ricebot.send_animation(chat_id, random.choice(leigif), reply_to_message_id=msg_id)
			#autoreply for weaboos
			elif(any(x in msg_text for x in weebgreet)):
				ricebot.send_animation(chat_id, random.choice(weebgif), disable_notification=True)
			#autoreply for luh with louise shrug
			# elif ("luh" in msg_split and (random.randrange(0,100) < 40)):
			# 	if (random.randint(0,15)):
			# 		ricebot.send_animation(chat_id, louisegif[0], reply_to_message_id=msg_id)
			# 	else:
			# 		ricebot.send_animation(chat_id, louisegif[random.randint(1,4)], disable_notification=True, reply_to_message_id=msg_id)
			#autoreply for drunk
			elif (any (x in msg_split for x in drunkgreet) and leichance):
				ricebot.send_photo(chat_id, random.choice(drunkpic), reply_to_message_id=msg_id)
			#autosend atom sticker
			elif ((any(x in msg_split for x in atomgreet)) and (atomchance == 0)):
				ricebot.send_sticker(chat_id, "CAADBQADHgADKGW-C2i6PBdd6c9ZAg", disable_notification=True, reply_to_message_id=msg_id)
			#party parrot autoreply
			elif (any (x in msg_text for x in parrotgreet)):
				if (random.randrange(1,100) < 6):
					ricebot.send_animation(chat_id, "CgADAQADPQADtY9QRi3NGeEEAmLKAg", reply_to_message_id=msg_id)
				else:
					ricebot.send_animation(chat_id, random.choice(parrotgif), disable_notification=True, reply_to_message_id=msg_id)
			#assumptions autoreply
			elif (any(x in msg_text for x in assumptgreet)):
				time.sleep(1)			
				ricebot.send_message(chat_id, "Di ako yun", parse_mode="Markdown", disable_web_page_preview=True, disable_notification=True, reply_to_message_id=msg_id)
			#autoreply for genie ferdz gif
			elif (("genie" in msg_split or "happy" in msg_split) and ("ferdz" in msg_split or "ferds" in msg_split)):
				if searchinString(ferdzgreet, msg_text, searchparam=r"(\S+) ferdz"):
					ricebot.send_animation(chat_id, genieferdzgif)
			#autoreply for happy jake gif
			elif ("happy" in msg_split and "jake" in msg_split):
				if searchinString(jakegreet, msg_text, searchparam=r"(\S+) jake"):
					ricebot.send_animation(chat_id, random.choice(jakegif))
			#autoreply for thick thighs
			elif (any(x in msg_split for x in tikigreet) and "thigh" in msg_text):
				if (searchinString(tikigreet, msg_text, searchparam=r"(\S+) thigh") or searchinString(tikigreet, msg_text, searchparam=r"(\S+) inner thigh")):
					ricebot.forward_message(chat_id, -1001255652659, 1496)
			#autoreply for toasties
			elif ("toasties" in msg_split and random.randint(0, 1)):
				ricebot.send_animation(chat_id, toastiesgif[0], reply_to_message_id=msg_id)
			#autoreply for jerome and athens pic
			elif (msg_text == "jerathens"):
				msgcontext = ricebot.send_photo(chat_id, "AgADBQADVagxG9cuOVfXq7usGDCFAsZo3jIABCF2Vg7uGe3afUIAAgI")
				prodexpr.run_once(delmsg, 3, context=msgcontext)
			elif ("nothing at all" in msg_text):
				ricebot.send_animation(chat_id, flandersgif[0], reply_to_message_id=msg_id)
			#weed jesus autoreply
			elif ("weed jesus" in msg_text):
				ricebot.send_animation(chat_id, weedjesusgif)
			#don't waste money autoreply
			elif (any(x in msg_text for x in saveupgreet)):
				if (random.randint(0,2)):
					if (update.message.reply_to_message):
						ricebot.send_photo(chat_id, saveuppic, reply_to_message_id=reply_msg_id)
					else:
						ricebot.send_photo(chat_id, saveuppic, reply_to_message_id=msg_id)
				else :
					if (update.message.reply_to_message):
						ricebot.send_animation(chat_id, random.choice(saveupgif), reply_to_message_id=reply_msg_id)
					else:
						ricebot.send_animation(chat_id, random.choice(saveupgif), reply_to_message_id=msg_id)
			# #greetings autoreply
			# elif (user_id == 456128183 and "hi" in msg_split):
			# 	ricebot.send_message(chat_id, "<code>Negative</code>", parse_mode="HTML", reply_to_message_id=msg_id)
			# elif ((user_id == 339707076 or user_id == 574787216) and (any(x in msg_split for x in justgreet))):
			# 	ricebot.send_message(chat_id, "<code>Pass</code>", parse_mode="HTML")
			# elif (user_id != 236212097 and angerychance and any(x in msg_split for x in justgreet)):
			# 	time.sleep(1)
			# 	ricebot.send_message(chat_id, random.choice(randomgreet), parse_mode="Markdown", disable_web_page_preview=None, disable_notification=True, reply_to_message_id=msg_id)
			#sad greetings autoreply
			elif (any(x in msg_split for x in sadgreet) and "rice" in msg_text):
				if searchinString(sadgreet, msg_text, searchparam=r"(\S+) @ricecooker"):
					ricebot.send_message(chat_id,"<.<", parse_mode="Markdown", disable_web_page_preview=None, disable_notification=True, reply_to_message_id=msg_id)
					time.sleep(1)
					ricebot.send_message(chat_id, ">.>", parse_mode="Markdown")
					ricebot.send_message(chat_id, "_spills rice_", parse_mode="Markdown")
				elif searchinString(sadgreet, msg_text, searchparam=r"(\S+) ricecooker"):
					ricebot.send_message(chat_id,"<.<", parse_mode="Markdown", disable_web_page_preview=None, disable_notification=True, reply_to_message_id=msg_id)
					time.sleep(1)
					ricebot.send_message(chat_id, ">.>", parse_mode="Markdown")
					ricebot.send_message(chat_id, "_spills rice_", parse_mode="Markdown")
				elif searchinString(sadgreet, msg_text, searchparam=r"(\S+) rice"):
					ricebot.send_message(chat_id,"<.<", parse_mode="Markdown", disable_web_page_preview=None, disable_notification=True, reply_to_message_id=msg_id)
					time.sleep(1)
					ricebot.send_message(chat_id, ">.>", parse_mode="Markdown")
					ricebot.send_message(chat_id, "_spills rice_", parse_mode="Markdown")
			#send unplug GIF if a kill greeting has been sent 
			elif (any(x in msg_split for x in killgreet) and "rice" in msg_text): 
				if searchinString(killgreet, msg_text, searchparam=r"(\S+) @ricecooker"):
					ricebot.send_animation(chat_id, unpluggif, reply_to_message_id=msg_id)
				elif searchinString(killgreet, msg_text, searchparam=r"(\S+) ricecooker"):
					ricebot.send_animation(chat_id, unpluggif, reply_to_message_id=msg_id)
				elif searchinString(killgreet, msg_text, searchparam=r"(\S+) rice"):
					ricebot.send_animation(chat_id, unpluggif, reply_to_message_id=msg_id)
			elif (any (x in msg_text for x in parrotgreet)):
					ricebot.send_animation(chat_id, random.choice(parrotgif), reply_to_message_id=msg_id)
		elif (update.message.new_chat_members):
			ricebot.send_message(chat_id, "<code>Hi! Welcome to r/ph tele! \n\nAs part of catfish verification standard procedures, we ask for a selfie of you with a tabo (tabofie) or a tinidor (tinidorfie). \nHave fun and stay fake!</code>", parse_mode="HTML", reply_to_message_id=msg_id)
		elif (anm_id and anm_id == "CgADBQADjwADxbwAAVQdtvEQ-lCPGwI"):
			ricebot.send_animation(chat_id, random.choice(stressgif), reply_to_message_id=msg_id)
		elif (anm_id and (anm_id == "CgADBQADIQAD1PpYV9Q8SLVB8kHHAg" or anm_id == "CgADBQADCQAD2MkBV-93jXgFs7gBAg")):
			if (leichance):
				ricebot.send_sticker(chat_id, random.choice(leisticker), reply_to_message_id=msg_id)
			else :
				ricebot.send_animation(chat_id, random.choice(leigif), reply_to_message_id=msg_id)

def cebGChandle(update: telegram.Update, context: telegram.ext.CallbackContext):
	#Initialize variables
	ricebot = context.bot

	msg_text = None
	msg_split = None
	reply_user_id = None

	#Check if message has content
	if (update.message):

		chat_id = update.message.chat_id
		msg_id = update.message.message_id

		if (update.message.text):
			msg_text = update.message.text.lower()
			msg_split = msg_text.split()
			ricebot.send_message(testGCID, update.message.from_user.name + "\n" + update.message.text, disable_notification=True)
			if (any(x in msg_text for x in weebgreet)):
				ricebot.send_animation(chat_id, random.choice(weebgif))
			#autoreply for bong revilla
			# elif (any(x in msg_split for x in revillagreet) or "bong revilla" in msg_text):
			# 	ricebot.send_animation(chat_id, revillagif, reply_to_message_id=msg_id)
			elif (any(x in msg_split for x in sadgreet) and "rice" in msg_text):
				if searchinString(sadgreet, msg_text, searchparam=r"(\S+) @ricecooker"):
					ricebot.send_message(chat_id,"<.<", parse_mode="Markdown", disable_web_page_preview=None, disable_notification=True, reply_to_message_id=msg_id)
					time.sleep(1)
					ricebot.send_message(chat_id, ">.>", parse_mode="Markdown")
					ricebot.send_message(chat_id, "_spills rice_", parse_mode="Markdown")
				elif searchinString(sadgreet, msg_text, searchparam=r"(\S+) ricecooker"):
					ricebot.send_message(chat_id,"<.<", parse_mode="Markdown", disable_web_page_preview=None, disable_notification=True, reply_to_message_id=msg_id)
					time.sleep(1)
					ricebot.send_message(chat_id, ">.>", parse_mode="Markdown")
					ricebot.send_message(chat_id, "_spills rice_", parse_mode="Markdown")
				elif searchinString(sadgreet, msg_text, searchparam=r"(\S+) rice"):
					ricebot.send_message(chat_id,"<.<", parse_mode="Markdown", disable_web_page_preview=None, disable_notification=True, reply_to_message_id=msg_id)
					time.sleep(1)
					ricebot.send_message(chat_id, ">.>", parse_mode="Markdown")
					ricebot.send_message(chat_id, "_spills rice_", parse_mode="Markdown")
			#send unplug GIF if a kill greeting has been sent 
			elif (any(x in msg_split for x in killgreet) and "rice" in msg_text): 
				if searchinString(killgreet, msg_text, searchparam=r"(\S+) @ricecooker"):
					ricebot.send_animation(chat_id, unpluggif, reply_to_message_id=msg_id)
				elif searchinString(killgreet, msg_text, searchparam=r"(\S+) ricecooker"):
					ricebot.send_animation(chat_id, unpluggif, reply_to_message_id=msg_id)
				elif searchinString(killgreet, msg_text, searchparam=r"(\S+) rice"):
					ricebot.send_animation(chat_id, unpluggif, reply_to_message_id=msg_id)
			elif (any (x in msg_text for x in parrotgreet)):
				ricebot.send_animation(chat_id, random.choice(parrotgif), reply_to_message_id=msg_id)
		elif (update.message.photo):
			ricebot.send_photo(testGCID, update.message.photo[-1].file_id, caption=update.message.caption)
		elif (update.message.animation):
			ricebot.send_animation(testGCID, update.message.animation.file_id, caption=update.message.caption)
		
		# if (update.message.new_chat_members):
		# 	ricebot.send_message(chat_id, "<code>Welcome to r/Sugbo Telegram!\n\nAs part of our verification, kindly post a selfie holding a silhig tukog or a stapler.\n\nHave fun!</code>", parse_mode="HTML", reply_to_message_id=msg_id)

def chat_id_capture(update, context):
	ricebot = context.bot
	chat_id = update.message.chat_id

	ricebot.send_message(testGCID, "Group chat ID: " + str(chat_id))

def foodGChandle(update, context):
	# Initialize variables
	ricebot = context.bot
	chat_id = update.message.chat_id

	#Add welcome greeter
	if (update.message.new_chat_members):
		ricebot.send_message(chat_id, "<code>Hello sa mga bago. Lapag kayo ng mga subo GIF. OO REQUIRED TO BAKLA!\n\nRules:\n1. I-video ang sarili nang walang audio na sumusubo ng pagkain.\n2. Once naglapag ka, verified tao ka. Hindi ka catfish.\n3. Bawal sumubo ng tao.\n\nGood morning po and happy eating ng ina nyo.</code>", parse_mode="HTML", reply_to_message_id=update.message.message_id)

def cronjobdos(context):
# 	context.bot.send_message(testGCID, "CRON JOB 420 ACTIVATED")
	context.bot.send_animation(prodGCID, random.choice(ftwentygif))
	if (random.randrange(0,9) == 5):
		context.bot.send_message(cebGCID, random.choice(weedvid))
	else:
		context.bot.send_animation(cebGCID, random.choice(cebweedgif))
	

def cronjobgreet(context):
	context.bot.send_photo(cebGCID, morningpic)
	if (random.randrange(0,2) == 2):
		context.bot.send_photo(cebGCID,"AgACAgUAAx0CSte9MwABAUb6YH6q6KD42fTZ3GbMK85_MZ_q1-MAAu6rMRtcRfBXUv3Fe9F-GVj-Fr9vdAADAQADAgADeQAD8uUDAAEfBA")


def cronjobpray(context):
	context.bot.send_photo(prodGCID, prayerpic)


def cronjobfrog(context):
	if (random.randrange(0,4)):
		context.bot.send_photo(prodGCID, wednesdayfrogpic)
		context.bot.send_photo(cebGCID, wednesdayfrogpic)
	else:
		froggif = random.choice(wednesdayfroggif)
		context.bot.send_animation(prodGCID, froggif)
		context.bot.send_animation(cebGCID, froggif)

def main():
	updater = telegram.ext.Updater(os.getenv("BOT_TOKEN"), use_context=True)
	dp = updater.dispatcher
	rm = updater.job_queue
	ma = updater.job_queue

	dp.add_handler(telegram.ext.CommandHandler("getchatid", chat_id_capture, pass_chat_data=True))
	dp.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.chat(testGCID), testGChandle))
	dp.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.chat(prodGCID), prodGChandle))
	dp.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.chat(foodGCID), foodGChandle))
	dp.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.chat(cebGCID), cebGChandle))
	dp.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.private, pmhandle))
	
	fourtwenty = rm.run_daily(cronjobdos, datetime.time(8,20,15,0))
	fourtwenty.enabled = True
	
	mnggrtsched = ma.run_daily(cronjobgreet, datetime.time(22,0,4,0), days=(0,2,3,4,5,6))
	mnggrtsched.enabled = True

	prayersched = rm.run_daily(cronjobpray, datetime.time(7,0,3,0))
	prayersched.enabled = True

	frogsched = ma.run_daily(cronjobfrog, datetime.time(22,30,3,0), days=(1,))
	frogsched.enabled = True

	updater.start_polling()

	updater.idle()

if __name__ == "__main__":
    main()

#Credits to the Python Telegram Bot team for the wonderful wrapper and examples
