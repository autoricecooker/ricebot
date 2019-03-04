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
from telegram.ext.dispatcher import run_async

#big ol' blob of variables

#wwgc = os.environ["WW_GC"]
testGCID = int(os.environ["TEST_GC"])
prodGCID = int(os.environ["PROD_GC"])
cebGCID = int(os.environ["CEB_GC"])
sadgreet = ["spill", "trip", "eat", "eat you", "bite", "bite you","tips", "tips over"]
killgreet = ["unplug", "unplug you", "kill", "kill you", "rip", "destroy", "hate", "hate you"]
randomgreet = ["Hello", "Hi", "Greetings", "Good day", "How are ya?", "Yes", "No", "What's up?"]
assumptgreet = ["akala ko si rice", "akala ko si ricecooker", "akala ko si @ricecooker", "kala ko si rice", "kala ko si @ricecooker", "kala ko si ricecooker", "ikaw ba yan rice", "kaw ba yan rice", "rice ikaw ba yan", "rice kaw ba yan", "ikaw ba yan @ricecooker", "si rice ba yun", "si @ricecooker ba yun", "si rice ba un", "si @ricecooker ba un", "is that @ricecooker"]
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
weebgreet = ["anime was a mistake", "weeb shit", "fucking weeb", "fuckin weeb", "fucking weeaboo", "fuckin weeaboo", "damn weeb", "damn weeaboo"]
leisticker = ["CAADBQADIQEAAiO4mBCSjVKUWk7MNwI", "CAADBQADHAEAAiO4mBCeaC0LYAlkowI", "CAADBQADIAEAAiO4mBD3UdIBPEO6WwI", "CAADBQADGwEAAiO4mBC51PR572t9EgI", "CAADBQADHwEAAiO4mBBJWiwq_cjWdQI", "CAADBQADHgEAAiO4mBBMQuYcpcSX2AI"]
#leigif = ["CgADBQADEAADS754Vj0cIPOA5fAWAg", "CgADBQADFQADDHrhVXLWPyi-fVESAg", "CgADBQADEQADNNrpV0yGyX3SyadcAg", "CgADBQADHwADYlzxVd_bBWXEyqHUAg"]
leigif = ["CgADBQADEQADNNrpV_JyDVwU2d1rAg", "CgADBQADFQADDHrhVeaTS0bvbyRWAg", "CgADBQADEAADS754Vha1dmKytEvNAg", "CgADBQADHwADYlzxVfOzb9cCUkuqAg"]
#stressgif = ["CgADBQADNgAD1k_RVO3goPd_-i6UAg", "CgADBQADeAADXqhQVB4H-vGgquQBAg", "CgADBQADagADIQNZVQwwt6F0hhTnAg", "CgADBQADMQADSQ5QVWEW6SjSG4KYAg"]
stressgif = ["CgADBQADeAADXqhQVCksGu6IfbQMAg", "CgADBQADMQADSQ5QVUn-yBLRrDvBAg", "CgADBQADagADIQNZVdJEKrwDU24lAg", "CgADBQADNgAD1k_RVFSZibSpxmu4Ag", "CgADBQADFgADjGnIVUDk7DZAN-6XAg", "CgADBQADAwADXbeJVIa-vUgkTDSCAg"]
blessgif =["CgADBQADQwADUt_RVJbf7QgSjFMQAg"]
#genieferdzgif = "CgADBQADEgADUT_BVphVHpXa9x1UAg"
genieferdzgif = "CgADBQADEgADUT_BVqvCsq_FYDT-Ag"
#unpluggif = "CgADBQADNwADtjzaDem_pNtFz2CxAg"
unpluggif = "CgADBQADNwADtjzaDXzFsIuaINkHAg"
#landigif = ["CgADBQADKQADvG2JViq33V_DvoF9Ag", "CgADBQADHQAD6QuQVwZwVsITdN6hAg"]
landigif = ["CgADBQADHQAD6QuQV_mxPdwxj0s2Ag", "CgADBQADKQADvG2JVi4mEJDnylDvAg"]
louisegif = ["CgADBQADHAADVMqxV2iqwCWWKYXRAg", "CgADBQADRQADggs5VTtpVvYfIcqBAg", "CgADBQADGwADwI9BVYEBhY4qglXKAg", "CgADBQADWwADfhjQVy2VyBHiS3kWAg", "CgADBQADXQADlN5hVIkXruw21LEsAg"]
toastiesgif = ["CgADBQADLwADv4dBVFVtZJ9jdSwFAg"]
jakegif = ["CgADBQADBwADGIgpVpF8EgH6Mc-9Ag", "CgADBQADCgADuNkwVpThek7KAmXsAg"]
drunkpic = ["AgADBQADOagxGxB_aVZNfo9wNUvyYvGl1jIABMOR93PzURnicEMDAAEC", "AgADBQADOqgxGxB_aVav5vKmhLduCGqk1jIABOQDiHpGpExCJUMDAAEC", "AgADBQADkagxG6Oe8FbPeySNTsva1S5U2zIABHbiq4wGrTTHhxABAAEC", "AgADBQADYKgxGzx76FYspQoUVI_orGFh2zIABPdENNUjOZ6HMQoBAAEC", "AgADBQADyagxG3vgQFfzWyPyZwABhDpToNYyAARIZLO6JHE6rwHyAwABAg", "AgADBQADyqgxG3vgQFdnwo6v0N37ltKu1jIABImnO1LEv_hLsvgDAAEC", "AgADBQADy6gxG3vgQFdhN5CqLNBoaZps3jIABIzvbj8OdXrYa0EAAgI", "AgADBQADzKgxG3vgQFd0wYPinyYN3Zhq2zIABNpbg4ad52tcN0oBAAEC"]
parrotgif = ["CgADBQADLQADkxKZVrE-Wx30uXiNAg", "CgADBQADWAADeL-YVnw3sjCV8aeLAg", "CgADBQADMAADkxKZVp3RsGgriq4TAg", "CgADBQADWQADeL-YVsV0J7Zx1H3-Ag", "CgADBQADLwADamEJVwABfmqsGruuIAI", "CgADBQADRQADxKcIVnp4XIZkwZhFAg", "CgADBQADRgADxKcIVtBU7hnUu1vtAg", "CgADBQADSgADFBMRVvS30XYL8EfxAg", "CgADBQADTQADxKcQVqmmDa3r6kUvAg"]
ftwentygif = ["CgADBQADZwADC8sAAVdyPHOcrabSlAI", "CgADBQADBQADilkQVlcE7H79KrlZAg"]
flandersgif = ["CgADBAADOQADvho0UUaTNwGy6fWJAg"]
weebgif = ["CgADBQADOwADyE_wVe3mk7g8DJnwAg", "CgADBQADWAAD5XgIVd4wMCz9ESrCAg"]
prayerpic = "AgADBQADbagxG4ocsVfyRzCWKWz83cBQ9jIABFnbxMn-gKxBdGgBAAEC"
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
@run_async
def delmsg(bot, job):
	msg = job.context
	msg.delete()

@run_async
def pmhandle(update: telegram.Update, context: telegram.ext.CallbackContext):
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
			if (angerychance and msg_text == "hi rice"):
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

@run_async
def testGChandle(update: telegram.Update, context: telegram.ext.CallbackContext):
	#Initialize variables
	ricebot = context.bot
	msg_text = None
	msg_split = None
	anm_id = None
	reply_user_id = None
	fwd_user_id = None
	sticker_id = None
	contxt = None
	landichance = random.randint(1,6) % 5
	atomchance = random.randint(1,6) % 6
	leichance = random.randint(1,3) % 3
	global testexpr
	#Check if message has content
	if (update.message):

		chat_id = update.message.chat_id
		msg_id = update.message.message_id
		user_id = update.message.from_user.id

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

		#Send motd when new members are added
		if (update.message.new_chat_members):
			ricebot.send_message(chat_id, "<code>All contents/events in this group chat are confidential. Disclosure is prohibited</code>", parse_mode="HTML")
		#Check if message is text
		if (update.message.text):
			msg_text = update.message.text.lower()
			msg_split = msg_text.split()	
			if (msg_text == "hipo"):
				if (landichance):
					ricebot.send_document(chat_id, landigif[0], caption=None, parse_mode="Markdown", disable_notification=True, reply_to_message_id=msg_id)
				else:
					ricebot.send_document(chat_id, landigif[1], caption=None, parse_mode="Markdown", disable_notification=True, reply_to_message_id=msg_id)
			elif (msg_text == "jerathens"):
				contxt = ricebot.send_photo(chat_id, "AgADBQADVagxG9cuOVfXq7usGDCFAsZo3jIABCF2Vg7uGe3afUIAAgI")
				testexpr.run_once(delmsg, 3, context=contxt)
			#replace string test
			# elif ("pass" in msg_split):
			# 	print ("pass keyword found")
			# 	print (msg_text.replace("pass", "patawad"))
			# 	ricebot.send_message(chat_id, msg_text.replace("pass", "patawad"), reply_to_message_id=msg_id)
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
			elif(any(x in msg_text for x in weebgreet)):
				ricebot.send_animation(chat_id, random.choice(weebgif))
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
				
		if (reply_user_id):
			ricebot.send_message(chat_id,"Reply user ID: \n" + str(reply_user_id))
		if (anm_id):
			ricebot.send_message(chat_id, "GIF ID: \n" + anm_id)
		if (sticker_id):
			ricebot.send_message(chat_id, "Sticker ID: \n" + sticker_id)
		if (update.message.photo):
			ricebot.send_message(chat_id, "Photo File ID: \n" + update.message.photo[-1].file_id)
		# if (update.message.document):
		# 	ricebot.send_message(chat_id, str(update.message.document.file_id))
		
		#Check if message is forwarded
		if (fwd_user_id):
			ricebot.send_message(chat_id, "Forwarded message user ID: " + str(fwd_user_id))
		
@run_async
def prodGChandle(update: telegram.Update, context: telegram.ext.CallbackContext):
	#Initialize variables
	ricebot = context.bot
	msg_text = None
	msg_split = None
	anm_id = None
	reply_user_id = None
	landichance = random.randint(1,6) % 5
	# angerychance = random.randint(1,4) % 4
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
			#autoreply for landi mo 
			elif (update.message.reply_to_message and msg_text == "landi mo" and user_id != reply_user_id):
				if (landichance):
					ricebot.send_animation(chat_id, landigif[0], caption=None, parse_mode="Markdown", disable_notification=True, reply_to_message_id=reply_msg_id)
				else:
					ricebot.send_animation(chat_id, landigif[1], caption=None, parse_mode="Markdown", disable_notification=True, reply_to_message_id=reply_msg_id)
			# elif ("pass" in msg_split):
			# 	print ("pass keyword found")
			# 	print (msg_text.replace("pass", "patawad"))
			# 	ricebot.send_message(chat_id, msg_text.replace("pass", "patawad"), reply_to_message_id=msg_id)
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
			#autoreply for weaboos
			elif(any(x in msg_text for x in weebgreet)):
				ricebot.send_animation(chat_id, random.choice(weebgif))
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
			ricebot.send_message(chat_id, "<code>Hi! Welcome to rph tele! \nAs part of catfish verification standard procedures, we ask for a selfie of you with a tabo (tabofie) and a tinidor (tinidorfie). \nHave fun and stay fake!</code>", parse_mode="HTML")
		elif (anm_id and (anm_id == "CgADBQADIQAD1PpYV9Q8SLVB8kHHAg" or anm_id == "CgADBQADCQAD2MkBV-93jXgFs7gBAg")):
			if (leichance):
				ricebot.send_sticker(chat_id, random.choice(leisticker), reply_to_message_id=msg_id)
			else :
				ricebot.send_animation(chat_id, random.choice(leigif), reply_to_message_id=msg_id)

@run_async
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
		user_id = update.message.from_user.id

		#Get original user ID from reply message
		if (update.message.reply_to_message):
			reply_user_id = update.message.reply_to_message.from_user.id
			reply_msg_id = update.message.reply_to_message.message_id

		if (update.message.text):
			msg_text = update.message.text.lower()
			msg_split = msg_text.split()
			if(any(x in msg_text for x in weebgreet)):
				ricebot.send_animation(chat_id, random.choice(weebgif))
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
			ricebot.send_message(chat_id, "<code>Welcome to r/Sugbo Telegram!\n\nAs part of our verification, kindly post a selfie holding a silhig tukog or a stapler.\n\nHave fun!</code>", parse_mode="HTML")

def cronjobdos(bot,job):
	bot.send_message(testGCID, "CRON JOB 420 ACTIVATED")
	bot.send_animation(prodGCID, random.choice(ftwentygif))


def cronjobpray(bot,job):
	bot.send_photo(testGCID, prayerpic)

def main():
	updater = telegram.ext.Updater(os.environ["BOT_TOKEN"], use_context=True, workers=8)
	dp = updater.dispatcher
	rm = updater.job_queue
	global testexpr
	global prodexpr
	testexpr = updater.job_queue
	prodexpr = updater.job_queue

	dp.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.chat(testGCID), testGChandle))
	dp.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.chat(prodGCID), prodGChandle))
	dp.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.chat(cebGCID), cebGChandle))
	dp.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.private, pmhandle))

	# fourtwenty = rm.run_daily(cronjobdos, datetime.time(8,20,15,0))
	# fourtwenty.enabled = False
	
	prayersched = rm.run_daily(cronjobpray, datetime.time(7,0,3,0))
	prayersched.enabled = True


	updater.start_polling()

	updater.idle()

if __name__ == "__main__":
    main()

#Credits to the Python Telegram Bot team for the wonderful API and examples