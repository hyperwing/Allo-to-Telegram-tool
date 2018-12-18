from os import listdir
from os.path import isfile, join
import telebot

#indices for the csv
date = 0,
convo_name = 1
convo_id =2
sender = 3
message_type = 4
message_content = 5

APItoken = '758991141:AAHmbVvfq3zFB-QWwIDhqn9FTEQ45xF1WR8'
bot = telebot.TeleBot(APItoken)
print ('starting tool')

#directory path
myPath = r"D:\Users\futbo\Documents\GitHub\Allo-to-Telegram-tool\alloCSV"

fileList = [f for f in listdir(myPath) if isfile(join(myPath, f))]

conversationNames = []
conversationData ={}


def file_processing(alloFile):
    print ("processing conversation ")

    #TODO check headers match
    alloFile.next()

    for row in alloFile:

        columns = row.split(',')
        # print(columns[convo_id])

        if(columns[convo_id] in conversationData):
            #list of messages in conversation
            current_convo = conversationData[columns[convo_id]]
            current_convo.append(columns[message_content])
            conversationData.update({columns[convo_id]: current_convo})
        else:
            #new conversations
            tempList = [columns[message_content]]
            conversationData.update({columns[convo_id]: tempList})

    print(conversationData)

for name in fileList:
    print (name)
    
    currentBackup = open(myPath+"\\" + name, "r")
    file_processing(currentBackup)

def telegram_writer():
    print ("begin writing")


# #starts bot
# @bot.message_handler(commands=['start', 'help'])
# def handle_start_help(message):
#     bot.send_message(message.chat.id, "Send me an Allo .csv")
#     # bot.reply_to(message, "Send me an Allo .csv")
#     pass

# @bot.message_handler(content_types=['document', 'audio'])
# def handle_docs_audio(message):
#     bot.reply_to(message, "document received, verifying validity...")
#     if(verify_csv(message.document)):
#         bot.send_message(message.chat.id, "verified")

#         bot.send_message(message.chat.id, "choose a chat")
#     else:
#         bot.send_message(message.chat.id, "invalid file")

# def verify_csv(documentToCheck):
#     mimeType = documentToCheck.mime_type
#     print("MIME type: "+mimeType)
#     return mimeType == "text/csv"
    

# def generate_conversations(alloCSV):
    


# bot.polling()