import pymongo


# 连接数据库
def connect_mongodb():
    return pymongo.MongoClient(host="localhost", port=27017)


# 取消连接
def disconnect_mongodb(client):
    client.close()


# 选择email数据库
def choose_database(client):
    return client.email


# 连接email中用户对应的数据表
def choose_user(db, username):
    user = db["{}".format(username)]
    return user


# 插入一条数据
def insert_one(user, email):
    user.insert_one(email)


# 插入多条数据
def insert_many(user, email_list):
    user.insert_many(email_list)


# 查找一条数据
def find_one(user):
    x = user.find_one()
    print(x)


# 查找数据--发信人
def find_by_addresser(user, addresser):
    results = user.find({"from": "{}".format(addresser)})
    for result in results:
        print(result)
    return results


# 查找数据--收信人
def find_by_addressee(user, addressee):
    results = user.find({"to": "{}".format(addressee)})
    for result in results:
        print(result)
    return results


# 查找数据--抄送
def find_by_copy(user, copy):
    results = user.find({"cc": "{}".format(copy)})
    for result in results:
        print(result)
    return results


# new_emails = []
# new_email_1 = myEmail.set_email("测试1", "xxx@xxx.com", "xxx@xxx.com", "xxx@xxx.com", "测试邮件1")
# new_email_2 = myEmail.set_email("测试2", "xxx@xxx.com", "xxx@xxx.com", "xxx@xxx.com", "测试邮件2")
# new_emails.append(new_email_1)
# new_emails.append(new_email_2)
# myClient = connect_mongodb()
# emaildb = choose_database(myClient)
# user = choose_user(emaildb, "demo")
# insert_many(user, new_emails)
# disconnect_mongodb(myClient)
