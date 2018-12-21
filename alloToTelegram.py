from os import listdir
from os.path import isfile, join
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import urllib2
#indices for the csv
date = 0,
convo_name = 1
convo_id =2
sender = 3
message_type = 4
message_content = 5

telegram_user_id = 0
bot_chat_id=0
chat_to_send = 0


APItoken = '758991141:AAHmbVvfq3zFB-QWwIDhqn9FTEQ45xF1WR8'
bot = telebot.TeleBot(APItoken)
print ('starting tool')

class AlloMessage:
    def __init__(self, ts, name, id, sender, message_type, message_content):
        self.ts = ts
        self.name = name
        self.id = id
        self.sender = sender
        self.message_type = message_type
        self.message_content = message_content

#directory path
# myPath = r"D:\Users\futbo\Documents\GitHub\Allo-to-Telegram-tool\alloCSV"

# fileList = [f for f in listdir(myPath) if isfile(join(myPath, f))]

conversationNames = []
conversationData ={}


def file_processing(alloFile):
    global conversationData
    global conversationNames
    print ("processing conversation ")

    #TODO check headers match
    alloFile.next()

    for row in alloFile:

        columns = row.split(',')
        # print(columns[convo_id])
        currentMessage = AlloMessage(columns[0],columns[1], columns[2], columns[3], columns[4], columns[5])


        if(currentMessage.id in conversationData):
            current_convo_list = conversationData[currentMessage.id]
            current_convo_list.append(currentMessage)
            conversationData.update({columns[convo_id]: current_convo_list})
        else:
            #new conversations
            conversationNames.append(columns[convo_name])

            tempList = [currentMessage]
            conversationData.update({currentMessage.id: tempList})

    print(conversationNames)
    # print(conversationData.get("7y0SfeN7lCuq0GFF5UsMYZofIjJ7LrvPvsePVWSv450=")[0].message_type)


#starts bot
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    global bot_chat_id 

    bot_chat_id= message.chat.id

    print("chat_id: "+ str(bot_chat_id))

    bot.send_message(bot_chat_id, "Send me an Allo .csv")
    pass

@bot.message_handler(content_types=['document', 'audio'])
def handle_docs_audio(message):
    global APItoken
    print("chat_id: "+ str(bot_chat_id))

    bot.reply_to(message, "document received, verifying validity...")
    if(verify_csv(message.document)):
        bot.send_message(bot_chat_id, "verified")

        target_url = "https://api.telegram.org/file/bot"+ str(APItoken)+"/"+bot.get_file(message.document.file_id).file_path

        print(target_url)
        data = urllib2.urlopen(target_url)
        file_processing(data)

        handle_convo(message)

    else:
        bot.send_message(bot_chat_id, "invalid file, send another")

@bot.message_handler(content_types=['contact'])
def handle_contacts(message):
    global chat_to_send

    bot.send_message(bot_chat_id, "contact received.")
    
    try:
        chat_to_send = message.contact.user_id
        print("user_id:" +str(chat_to_send))
        bot.send_message(bot_chat_id, "user id:" +str(chat_to_send))
        pass
    except:
        print("invalid contact")
        bot.send_message(bot_chat_id, "Contact does not have a telegram id, try another")
        pass

    

    #TODO display chats to import
    

def verify_csv(documentToCheck):
    mimeType = documentToCheck.mime_type
    print("MIME type: "+mimeType)
    return mimeType == "text/csv"
        



def gen_markup():
    markup = InlineKeyboardMarkup()
    print("convo length: "+str(conversationNames.count))
    markup.row_width = conversationNames.count
    for name in conversationNames:
        markup.add(InlineKeyboardButton("Send contact", callback_data= name))
    return markup

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):

    for conversation in conversationNames:
        if call.data == conversation:
            bot.answer_callback_query(call.id, conversation+"chosen")
            print("choice: "+conversation)


    
    # if call.data == "cb_contact":
    #     bot.answer_callback_query(call.id, "send me the contact to add the conversation to")
    #     print("choice:contact")

    # elif call.data == "cb_id":
    #     bot.answer_callback_query(call.id, "send the telegram id of the conversation")
    #     print("choice:telegramid")


@bot.message_handler(func=lambda message: True)
def handle_convo(message):
    bot.send_message(bot_chat_id, "choose a chat method", reply_markup=gen_markup())



bot.polling()