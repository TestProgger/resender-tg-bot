# -*- coding: utf-8 -*-
import config
import telebot
from telebot import types
import hashlib
import requests
from misc import file_put_content , init_bot_folders
import os
import logging

bot = telebot.TeleBot(config.token)
init_bot_folders()

logging.basicConfig(
	level=logging.DEBUG,
	filename=('bot_logs.log'),
	format=('[%(asctime)s] %(levelname)-8s %(message)s')
)


@bot.message_handler(commands=["start"])
def start(message):
	bot.send_message(message.chat.id, 'Hello. \n\n Write /help fro help.')


@bot.message_handler(commands=["help"])
def help(message):
	bot.send_message(message.chat.id, 'Help message😈')


@bot.message_handler(content_types=["text"])
def messages(message):
	if int(message.chat.id) == int(config.owner):
		try:
			chatId=message.text.split(': ')[0]
			text=message.text.split(': ')[1]
			bot.send_message(chatId, text)
		except:
			pass
	else:
		bot.send_message(config.owner, str(message.chat.id) + ': ' + message.text)	
		bot.send_message(message.chat.id, '%s, wait please 👍'%message.chat.username)


@bot.message_handler(content_types=["photo" , "video" , "document" , "audio" , "voice"])
def attachment_handler(message):
	content_type = message.content_type
	chat_id = message.chat.id
	user_name = message.chat.username

	if content_type == "photo":
		attachment_id = message.photo.file_id
		attachment_file_name = os.urandom(8).hex() + ".jpg"
		send_func = bot.send_photo

	elif content_type == "video":
		attachment_id = message.video.file_id
		attachment_file_name = message.video.file_name
		send_func = bot.send_video

	elif content_type == "document":
		attachment_id = message.document.file_id
		attachment_file_name = message.document.file_name
		send_func = bot.send_document

	elif content_type == "audio":
		attachment_id = message.audio.file_id
		attachment_file_name = os.urandom(8).hex() + ".mp3"
		send_func = bot.send_audio

	elif content_type == "voice":
		attachment_id = message.voice.file_id
		attachment_file_name = os.urandom(8).hex() + ".mp3"
		send_func = bot.send_voice
	
	attachment_url = bot.get_file_url(attachment_id)
	response = requests.get(attachment_url)

	try:
		file_put_content(response.content , attachment_file_name , content_type+"s")
	except Exception:
		logging.error(f"Файл {attachment_file_name} не сохранен") 
		bot.send_message(config.owner , f"Не удалось сохранить файл {attachment_file_name}")
		bot.send_message(message.chat.id , f"Не удалось сохранить файл {attachment_file_name}")
	else:
		bot.send_message(config.owner , f"[USERNAME][CHAT ID][FILENAME]: {user_name} | {chat_id} | {attachment_file_name}")
		
		full_path = config.attachments_folder + content_type+"s/" + attachment_file_name
		
		file_descriptor = open( full_path , 'rb')

		send_func(config.owner , file_descriptor)
		file_descriptor.close()
		if not config.persist_files:
			os.remove(full_path)
			logging.info(f"[USERNAME][FILENAME] : {user_name} | {attachment_file_name}  DELETED")
		logging.info(f"[USERNAME][CHAT ID][FILENAME][CONTENT TYPE] : {user_name} | {chat_id} | {attachment_file_name} | {content_type}")


if __name__ == '__main__':
	bot.polling(none_stop = True)
