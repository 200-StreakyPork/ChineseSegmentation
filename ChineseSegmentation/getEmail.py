import os
import email
from ChineseSegmentation import JB, parseEmail as pe, myEmail, FileController as fc, MongoDB
import re


def get_content(email_text):
    email_content = ""
    pos = max(email_text.find("X-MimeOLE"), email_text.find("X-Mailer"), email_text.find("Content-Type"), email_text.find("boundary"),
              email_text.find("charset"),email_text.find("Disposition-Notification-To"))
    i = 0
    for line in email_text[pos:].splitlines(keepends=True):
        line = line.replace(" ","")
        if i > 0:
            email_content += line
        i += 1
    return email_content


def get_emails(db):
    path = "trec06c/data"
    dirs = os.listdir(path)
    new_emails = []
    i = 0
    for dir in dirs:
        new_emails.clear()
        user = MongoDB.choose_user(db, dir)
        emails = os.listdir(path + "/" + dir)
        j = 0
        for e in emails:
            print(dir + "/" + e, end=" ")
            text = fc.get_text(path + "/" + dir + "/" + e)
            print("邮件长度:", len(text))
            # 打印某封邮件内容
            j = j + 1
            msg = email.message_from_string(text)
            title, addresser, addressee, copy = pe.parse_header(msg)
            content = get_content(text)
            doc = re.split('。|；|·|！|？|\n', content)
            doc = list(filter(None, doc))
            split = []
            for i in range(len(doc)):
                split.append(JB.participle_text(doc[i]))
                doc[i] = doc[i] + "。"
            # print(split)
            new_email = myEmail.set_email(title, addresser, addressee, copy, doc, split)
            new_emails.append(new_email)
        i = i + 1
        # MongoDB.insert_many(user, new_emails)


if __name__ == '__main__':
    myClient = MongoDB.connect_mongodb()
    emaildb = MongoDB.choose_database(myClient)
    get_emails(emaildb)
    MongoDB.disconnect_mongodb(myClient)
