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

#user interacting with bot id
telegram_user_id = 0
bot_chat_id=0
chat_to_send = 0

#allo id number
selectedConversation = ""
#all allo ids in csv
allo_ids =[]

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
            #print("Adding "+currentMessage.name)
            #print("ID: "+ currentMessage.id)
            #print("ID: "+ currentMessage.message_content)
            current_convo_list = conversationData[currentMessage.id]
            current_convo_list.append(currentMessage)
            conversationData.update({columns[convo_id]: current_convo_list})
        else:
            #new conversations
            conversationNames.append(columns[convo_name])

            tempList = [currentMessage]
            conversationData.update({currentMessage.id: tempList})

    #print(conversationNames)
    #print(conversationData)
    # print(conversationData.get("7y0SfeN7lCuq0GFF5UsMYZofIjJ7LrvPvsePVWSv450=")[0].message_type)


#Sends messages to the chat
def send_to_chat():
    global selectedConversation
    print("sending to "+conversationNames[convo_name])
    print (selectedConversation)
    print(conversationData[selectedConversation][0].name)



    for convo in conversationData[selectedConversation]:
        #for message in convo_list:
        senderTxt = convo.sender[13:]

        print(convo.ts+"\n"+senderTxt+":\n"+convo.message_content)
        bot.send_message(bot_chat_id, convo.ts+"\n"+senderTxt+":\n"+convo.message_content)
    print("convo imported")
    bot.send_message(bot_chat_id, "finished importing")

#starts bot
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    global bot_chat_id 

    bot_chat_id= message.chat.id

    print("chat_id: "+ str(bot_chat_id))

    bot.send_message(bot_chat_id, "PM me an Allo .csv")
    pass

@bot.message_handler(commands=['transfer'])
def handle_start_transfer(message):
    bot.send_message(bot_chat_id, "beginning transfer")
    send_to_chat()

@bot.message_handler(commands=['getGroupID'])
def handle_get_group_id(message):
    chat_to_send = message.chat.id
    print("chat to send: "+str(chat_to_send))
    idStr = "ID is "+str(chat_to_send)
    bot.send_message(chat_to_send, idStr)
    

@bot.message_handler(content_types=['document', 'audio'])
def handle_docs_audio(message):
    global APItoken
    print("chat_id: "+ str(bot_chat_id))

    bot.reply_to(message, "document received, verifying validity...")
    if(verify_csv(message.document)):
        bot.send_message(bot_chat_id, "verified")
        bot.send_message(bot_chat_id, "processing file")

        target_url = "https://api.telegram.org/file/bot"+ str(APItoken)+"/"+bot.get_file(message.document.file_id).file_path

        print(target_url)
        data = urllib2.urlopen(target_url)
        file_processing(data)

        handle_convo(message)

    else:
        bot.send_message(bot_chat_id, "invalid file, send another")



# THIS IS USEFUL FOR SOME FUTURE SHIT
@bot.message_handler(content_types=['contact'])
def handle_contacts(message):
    global chat_to_send
    
    bot.send_message(bot_chat_id, "contact received.")
    
    try:
        chat_to_send = message.contact.user_id
        print("user_id:" +str(chat_to_send))
        if(chat_to_send == None):
            raise ValueError('Contact is empty')
        # bot.send_message(bot_chat_id, "user id:" +str(chat_to_send))
        
        # bot.send_message(bot_chat_id, "Allo chat :"+conversationNames[selectedConversation])
        bot.send_message(bot_chat_id, "Telegram User ID: "+ str(chat_to_send ))
        bot.send_message(bot_chat_id, "/transfer to begin messages" )
        pass
    except ValueError as err:
        print(err)
        bot.send_message(bot_chat_id, "Contact does not have a telegram id, click on the contact in Telegram and share to this chat")



def verify_csv(documentToCheck):
    mimeType = documentToCheck.mime_type
    print("MIME type: "+mimeType)
    return mimeType == "text/csv"
        



def gen_markup():
    global allo_ids
    markup = InlineKeyboardMarkup()
    print("number of convos: "+str(len(conversationNames)))

    #adds rows to the inline keyboard
    markup.row_width = len(conversationNames)

    #puts the allo ids into a global variable
    allo_ids = [len(conversationNames)]
    allo_ids.append(conversationData.keys())
    print(allo_ids)
    #allo_ids[1].reverse()
    
    # allo_index =0
    # for name in conversationNames:
    #     print("name: "+name)
    #     markup.add(InlineKeyboardButton(name, callback_data= str(allo_index)))
    #     allo_index +=1
    # return markup

    allo_index = 0
    for conversation in conversationData:
        print("name:"+ conversation)
        print(conversationData[conversation][0].name)
        markup.add(InlineKeyboardButton(conversationData[conversation][0].name, callback_data= str(allo_index)))
        allo_index +=1
    return markup

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global selectedConversation

    print("callback handler :"+call.data)
    index = int(call.data)
    for conversation in conversationNames:
        if conversationNames[index] == conversation:
            bot.answer_callback_query(call.id, conversation+" chosen")
            #first element is size
            selectedConversation = str(allo_ids[1] [index] ) 
            print("alloID: "+str(selectedConversation))
            print("choice: "+conversationNames[index])

    bot.send_message(bot_chat_id, "/transfer to start")

    # if call.data == "cb_contact":
    #     bot.answer_callback_query(call.id, "send me the contact to add the conversation to")
    #     print("choice:contact")

    # elif call.data == "cb_id":
    #     bot.answer_callback_query(call.id, "send the telegram id of the conversation")
    #     print("choice:telegramid")


@bot.message_handler(func=lambda message: True)
def handle_convo(message):
    bot.send_message(bot_chat_id, "choose a chat", reply_markup=gen_markup())



bot.polling()