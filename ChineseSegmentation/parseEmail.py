import imaplib
import email
from email.header import decode_header
from ChineseSegmentation import JB, myEmail, FileController as fc, MongoDB
import os
import chardet


def decode_str(self, s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value


# 判断邮件格式
def guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        for part in msg.walk():
            content_type = part.get("Content-Type", "").lower()
            if content_type.find("charset=") >= 0:
                break
        pos = content_type.find('charset=')
        if pos >= 0:
            # 去掉尾部不代表编码的字段
            charset = content_type[pos + 8:].strip('; format=flowed; delsp=yes')
    return charset


# 解析邮件首部
def parse_header(message):
    subStr = message.get("subject")
    if subStr is None:
        subject = "无主题"
    else:
        dh = decode_header(subStr)
        subinfo = dh[0][0]
        subcode = dh[0][1]
        if not subcode:
            subject = subinfo
        else:
            if isinstance(subinfo, bytes):
                subject = subinfo.decode(subcode, errors="ignore")
            else:
                subject = subinfo
    # 主题
    # print(subject)
    # 发件人
    addresser = email.utils.parseaddr(message.get("from"))[1]
    # print("From:", addresser)
    # 收件人
    addressee = email.utils.parseaddr(message.get('to'))[1]
    # print("To:", addressee)
    # 抄送人
    copy = email.utils.parseaddr(message.get('cc'))[1]
    # print("Cc:", copy)
    return subject, addresser, addressee, copy


# 解析邮件信体
def parse_body(message):
    # 循环信件中的每一个mime的数据块
    for part in message.walk():
        # 判断是否是一个multipart，如果是，里面的数据是一个message列表
        if not part.is_multipart():
            charset = part.get_charset()
            # print 'charset: ', charset
            content_type = part.get_content_type()
            name = part.get_param("name")  # 如果是附件，这里就会取出附件的文件名
            if name:
                print("This is an enclosure.")
                # 有附件
                # 下面的三行代码只是为了解码，像=?gbk?Q?=CF=E0=C6=AC.rar?=这样的文件名
                fdh = decode_header(name)
                fname = fdh[0][0]
                print("附件名:", fname)
                # attach_data = par.get_payload(decode=True) #　解码出附件数据，然后存储到文件中
                # try:
                #     f = open(fname, 'wb') #注意一定要用wb来打开文件，因为附件一般都是二进制文件
                # except:
                #     print '附件名有非法字符，自动换一个'
                #     f = open('aaaa', 'wb')
                # f.write(attach_data)
                # f.close()
            else:
                # 不是附件，是正文
                if content_type == "text/plain":
                    content = part.get_payload(decode=True)
                    charset = guess_charset(message)
                    print(charset)
                    # charset = "utf-8"
                    if charset:
                        content = content.decode(charset).encode("utf-8")
                        # print("This is a text:", content)
                    return content
                else:
                    print("This is a html:", content_type)
                    html = part.get_payload(decode=True)
                    coding = chardet.detect(html)["encoding"]
                    print(html.decode("gbk", errors="ignore"))


# 获取邮件
def get_mail(host, username, password, port=993):  # 端口自行选择空闲端口
    try:
        service = imaplib.IMAP4_SSL(host, port)
    except Exception:
        service = imaplib.IMAP4(host, port)
    service.login(username, password)
    # 邮箱中的文件夹，默认为'INBOX'
    service.select()
    # 搜索匹配邮件，第一个参数是字符集，None默认就是ASCII编码，第二个参数是查询条件，这里的ALL就是查找全部，格式为"(FROM "xx@xxx.com")"
    type, data = service.search(None, "ALL")
    # 邮件列表，使用空格分割得到邮件索引
    msgList = data[0].split()
    # 最新邮件，第0封邮件为最早的一封邮件
    latest = msgList[len(msgList) - 1]
    type, datas = service.fetch(latest, '(RFC822)')
    text = datas[0][1].decode("utf8")
    message = email.message_from_string(text)
    # print(message)
    title, addresser, addressee, copy = parse_header(message)
    content = parse_body(message)
    service.close()
    service.logout()
    return title, addresser, addressee, copy, content


# 读取中文邮件集
def get_emails(db):
    path = "trec06c/data"
    dirs = os.listdir(path)
    for dir in dirs:
        user = MongoDB.choose_user(db, dir)
        emails = os.listdir(path + "/" + dir)
        new_emails = []
        for e in emails:
            email_path = path + "/" + dir + "/" + e
            print(email_path)
            text = fc.get_text(email_path)
            msg = email.message_from_string(text)
            title, addresser, addressee, copy = parse_header(msg)
            content = parse_body(msg)
            content = JB.participle_text(content)
            new_email = myEmail.set_email(title, addresser, addressee, copy, content)
            new_emails.append(new_email)

        # mongodb.insert_many(user, new_emails)

# # 连接邮箱
# host = "imap.qq.com"
# username = "1351446867@qq.com"
# password = "vyrfplitjeuohgji"
# title, addresser, addressee, copy, content = get_mail(host, username, password)
# # 中文分词
# content = JB.participle_text(content)
# # 添加至MongoDB数据库
# new_email = myEmail.set_email(title, addresser, addressee, copy, content)
# myClient = mongodb.connect_mongodb()
# emaildb = mongodb.choose_database(myClient)
# user = mongodb.choose_user(emaildb, "demo")
# mongodb.insert_one(user, new_email)
# mongodb.disconnect_mongodb(myClient)