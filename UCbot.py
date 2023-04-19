from fbchat import Client, log, _graphql
from fbchat.models import *
import pymongo, re
# from keep_alive import keep_alive

admins = ['100007289010328', '100083658307984', '100082754857375']

myclient = pymongo.MongoClient("mongodb+srv://UCManage:Nabilmim123@ucmanager.sa47l3e.mongodb.net/?retryWrites=true&w=majority")
mydb = myclient["UCdata"].ucdata
userdb = myclient["UCdata"].userInfo


def users():
    return [i['uid'] for i in userdb.find({})]


class ChatBot(Client):
    global mydb

    def onMessage(self, mid=None, author_id=None, message_object=None, thread_id=None, thread_type=ThreadType.USER, **kwargs):                                   
        
    
        global command, fullmsg, msg
        fullmsg = str(message_object.text)
        print(fullmsg)

        command = fullmsg.split(" ")[0].lower()
        msg = fullmsg.replace(command+" ", "")

        if command == "/adduc" and author_id in admins:
            bdt = msg.split()[0]
            if bdt not in ["80", '160', '405', '810', '1625', '161', '162', '800', '2000']:
                self.send(Message(text='Pʟᴇᴀsᴇ Sᴘᴇᴄɪғʏ Cᴏʀʀᴇᴄᴛ ʙᴅᴛ \n\nExᴀᴍᴘʟᴇ : /uc 80 <UCs>', reply_to_id=mid), thread_id=thread_id, thread_type=thread_type)
                pass
            try:
                txt = message_object.replied_to.text
            except:
                txt = msg
            ucs = re.findall('(\w{4}-\w-S-\d{8} \d{4}-\d{4}-\d{4}-\d{4})', txt)
            oldLst = mydb.find({"type":"ucs"})[0][bdt]
            newLst = list(set(oldLst + ucs))
            mydb.update_one({"type":"ucs"},{'$set':{bdt : newLst}})
            self.send(Message(text=f'Sᴜᴄᴇssғᴜʟ !!\n\nNᴇᴡ Aᴅᴅᴇᴅ 🆄︎🅲︎  :   {len(newLst)-len(oldLst)}  Pᴄs\nTᴏᴛᴀʟ {bdt}  🆄︎🅲︎   :   {len(newLst)} Pᴄs', reply_to_id=mid), thread_id=thread_id, thread_type=thread_type)

        elif command == "/signup" :
            if author_id in admins:
                if thread_type == ThreadType.USER:
                    author_id = thread_id
                elif thread_type == ThreadType.GROUP:
                    try:
                        author_id = message_object.replied_to.author
                    except:
                        self.send(Message(text="Rᴇᴘʟʏ Tᴏ Usᴇʀs Mᴇssᴀɢᴇ!", reply_to_id=mid), thread_id=thread_id, thread_type=thread_type)
                        pass
            if author_id in users():
                self.send(Message(text='Usᴇʀ Aʟʀᴇᴀᴅʏ Rᴇɢɪsᴛᴇʀᴇᴅ!.', reply_to_id=mid), thread_id=thread_id, thread_type=thread_type)

            else:
                name = client.fetchUserInfo(author_id)[author_id].name
                data = {
                        "uid" : author_id,
                        "name" : name,
                        "balance" : {"advance" : 0, 
                                    "baki":{"bakiLimit" : 0, 
                                            "due" : 0,
                                            "bakiUC" : {"80":0, "160" : 0, "405":0, "810":0, "1625" : 0, "161" : 0, "162" : 0, "800" : 0, '2000' : 0 }}
                                }
                        }
                userdb.insert_one(data)
                self.send(Message(text=f'Usᴇʀ {name} Rᴇɢɪsᴛᴇʀᴇᴅ!!. ', reply_to_id=mid), thread_id=thread_id, thread_type=thread_type)

        elif "/bakilimit" == command and author_id in admins:
            if thread_type == ThreadType.USER:
                user = thread_id
            elif thread_type == ThreadType.GROUP:
                try:
                    user = message_object.replied_to.author
                except:
                    self.send(Message(text="Rᴇᴘʟʏ Tᴏ Usᴇʀs Mᴇssᴀɢᴇ!", reply_to_id=mid), thread_id=thread_id, thread_type=thread_type)
                    pass
            try:
                tk = int(msg)
            except:
                self.send(Message(text='Numbers Only.. ', reply_to_id=mid), thread_id=thread_id, thread_type=thread_type)
                pass

            balanceData = userdb.find({"uid":user})[0]['balance']
            balanceData['baki']['bakiLimit'] = tk
            userdb.update_one({"uid":user}, {"$set":{'balance':balanceData}})
            # userdb.find({"uid":user})[0]['balance']['baki']['bakiLimit']
            self.send(Message(text=f'Bᴀᴋɪ Lɪᴍɪᴛ Uᴘᴅᴀᴛᴇᴅ Tᴏ : {tk} Tᴋ', reply_to_id=mid), thread_id=thread_id, thread_type=thread_type)

        elif "/addbalance" == command and author_id in admins:
            if thread_type == ThreadType.USER:
                user = thread_id
            elif thread_type == ThreadType.GROUP:
                try:
                    user = message_object.replied_to.author
                except:
                    self.send(Message(text="Rᴇᴘʟʏ Tᴏ Usᴇʀs Mᴇssᴀɢᴇ!", reply_to_id=mid), thread_id=thread_id, thread_type=thread_type)
                    pass
            try:
                tk = int(msg)
            except:
                self.send(Message(text='Numbers Only.. ', reply_to_id=mid), thread_id=thread_id, thread_type=thread_type)
                pass

            balanceData = userdb.find({"uid":user})[0]['balance']
            balanceData['advance'] += tk
            userdb.update_one({"uid":user}, {"$set":{'balance':balanceData}})
            balance = userdb.find({"uid":user})[0]['balance']['advance']
            self.send(Message(text=f'Bᴀʟᴀɴᴄᴇ Aᴅᴅᴇᴅ : {tk} Tk.\n\nNᴇᴡ Bᴀʟᴀɴᴄᴇ  : {balance}', reply_to_id=mid), thread_id=thread_id, thread_type=thread_type)


        elif command == '/uc':
            if author_id in admins or author_id in users():
                bdt = msg.split()[0]
                try:
                    ammount = msg.split()[1]
                except:
                    ammount = 1

                if bdt not in ["80", '160', '405', '810', '1625', '161', '162', '800', '2000']:
                    self.send(Message(text='Pʟᴇᴀsᴇ Sᴘᴇᴄɪғʏ Cᴏʀʀᴇᴄᴛ ʙᴅᴛ \n\nExᴀᴍᴘʟᴇ : /uc 80 <ammount>', reply_to_id=mid), thread_id=thread_id, thread_type=thread_type)
                    return

                try:
                    ammount = int(ammount)
                    if ammount < 0 :
                        self.send(Message(text='Oɴʟʏ Positive Nᴜᴍʙᴇʀ. \n\nExᴀᴍᴘʟᴇ : /uc 80 2', reply_to_id=mid), thread_id=thread_id, thread_type=thread_type)
                        pass

                except:
                    self.send(Message(text='Oɴʟʏ Nᴜᴍʙᴇʀ. \n\nExᴀᴍᴘʟᴇ : /uc 80 2', reply_to_id=mid), thread_id=thread_id, thread_type=thread_type)
                    pass

                avUC = mydb.find({"type":"ucs"})[0][bdt]
                if len(avUC) == 0:
                    self.send(Message(text=f'⚠︎ {bdt} 🆄︎🅲︎ Sᴛᴏᴄᴋ Oᴜᴛ ⚠︎', reply_to_id=mid), thread_id=thread_id, thread_type=thread_type)
                
                elif len(avUC) < ammount:
                    self.send(Message(text=f'⚠︎ Oɴʟʏ {len(avUC)} Pɪᴄᴇs {bdt} 🆄︎🅲︎ Aᴠᴀɪʟᴀʙʟᴇ ⚠︎', reply_to_id=mid), thread_id=thread_id, thread_type=thread_type)
                
                else:
                    if author_id in admins:
                        sendUc = ""
                        for i in range(ammount):
                            sendUc = sendUc + "• " + avUC.pop(0) + "\n"

                        sendUc = sendUc + f'\n\n✓ {bdt} 🆄︎🅲︎  x  {ammount}  ✓'
                        self.send(Message(text=sendUc, reply_to_id=mid), thread_id=thread_id, thread_type=thread_type)
                        mydb.update_one({"type":"ucs"},{'$set':{bdt : avUC}})

                    else:
                        itemPrice = mydb.find({"type":"ucPrice"})[0][bdt]
                        totalPrice = itemPrice * ammount
                        userInfo = userdb.find({"uid":author_id})[0]
                        userBalance = userInfo['balance']['advance']
                        
                        if userBalance >=  totalPrice:
                            userInfo['balance']['advance'] -= totalPrice
                            userdb.update_one({"uid":author_id}, {"$set":{'balance':userInfo['balance']}})
                            sendUc = ""
                            for i in range(ammount):
                                sendUc = sendUc + "• " + avUC.pop(0) + "\n"

                            sendUc = sendUc + f'\n\n✓ {bdt} 🆄︎🅲︎  x  {ammount}  ✓'
                            self.send(Message(text=sendUc, reply_to_id=mid), thread_id=thread_id, thread_type=thread_type)
                            mydb.update_one({"type":"ucs"},{'$set':{bdt : avUC}})
                            self.send(Message(text=f"Bᴀʟᴀɴᴄᴇ : {userBalance} - ({itemPrice} x {ammount}) = {userInfo['balance']['advance']}"), thread_id=thread_id, thread_type=thread_type)

                        else:
                            self.send(Message(text=f"Yᴏᴜʀᴜ Dᴏɴᴛ Hᴀᴠᴇ Eɴᴏᴜɢʜ Bᴀʟᴀɴᴄᴇ.\n\n\nBᴀʟᴀɴᴄᴇ :{userBalance}\n\nRᴇǫᴜɪʀᴇᴅ : {itemPrice} x {ammount} = {totalPrice}", reply_to_id=mid), thread_id=thread_id, thread_type=thread_type)
                            pass
            else:
                self.send(Message(text=f'Yᴏᴜ Aʀᴇ Nᴏᴛ Aɴ Usᴇʀ!', reply_to_id=mid), thread_id=thread_id, thread_type=thread_type)


        elif command == "/stock" and (author_id in admins or author_id in users()):
            stock = mydb.find({"type":"ucs"})[0]
            USDT = mydb.find({"type":"priceUSDT"})[0]
            totalUSDT = USDT['80']*len(stock['80'])+USDT['160']*len(stock['160'])+USDT['405']*len(stock['405'])+USDT['810']*len(stock['810'])+USDT['1625']*len(stock['1625'])+USDT['161']*len(stock['161'])+USDT['162']*len(stock['162'])+USDT['800']*len(stock['800'])+USDT['2000']*len(stock['2000'])
            text = f'''
▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔
☞︎︎︎ 80     🆄︎🅲︎  ➪  {len(stock['80'])} ᴘᴄs

☞︎︎︎ 160    🆄︎🅲︎  ➪  {len(stock['160'])} ᴘᴄs

☞︎︎︎ 405   🆄︎🅲︎  ➪  {len(stock['405'])} ᴘᴄs

☞︎︎︎ 810    🆄︎🅲︎  ➪  {len(stock['810'])} ᴘᴄs

☞︎︎︎ 1625  🆄︎🅲︎  ➪  {len(stock['1625'])} ᴘᴄs


☞︎︎︎ 161  🆄︎🅲︎  ➪  {len(stock['161'])} ᴘᴄs

☞︎︎︎ 162  🆄︎🅲︎  ➪  {len(stock['162'])} ᴘᴄs

☞︎︎︎ 800  🆄︎🅲︎  ➪  {len(stock['800'])} ᴘᴄs

☞︎︎︎ 2000 🆄︎🅲︎  ➪  {len(stock['2000'])} ᴘᴄs

▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔
Wᴏʀᴛʜ Oғ : {round(totalUSDT,2)} ᴜsᴅᴛ 
            '''
            self.send(Message(text=text, reply_to_id=mid), thread_id=thread_id, thread_type=thread_type)

        elif command == "/addgc" and author_id in admins:
            try:
                self.addUsersToGroup(thread_id, thread_id="6026226014138998")
            except:
                pass
        

        elif command == "/baki" and thread_id not in admins and (author_id in admins or author_id in users()):
            if author_id in admins:
                if thread_type == ThreadType.USER:
                    user = thread_id
                elif thread_type == ThreadType.GROUP:
                    try:
                        user = message_object.replied_to.author
                    except:
                        self.send(Message(text="Rᴇᴘʟʏ Tᴏ Usᴇʀs Mᴇssᴀɢᴇ!", reply_to_id=mid), thread_id=thread_id, thread_type=thread_type)
                        pass
                    
            elif author_id in users():
                user = author_id
            bdt = msg.split()[0]
            try:
                ammount = msg.split()[1]
            except:
                ammount = 1

            if bdt not in ["80", '160', '405', '810', '1625', '161', '162', '800', '2000']:
                self.send(Message(text='Pʟᴇᴀsᴇ Sᴘᴇᴄɪғʏ Cᴏʀʀᴇᴄᴛ ʙᴅᴛ \n\nExᴀᴍᴘʟᴇ : /baki 80 <ammount>', reply_to_id=mid), thread_id=thread_id, thread_type=thread_type)
                pass

            try:
                ammount = int(ammount)
                if ammount < 0 :
                    self.send(Message(text='Oɴʟʏ Positive Nᴜᴍʙᴇʀ. \n\nExᴀᴍᴘʟᴇ : /baki 80 2', reply_to_id=mid), thread_id=thread_id, thread_type=thread_type)
                    pass

            except:
                self.send(Message(text='Oɴʟʏ Nᴜᴍʙᴇʀ. \n\nExᴀᴍᴘʟᴇ : /baki 80 2', reply_to_id=mid), thread_id=thread_id, thread_type=thread_type)
                pass

            avUC = mydb.find({"type":"ucs"})[0][bdt]
            if len(avUC) == 0:
                self.send(Message(text=f'⚠︎ {bdt} 🆄︎🅲︎ Sᴛᴏᴄᴋ Oᴜᴛ ⚠︎', reply_to_id=mid), thread_id=thread_id, thread_type=thread_type)
                pass

            elif len(avUC) < ammount:
                self.send(Message(text=f'⚠︎ Oɴʟʏ {len(avUC)} Pɪᴄᴇs {bdt} 🆄︎🅲︎ Aᴠᴀɪʟᴀʙʟᴇ ⚠︎', reply_to_id=mid), thread_id=thread_id, thread_type=thread_type)
                pass
            
            else:
                userInfo = userdb.find({"uid":user})[0]
                dueLimit = userInfo['balance']['baki']['bakiLimit']
                due = userInfo['balance']['baki']['due']
                itemPrice = mydb.find({"type":"ucPrice"})[0][bdt]
                totalPrice = itemPrice*ammount

                if (due+totalPrice) <= dueLimit:
                    userInfo['balance']['baki']['due'] += totalPrice
                    userInfo['balance']['baki']['bakiUC'][bdt] += ammount
                    userdb.update_one({"uid":user}, {"$set":{'balance' :userInfo['balance']}})

                    sendUc = ""
                    for i in range(ammount):
                        sendUc = sendUc + "• " + avUC.pop(0) + "\n"

                    sendUc = sendUc + f'\n\n✓ {bdt} 🆄︎🅲︎  x  {ammount}  ✓'
                    self.send(Message(text=sendUc, reply_to_id=mid), thread_id=thread_id, thread_type=thread_type)
                    mydb.update_one({"type":"ucs"},{'$set':{bdt : avUC}})
                    self.send(Message(text=f"Tᴏᴛᴀʟ Dᴜᴇ : {due} + ({itemPrice}x{ammount}) = {userInfo['balance']['baki']['due']}"), thread_id=thread_id, thread_type=thread_type)

                else:
                    self.send(Message(text=f"Yᴏᴜʀ Dᴜᴇ Lɪᴍɪᴛ Is Oᴠᴇʀ.\n\nLɪᴍɪᴛ     : {dueLimit}\n\nUsᴇᴅ     : {userInfo['balance']['baki']['due']}\nLᴇғᴛ    : {dueLimit - userInfo['balance']['baki']['due']}\nRᴇǫᴜɪʀᴇᴅ : {itemPrice} x {ammount} = {totalPrice}", reply_to_id=mid), thread_id=thread_id, thread_type=thread_type)
                    pass


        elif command == '/addbaki' and (author_id in admins) and (thread_id not in admins):
            if thread_type == ThreadType.USER:
                user = thread_id
            elif thread_type == ThreadType.GROUP:
                try:
                    user = message_object.replied_to.author
                except:
                    self.send(Message(text="Rᴇᴘʟʏ Tᴏ Usᴇʀs Mᴇssᴀɢᴇ!", reply_to_id=mid), thread_id=thread_id, thread_type=thread_type)
                    pass

            bdt = msg.split()[0]
            if bdt not in ["80", '160', '405', '810', '1625', '161', '162', '800', '2000']:
                self.send(Message(text='Pʟᴇᴀsᴇ Sᴘᴇᴄɪғʏ Cᴏʀʀᴇᴄᴛ ʙᴅᴛ \n\nExᴀᴍᴘʟᴇ : /addbaki 80 <ammount>', reply_to_id=mid), thread_id=thread_id, thread_type=thread_type)
                pass

            try:
                ammount = msg.split()[1]
            except:
                ammount = 1
            try:
                ammount = int(ammount)
            except:
                self.send(Message(text='Oɴʟʏ Nᴜᴍʙᴇʀ. \n\nExᴀᴍᴘʟᴇ : /addbaki 80 2', reply_to_id=mid), thread_id=thread_id, thread_type=thread_type)
                pass

            itemPrice = mydb.find({"type":"ucPrice"})[0][bdt]
            userInfo = userdb.find({"uid":user})[0]
            userInfo['balance']['baki']['bakiUC'][bdt] += ammount
            userInfo['balance']['baki']['due'] += itemPrice*ammount
            userdb.update_one({"uid":user}, {"$set":{'balance':userInfo['balance']}})
            self.send(Message(text='Bᴀᴋɪ Lɪsᴛ Uᴘᴅᴀᴛᴇᴅ!\n\nUsᴇ Cᴏᴍᴍᴀɴᴅ "/check" Tᴏ Sᴇᴇ Yᴏᴜʀ Lɪsᴛ! ', reply_to_id=mid), thread_id=thread_id, thread_type=thread_type)


        elif ("/check" == command or "/due" == command) and (author_id in users() or author_id in admins) and (thread_id not in admins):
            if author_id in admins:
                if thread_type == ThreadType.USER:
                    user = thread_id
                elif thread_type == ThreadType.GROUP:
                    try:
                        user = message_object.replied_to.author
                    except:
                        self.send(Message(text="Rᴇᴘʟʏ Tᴏ Usᴇʀs Mᴇssᴀɢᴇ!", reply_to_id=mid), thread_id=thread_id, thread_type=thread_type)
                        pass
                    
            elif author_id in users():
                user = author_id

            userInfo = userdb.find({"uid":user})[0] 
            due = userInfo['balance']['baki']['due']
            bakiUC = userInfo['balance']['baki']['bakiUC']
            text =f'''
☞︎︎︎ 80   🆄︎🅲︎  ➪  {bakiUC['80']} ᴘᴄs

☞︎︎︎ 160  🆄︎🅲︎  ➪  {bakiUC['160']} ᴘᴄs

☞︎︎︎ 405  🆄︎🅲︎  ➪  {bakiUC['405']} ᴘᴄs

☞︎︎︎ 810  🆄︎🅲︎  ➪  {bakiUC['810']} ᴘᴄs

☞︎︎︎ 1625 🆄︎🅲︎  ➪  {bakiUC['1625']} ᴘᴄs


☞︎︎︎ 161  🆄︎🅲︎  ➪  {bakiUC['161']} ᴘᴄs

☞︎︎︎ 162  🆄︎🅲︎  ➪  {bakiUC['162']} ᴘᴄs

☞︎︎︎ 800  🆄︎🅲︎  ➪  {bakiUC['800']} ᴘᴄs

☞︎︎︎ 2000 🆄︎🅲︎  ➪  {bakiUC['2000']} ᴘᴄs

▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔
☞︎︎︎ Tᴏᴛᴀʟ Dᴜᴇ ➪ {due} Tᴋ

            '''
            self.send(Message(text=text, reply_to_id=mid), thread_id=thread_id, thread_type=thread_type)
        

        elif command == "/clear" and author_id in admins:
            if thread_type == ThreadType.USER:
                user = thread_id
            elif thread_type == ThreadType.GROUP:
                try:
                    user = message_object.replied_to.author
                except:
                    self.send(Message(text="Rᴇᴘʟʏ Tᴏ Usᴇʀs Mᴇssᴀɢᴇ!", reply_to_id=mid), thread_id=thread_id, thread_type=thread_type)
                    pass

            userInfo = userdb.find({"uid":user})[0]
            userInfo['balance']['baki']['due'] = 0
            userInfo['balance']['baki']['bakiUC'] = {'80': 0, '160': 0, '405': 0, '810': 0, '1625': 0, '161' : 0, '162' : 0, '800' : 0, '2000' : 0}
            userdb.update_one({"uid":user}, {"$set":{'balance':userInfo['balance']}})
            self.send(Message(text=f"Dᴜᴇ Cʟᴇᴀʀ Oғ {userInfo['name']} !\n\nTʜᴀɴᴋs Fᴏʀ Yᴏᴜʀ Sᴜᴘᴘᴏʀᴛ ❤️❤️", reply_to_id=mid), thread_id=thread_id, thread_type=thread_type)

        elif "/rate" == command and (author_id in admins or author_id in users()):
            itemPrice = mydb.find({"type":"ucPrice"})[0]
            text =f'''
☞︎︎︎ 80   🆄︎🅲︎  ➪  {itemPrice['80']} Bᴀɴᴋ

☞︎︎︎ 160  🆄︎🅲︎  ➪  {itemPrice['160']} Bᴀɴᴋ

☞︎︎︎ 405  🆄︎🅲︎  ➪  {itemPrice['405']} Bᴀɴᴋ

☞︎︎︎ 810  🆄︎🅲︎  ➪  {itemPrice['810']} Bᴀɴᴋ

☞︎︎︎ 1625 🆄︎🅲︎  ➪  {itemPrice['1625']} Bᴀɴᴋ


☞︎︎︎ 161  🆄︎🅲︎  ➪  {itemPrice['161']} Bᴀɴᴋ

☞︎︎︎ 162  🆄︎🅲︎  ➪  {itemPrice['162']} Bᴀɴᴋ

☞︎︎︎ 800  🆄︎🅲︎  ➪  {itemPrice['800']} Bᴀɴᴋ

☞︎︎︎ 2000 🆄︎🅲︎  ➪  {itemPrice['2000']} Bᴀɴᴋ
▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔
☞︎︎︎ SM Payment ➪ +1%


            '''
            self.send(Message(text=text, reply_to_id=mid), thread_id=thread_id, thread_type=thread_type)
        

        elif "/notify" == command and author_id in admins:
            bakiUsers = [{'uid' :i['uid'],'name':i['name'], 'due':i['balance']['baki']['due']} for i in userdb.find({}) if i['balance']['baki']['due'] != 0]
            if len(bakiUsers) != 0:
                for User in bakiUsers:

                    text = f'''
▔▔▔▔▔▔▔▔▔▔▔▔
Dᴇᴀʀ {User['name']} ❤️


➪ Yᴏᴜʀ Dᴜᴇ :  {User['due']} Tᴋ
➪ Pʟᴇᴀsᴇ Pᴀʏ !!
▔▔▔▔▔▔▔▔▔▔▔▔


'''
                    try:
                        print(User['uid'])
                        self.send(Message(text=text+msg), thread_id=User['uid'], thread_type=ThreadType.USER)

                    except Exception as ex:
                        print(ex)
            
     


while True: 
    try:
#         keep_alive()
        c_user = "100007289010328"
        xs = pymongo.MongoClient("mongodb+srv://pBot:%24%24Nabil%24%24@pbot.wttlhxr.mongodb.net/?retryWrites=true&w=majority")['Users'].userInfo.find({"c_user" : c_user})[0]["xs"]

        cookies = {
        "sb": "xasyYmAoy1tRpMGYvLxgkHBF",
        "fr": "0NxayJuewRHQ30OX3.AWVJwIYNh0Tt8AJv6kSwDamhkoM.BiMrVd.Iu.AAA.0.0.BiMtVZ.AWXMVaiHrpQ",
        "c_user": c_user,
        "datr": "xasyYs51GC0Lq5",
    " xs" : xs
    }
        client = ChatBot("","", session_cookies=cookies)
        print(client.isLoggedIn())
#         client.listen()
    except:
        continue
