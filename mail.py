import smtplib
from email.message import EmailMessage

def sendEmail(emailTo, sub, msg):
    gmailUser = "webappfeit@gmail.com"
    gmailPassword = "webAppTest44$"

    sendMessage = EmailMessage()
    sendMessage.set_content(msg)
    sendMessage['Subject'] = sub
    sendMessage['From'] = gmailUser
    sendMessage['To'] = emailTo

    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(gmailUser, gmailPassword)
        smtp_server.send_message(sendMessage)
        smtp_server.close()
    except Exception as ex:
        print ("Something went wrong!!\n",ex)
