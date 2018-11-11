import json
import time
import datetime
import os
import re
import sys
import random
import telegram
import telegram.ext
from pprint import pprint
from telegram.error import NetworkError, Unauthorized
from time import sleep

#big ol' blob of variables

#wwgc = os.environ["WW_GC"]
sadgreet = ["spill", "trip", "eat", "bite", "tips", "tips over"]
killgreet = ["unplug", "kill", "rip", "destroy", "hate"]
randomgreet = ["Hello", "Hi", "Greetings", "Good day", "How are ya?", "Yes", "No", "What's up?"]
assumptgreet = ["akala ko si rice", "akala ko si ricecooker", "akala ko si @ricecooker", "kala ko si rice", "kala ko si @ricecooker", "kala ko si ricecooker", "ikaw ba yan rice", "kaw ba yan rice", "rice ikaw ba yan", "rice kaw ba yan", "ikaw ba yan @ricecooker"]
angerygreet = ["Shooo", "...", "Wag ka na", ":|"]
athensgreet =["athens", "ganda ako", "ganda ko", "cute ako", "cute me", "cute kasi ako", "cute ko", "cute talaga ako","maganda talaga ako", "maganda kasi ako", "im beautiful", "i am beautiful", "i'm beautiful"]
stressgreet = ["stress", "stresss", "stressss", "stressed", "stressssss", "overstress", "megastress"]
blessgreet = ["bless", "blesss", "blessed"]
drunkgreet = ["lasing"]
werewolfcommands = ["/werewolf@riceCookerisnotAbot", "/startchaos@werewolfbot", "/nextgame@werewolfbot", "/start@werewolfbot",]
atomgreet = ["atom", "nambabakod"]
parrotgreet = ["party parrot", "partyparrot"]
tikigreet = ["meaty", "thicc", "thick", "tiki"]
ferdzgreet = ["happy", "genie"]
jakegreet = ["happy", "joyful"]
justgreet = ["hi", "hello", "henlo", "hallu", "elo", "hellu", "haller", "haler"]
leigreetphrase = ["cute ako", "maganda ako", "pinaka cute", "pinaka maganda", "i am beautiful", "sexy ako", "most beautiful", "ganda ko", "5'11", "qt ko", "qt ako"]
leigreetword = ["pinakacute", "cute", "pinakamaganda"]
leisticker = ["CAADBQADIQEAAiO4mBCSjVKUWk7MNwI", "CAADBQADHAEAAiO4mBCeaC0LYAlkowI", "CAADBQADIAEAAiO4mBD3UdIBPEO6WwI", "CAADBQADGwEAAiO4mBC51PR572t9EgI", "CAADBQADHwEAAiO4mBBJWiwq_cjWdQI", "CAADBQADHgEAAiO4mBBMQuYcpcSX2AI"]
#leigif = ["CgADBQADEAADS754Vj0cIPOA5fAWAg", "CgADBQADFQADDHrhVXLWPyi-fVESAg", "CgADBQADEQADNNrpV0yGyX3SyadcAg", "CgADBQADHwADYlzxVd_bBWXEyqHUAg"]
leigif = ["CgADBQADEQADNNrpV_JyDVwU2d1rAg", "CgADBQADFQADDHrhVeaTS0bvbyRWAg", "CgADBQADEAADS754Vha1dmKytEvNAg", "CgADBQADHwADYlzxVfOzb9cCUkuqAg"]
#stressgif = ["CgADBQADNgAD1k_RVO3goPd_-i6UAg", "CgADBQADeAADXqhQVB4H-vGgquQBAg", "CgADBQADagADIQNZVQwwt6F0hhTnAg", "CgADBQADMQADSQ5QVWEW6SjSG4KYAg"]
stressgif = ["CgADBQADeAADXqhQVCksGu6IfbQMAg", "CgADBQADMQADSQ5QVUn-yBLRrDvBAg", "CgADBQADagADIQNZVdJEKrwDU24lAg", "CgADBQADNgAD1k_RVFSZibSpxmu4Ag"]
blessgif =["CgADBQADQwADUt_RVJbf7QgSjFMQAg"]
#genieferdzgif = "CgADBQADEgADUT_BVphVHpXa9x1UAg"
genieferdzgif = "CgADBQADEgADUT_BVqvCsq_FYDT-Ag"
#unpluggif = "CgADBQADNwADtjzaDem_pNtFz2CxAg"
unpluggif = "CgADBQADNwADtjzaDXzFsIuaINkHAg"
#landigif = ["CgADBQADKQADvG2JViq33V_DvoF9Ag", "CgADBQADHQAD6QuQVwZwVsITdN6hAg"]
landigif = ["CgADBQADHQAD6QuQV_mxPdwxj0s2Ag", "CgADBQADKQADvG2JVi4mEJDnylDvAg"]
louisegif = ["CgADBQADHAADVMqxV2iqwCWWKYXRAg", "CgADBQADRQADggs5VTtpVvYfIcqBAg", "CgADBQADGwADwI9BVYEBhY4qglXKAg", "CgADBQADWwADfhjQVy2VyBHiS3kWAg", "CgADBQADXQADlN5hVIkXruw21LEsAg"]
toastiesgif = ["CgADBQADLwADv4dBVFVtZJ9jdSwFAg"]
jakegif = ["CgADBQADBwADGIgpVpF8EgH6Mc-9Ag"]
drunkpic = ["AgADBQADOagxGxB_aVZNfo9wNUvyYvGl1jIABMOR93PzURnicEMDAAEC", "AgADBQADOqgxGxB_aVav5vKmhLduCGqk1jIABOQDiHpGpExCJUMDAAEC", "AgADBQADkagxG6Oe8FbPeySNTsva1S5U2zIABHbiq4wGrTTHhxABAAEC", "AgADBQADYKgxGzx76FYspQoUVI_orGFh2zIABPdENNUjOZ6HMQoBAAEC", "AgADBQADyagxG3vgQFfzWyPyZwABhDpToNYyAARIZLO6JHE6rwHyAwABAg", "AgADBQADyqgxG3vgQFdnwo6v0N37ltKu1jIABImnO1LEv_hLsvgDAAEC", "AgADBQADy6gxG3vgQFdhN5CqLNBoaZps3jIABIzvbj8OdXrYa0EAAgI", "AgADBQADzKgxG3vgQFd0wYPinyYN3Zhq2zIABNpbg4ad52tcN0oBAAEC"]
parrotgif = ["CgADBQADLQADkxKZVrE-Wx30uXiNAg", "CgADBQADWAADeL-YVnw3sjCV8aeLAg", "CgADBQADMAADkxKZVp3RsGgriq4TAg", "CgADBQADWQADeL-YVsV0J7Zx1H3-Ag", "CgADBQADLwADamEJVwABfmqsGruuIAI"]
landichance = 0
angerychance = 0
atomchance = 0
leichance = 0
update_id = 0

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

def handle(ricebot, update):
	#Initialize variables
	msg_text = None
	msg_split = None
	anm_id = None
	reply_user_id = None
	fwd_user_id = None
	sticker_id = None
	landichance = random.randint(1,6) % 5
	angerychance = random.randint(1,4) % 4
	atomchance = random.randint(1,6) % 6
	leichance = random.randint(1,3) % 3

	#Check if message has content
	if update.message:

		chat_id = update.message.chat_id
		msg_id = update.message.message_id
		user_id = update.message.from_user.id

		#Get message text if not none
		if (update.message.text):
			msg_text = update.message.text.lower()
			msg_split = msg_text.split()	
		#Get original user ID from reply message
		if (update.message.reply_to_message):
			reply_user_id = update.message.reply_to_message.from_user.id
			reply_msg_id = update.message.reply_to_message.message_id
		#Get GIF file ID
		if (update.message.animation):
			anm_id = update.message.animation.file_id
		#Get user ID from forwarded messages
		if (update.message.forward_from):
			fwd_user_id = update.message.forward_from.id
		#Get sticker file ID
		if (update.message.sticker):
			sticker_id = update.message.sticker.file_id

		#For testGC input
		if (chat_id == -1001255652659):

			#Send motd when new members are added
			if (update.message.new_chat_members):
				ricebot.send_message(-1001255652659, "<code>All contents/events in this group chat are confidential. Disclosure is prohibited</code>", parse_mode="HTML")
			#Check if message is text
			if (msg_text):
				if (msg_text == "hipo"):
					if (landichance):
						ricebot.send_document(chat_id, landigif[0], caption=None, parse_mode="Markdown", disable_notification=True, reply_to_message_id=msg_id)
					else:
						ricebot.send_document(chat_id, landigif[1], caption=None, parse_mode="Markdown", disable_notification=True, reply_to_message_id=msg_id)
				elif (msg_text == "jerathens"):
					ricebot.send_photo(chat_id, "AgADBQADVagxG9cuOVfXq7usGDCFAsZo3jIABCF2Vg7uGe3afUIAAgI")
				#autoreply for thick thighs
				elif (any(x in msg_split for x in tikigreet) and "thigh" in msg_text):
					if searchinString(tikigreet, msg_text, searchparam=r"(\S+) thigh"):
						ricebot.forward_message(chat_id, -1001255652659, 1496)
				#autoreply for genie ferdz gif
				elif (any(x in msg_split for x in ferdzgreet) and "ferdz" in msg_split):
					if searchinString(ferdzgreet, msg_text, searchparam=r"(\S+) ferdz"):
						ricebot.send_animation(chat_id, genieferdzgif)
				#autoreply for bless
				elif (any(x in msg_split for x in blessgreet) and random.randint(0,3)):
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
				
			if (reply_user_id):
				ricebot.send_message(chat_id,"Reply user ID: " + str(reply_user_id))
			if (anm_id):
				if (anm_id == "CgADBQADIQAD1PpYV8uam3a7hV41Ag"):
					ricebot.send_sticker(chat_id, random.choice(leisticker), reply_to_message_id=msg_id)
				ricebot.send_message(chat_id, anm_id)
			if (sticker_id):
				ricebot.send_message(chat_id, sticker_id)
			if (update.message.photo):
				ricebot.send_message(chat_id, update.message.photo[-1].file_id)
			if (update.message.document):
				ricebot.send_message(chat_id, str(update.message.document.file_id))
			
			#Check if message is forwarded
			if (fwd_user_id):
					ricebot.send_message(chat_id, "Forwarded message user ID: " + str(fwd_user_id))
		
		#For production GC input
		elif (chat_id == -1001043875036):
			if (msg_text and user_id != 456128183):
				#autoreply for athens
				if (user_id == 322520879):
					if (msg_text == "hipo" or msg_text == "landi mo" or msg_split == "hi" or any(x in msg_split for x in stressgreet) or "luh" in msg_split):
						ricebot.send_message(chat_id, random.choice(angerygreet), parse_mode="Markdown", disable_web_page_preview=None, disable_notification=True, reply_to_message_id=msg_id)
					elif (any (x in msg_text for x in athensgreet)):
						ricebot.send_sticker(chat_id, "CAADBQADCQADL0c5E0v6frqfrAl0Ag", reply_to_message_id=msg_id)
				#autoreply for landi mo 
				elif (update.message.reply_to_message and msg_text == "landi mo" and user_id != reply_user_id):
					if (landichance):
						ricebot.send_animation(chat_id, landigif[0], caption=None, parse_mode="Markdown", disable_notification=True, reply_to_message_id=reply_msg_id)
					else:
						ricebot.send_animation(chat_id, landigif[1], caption=None, parse_mode="Markdown", disable_notification=True, reply_to_message_id=reply_msg_id)
				#autoreply for hipo messages
				elif (msg_text == "hipo" and user_id != 322520879):
					if (landichance):
						ricebot.send_document(chat_id, landigif[0], caption=None, parse_mode="Markdown", disable_notification=True, reply_to_message_id=msg_id)
					else:
						ricebot.send_document(chat_id, landigif[1], caption=None, parse_mode="Markdown", disable_notification=True, reply_to_message_id=msg_id)
				#autoreply for stress
				elif (any(x in msg_split for x in stressgreet) and random.randint(0,1)):
					ricebot.send_animation(chat_id, random.choice(stressgif), reply_to_message_id=msg_id)
				#autoreply for bless
				elif (any (x in msg_split for x in blessgreet) and random.randint(0,3)):
					ricebot.send_animation(chat_id, random.choice(blessgif), reply_to_message_id=msg_id)
				#autoreply for lei's narcissism
				elif ((user_id == 477167517) and (any(x in msg_text for x in leigreetphrase) or any(y in msg_split for y in leigreetword))):
					if (leichance):
						ricebot.send_sticker(chat_id, random.choice(leisticker))
					else :
						ricebot.send_animation(chat_id, random.choice(leigif))
				#autoreply for luh with louise shrug
				elif ("luh" in msg_split and (random.randrange(0,100) < 40)):
					if (random.randint(0,15)):
						ricebot.send_animation(chat_id, louisegif[0], reply_to_message_id=msg_id)
					else:
						ricebot.send_animation(chat_id, louisegif[random.randint(1,4)], reply_to_message_id=msg_id)
				#autoreply for drunk
				elif (any (x in msg_split for x in drunkgreet) and leichance):
					ricebot.send_photo(chat_id, random.choice(drunkpic), reply_to_message_id=msg_id)
				#autosend atom sticker
				elif ((any(x in msg_split for x in atomgreet)) and (atomchance == 0)):
					ricebot.send_sticker(chat_id, "CAADBQADHgADKGW-C2i6PBdd6c9ZAg", disable_notification=None, reply_to_message_id=msg_id)
				#party parrot autoreply
				elif (any (x in msg_text for x in parrotgreet)):
					if (random.randrange(1,100) < 6):
						ricebot.send_animation(chat_id, "CgADAQADPQADtY9QRi3NGeEEAmLKAg", reply_to_message_id=msg_id)
					else:
						ricebot.send_animation(chat_id, random.choice(parrotgif), reply_to_message_id=msg_id)
				#assumptions autoreply
				elif (any(x in msg_text for x in assumptgreet)):
					time.sleep(1)			
					ricebot.send_message(chat_id, "Di ako yun", parse_mode="Markdown", disable_web_page_preview=None, disable_notification=True, reply_to_message_id=msg_id)
				#autoreply for genie ferdz gif
				elif (("genie" in msg_split or "happy" in msg_split) and ("ferdz" in msg_split or "ferds" in msg_split)):
					if searchinString(ferdzgreet, msg_text, searchparam=r"(\S+) ferdz"):
						ricebot.send_animation(chat_id, genieferdzgif)
				#autoreply for happy jake gif
				elif ("happy" in msg_split and "jake" in msg_split):
					if searchinString(jakegreet, msg_text, searchparam=r"(\S+) jake"):
						ricebot.send_animation(chat_id, jakegif[0])
				#autoreply for thick thighs
				elif (any(x in msg_split for x in tikigreet) and "thigh" in msg_text):
					if searchinString(tikigreet, msg_text, searchparam=r"(\S+) thigh"):
						ricebot.forward_message(chat_id, -1001255652659, 1496)
				#autoreply for toasties
				elif ("toasties" in msg_split and random.randint(0, 1)):
					ricebot.send_animation(chat_id, toastiesgif[0], reply_to_message_id=msg_id)
			elif (update.message.new_chat_members):
				ricebot.send_message(chat_id, "<code>Hi! Welcome to rph tele! As part of catfish verification standard procedures, we ask for a selfie of you with a tabo (tabofie) and a tinidor (tinidorfie). Have fun and stay fake!</code>", parse_mode="HTML")
			elif (anm_id and (anm_id == "CgADBQADIQAD1PpYV9Q8SLVB8kHHAg" or anm_id == "CgADBQADCQAD2MkBV-93jXgFs7gBAg")):
				if (leichance):
					ricebot.send_sticker(chat_id, random.choice(leisticker), reply_to_message_id=msg_id)
				else :
					ricebot.send_animation(chat_id, random.choice(leigif), reply_to_message_id=msg_id)
				

	
		#non-gc specific autoreply
		#send greetings
		if (msg_text):
			if (user_id == 456128183 and "hi" in msg_split):
				ricebot.send_message(chat_id, "<code>Negative</code>", parse_mode="HTML", reply_to_message_id=msg_id)
			elif ((user_id == 339707076 or user_id == 574787216) and (any(x in msg_split for x in justgreet))):
				ricebot.send_message(chat_id, "<code>Pass</code>", parse_mode="HTML")
			elif (angerychance and msg_text == "hi rice"):
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
			
def cronjob(bot, job):
	bot.send_photo(-1001043875036, "AgADBQADVagxG9cuOVfXq7usGDCFAsZo3jIABCF2Vg7uGe3afUIAAgI")
	bot.send_message(-1001255652659, "CRON JOB ACTIVATED")

def main():
	updater = telegram.ext.Updater(os.environ["BOT_TOKEN"])
	dp = updater.dispatcher
	jq = updater.job_queue
	# jqtwo = updater.job_queue

	dp.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.all, handle))
	
	jerathensone = jq.run_daily(cronjob, datetime.time(17,1,0,0))
	jerathensone.enabled = True
	updater.start_polling()

	updater.idle()

if __name__ == "__main__":
    main()

#Credits to the Python Telegram Bot team for the wonderful API and examples