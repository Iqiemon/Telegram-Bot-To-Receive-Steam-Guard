from telegram.ext import Updater
updater = Updater(token='YOURBOTTOKEN', use_context=True)
dispatcher = updater.dispatcher

import smtplib
import time
import imaplib
import email
import traceback 
# -------------------------------------------------
#
# Utility to read email from Gmail Using Python
#
# ------------------------------------------------
ORG_EMAIL = "@gmail.com" 
FROM_EMAIL = "YOUREMAIL" + ORG_EMAIL 
FROM_PWD = "YOURPASSWORD" 
SMTP_SERVER = "imap.gmail.com" 
SMTP_PORT = 993


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome !")

from telegram.ext import CommandHandler
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
updater.start_polling()


def sg(update, context):
    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL,FROM_PWD)
        mail.select('inbox')

        data = mail.search(None, 'ALL')
        mail_ids = data[1]
        id_list = mail_ids[0].split()   
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])

        
        data = mail.fetch(str(latest_email_id), '(RFC822)' )
        for response_part in data:
            arr = response_part[0]
            if isinstance(arr, tuple):
                msg = email.message_from_string(str(arr[1],'utf-8'))
                email_from = msg['from']
                listW = list(email_from.split(" "))
                try:
                    #print(listW[2])
                    if listW[2] != "<noreply@steampowered.com>":
                        update.message.reply_text("Please try to request again.")
                        exit()
                except:
                    update.message.reply_text("Please resend the steam guard code again.")
                
                if msg.is_multipart():
                # iterate over email parts
                    for part in msg.walk():
                        # extract content type of email
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        try:
                            # get the email body
                            body = part.get_payload(decode=True).decode()
                        except:
                            pass
                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            # print text/plain emails and skip attachments
                            list1 = list(body.split(" ")) 
                            #print(list1) 
                            #print(list1[13])
                            try:
                                wiwu = list1[13]
                                list2 = list(wiwu.split("\n"))
                                #print(list2)
                                codewithr = list2[2]
                                #print(body)
                                update.message.reply_text(codewithr)
                                #print(codewithr)
                            except:
                                update.message.reply_text("Failed.")
                                
                        
        

    except Exception as e:
        traceback.print_exc() 
        print(str(e))
    
    
from telegram.ext import CommandHandler
sg_handler = CommandHandler('sg', sg)
dispatcher.add_handler(sg_handler)

