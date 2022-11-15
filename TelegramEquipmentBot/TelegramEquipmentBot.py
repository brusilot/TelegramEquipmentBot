
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters

import json
from datetime import datetime
from settings.credentials import bot_token

updater = Updater(bot_token,
                  use_context=True)
  
  
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Bot started sucessfully")


def help(update: Update, context: CallbackContext):
    update.message.reply_text("""Bot created to control equipment reservation
For a list of commands please type /commands""")
    
def commands(update: Update, context: CallbackContext):
    update.message.reply_text("""addUser {name} -> Add user to DB 
addEquipment {equipment} -> Add equipment to DB
addReservation {equipment} {user} {startDate As YYYY-MM-DD} {endDate as YYYY-MM-DD} -> Add a reservation to the calendar
""")
    
def unknown_text(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry I can't recognize you , you said '%s'" % update.message.text)
  
  
def unknown(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry '%s' is not a valid command" % update.message.text)

## control calls

def addUser(update, context):
    args=update.message.text[9:] #9 because your command is /addUser (+space) = 9 chars
    args = args.split()        #create split
    name = args[0]              #first from split is class to search
    update.message.reply_text(userAdd(name))
    
def addEquipment(update, context):
    args=update.message.text[14:] #14 because your command is /addEquipment (+space) = 14 chars
    args = args.split()        #create split
    equipment = args[0]              #first from split is class to search
    update.message.reply_text(equipmentAdd(equipment))
    

def addReservation(update, context):
    args=update.message.text[16:] #16 because your command is /addReservation (+space) = 16 chars
    args = args.split()        #create split
    print(arg.lenght())
    equipment = args[0]  
    name = args[1] 
    start = args[2] 
    end = args[3] 
    reservationAdd(equipment, name, start, end)

##initial Handlers

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('commands', commands))

## Our Handlers

updater.dispatcher.add_handler(CommandHandler('addUser', addUser))
updater.dispatcher.add_handler(CommandHandler('addEquipment', addEquipment))
updater.dispatcher.add_handler(CommandHandler('addUser', addUser))

## unknow command handlers

updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
updater.dispatcher.add_handler(MessageHandler(
    # Filters out unknown commands
    Filters.command, unknown))
  
# Filters out unknown messages.
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))

## user Functions
def userAdd(name):
    with open('users.json', 'r+') as f:
        users = json.load(f)
        for i in users:
            if i["name"] == name:
                f.close() 
                return("user already added")
        newuser = {
            "name": name
        }
        users.append(newuser)
        f.seek(0)
        json.dump(users, f, indent = 3)
        f.close() 
        return("adding user")
       
    
def userExists(name):
    with open('users.json', 'r+') as f:
            users = json.load(f)
            for i in users:
                if i["name"] == name:
                    f.close() 
                    return True
            f.close() 
            return False
        
def userDelete(name):
    with open('users.json', 'r') as f:
        users = json.load(f)

        users = [obj for obj in users if obj['name'] != name]
        with open('users.json', 'w') as f:
            json.dump(users, f)
    f.close() 
    return("User Removed")

## Equipment Functions

def equipmentAdd(equipment):
    with open('equipment.json', 'r+') as f:
        equipments = json.load(f)
        for i in equipments:
            if i["equipment"] == equipment:
                print("equipment already added")
                return
        newequipment = {
            "equipment": equipment
        }
        equipments.append(newequipment)
        f.seek(0)
        json.dump(equipments, f, indent = 3)
        print("adding equipment")
    f.close()    
    
def equipmentExists(equipment):
    with open('equipment.json', 'r+') as f:
            users = json.load(f)
            for i in users:
                if i["equipment"] == equipment:
                    return True
            return False
        
def equipmentDelete(equipment):
    with open('equipment.json', 'r') as f:
        equipments = json.load(f)

        equipments = [obj for obj in equipments if obj['equipment'] != equipment]
        with open('equipment.json', 'w') as f:
            json.dump(equipments, f)
    f.close() 
    return("Equipment Removed")

## Reservation Functions

def reservationAdd(equipment, name, start, end):
    format = "%Y-%m-%d"
    startDt = datetime.strptime(start, format)
    if startDt <  datetime.today():
        return("Initial date before today")
    if end < start:
        return("Final date before start date")
    if equipmentExists(equipment) == False:
        return("equipament not found")
    if userExists(name) == False:
        return("user not found")
    if conflict(equipment, start, end) == True:
        return("Equipament already taken in this period")
    with open('calendar.json', 'r+') as f:
        calendar = json.load(f)
        newReservation = {
            "user": name,
            "equipment": equipment,
            "start": start,
            "end": end
        }
        calendar.append(newReservation)
        f.seek(0)
        json.dump(calendar, f, indent = 3)
        print("adding reservation")
    f.close()    
    
    
def conflict(equipment, inicio, fim):
     with open('calendar.json', 'r') as f:
        calendario = json.load(f)
        for i in calendario:
            if i["equipment"] == equipment:
                if i["start"] <= inicio <= i["end"]:
                    return True
                if i["start"] <= fim <= i["end"]:
                    return True 
                if inicio <= i["start"] <= fim:
                    return True
                if inicio <= i["end"] <= fim:
                    return True 
        return False


## start Bot
updater.start_polling()


## TODOS

## - See calendar
## - remove from calendar if ended more than 7 days ago
## - Validation to call commands if has all the args
## - Graphical Calendar?
## - use with buttons?