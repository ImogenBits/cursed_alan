from logging import error
import discord
import os
from dotenv import load_dotenv

load_dotenv()

client = discord.Client()

q1 = "👻"
q2 = "🦇"
q3 = "🧹"
q4 = "🧙"
q5 = "🔮"
q6 = "🧞"

qF = "🪄"

Q = {q1, q2, q3, q4, q5, q6, qF}

# (sym, dir, q)
utm = {
    q1: {
        0: (4, -1, q1),
        1: (3, 1, q1),
        2: (2, -1, q1),
        3: (0, 1, q1),
        4: (4, -1, q1),
        5: (0, 1, q4),
    },
    q2: {
        0: (0, 1, q2),
        1: (3, -1, q3 ),
        2: (4, 1, q2),
        3: (3, -1, q2),
        4: (1, -1, q2),
        5: (2, 1, q2),
    },
    q3: {
        0: (1, 1, q3),
        1: (4, 1, q4),
        2: (2, 1, q3),
        3: (3, 0, qF),
        4: (5, 1, q1),
        5: (1, 1, q1),
    },
    q4: {
        0: (0, 1, q4),
        1: (5, -1, q2),
        2: (4, 1, q4),
        3: (3, 0, qF),
        4: (5, -1, q2),
        5: (2, 1, q4),
    }
}

pal = {
    q1: {
        0: (1, 0, qF),
        1: (0, 1, q2),
        2: (0, 1, q3),
    },
    q2: {
        0: (0, -1, q4),
        1: (1, 1, q2),
        2: (2, 1, q2),
    },
    q3: {
        0: (0, -1, q5),
        1: (1, 1, q3),
        2: (2, 1, q3),
    },
    q4: {
        #0: (0, -1, q5),
        1: (0, -1, q6),
        2: (0, 0, qF),
    },
    q5: {
        #0: (0, -1, q5),
        1: (0, 0, qF),
        2: (0, -1, q6),
    },
    q6: {
        0: (0, 1, q1),
        1: (1, -1, q6),
        2: (2, -1, q6),
    },
}

tms = {"utm": utm, "pal": pal}

def step(msg, tm):
    head = 0
    while head < len(msg) and msg[head] not in Q:
        head += 1
    if head >= len(msg):
        return False, "no state found"
    if msg[head] == qF:
        return False, "computation finished"
    
    if head == len(msg) - 1:
        msg = msg + "0"

    state, sym = msg[head], msg[head + 1]
    newSym, dir, newState = tm[state][int(sym)]

    if dir == -1 and head == 0:
        msg = "0" + msg
        head += 1

    newSym = str(newSym)
    leftSym = msg[head - 1] if head >= 1 else ""
    oldStart = msg[:head - 1] if head >= 2 else ""

    if dir == 1:
        newMsg = leftSym + newSym + newState
    elif dir == -1:
        leftSym = leftSym if leftSym != "" else "0"
        newMsg = newState + leftSym + newSym
    elif dir == 0:
        newMsg = leftSym + newState + newSym
    
    return True, oldStart + newMsg + msg[head + 2:]

def getNewMessage(msg):
    if msg == "stop" or len(msg) == 0:
        return ""

    msgArr = msg.split()

    if len(msgArr) == 1:
        tm = utm
    elif msgArr[0] in tms:
        tm = tms[msgArr[0]]
        id = msgArr[1]
    else:
       return "TM not found, supported TMs are: " + ", ".join(tms)

    cont, newMsg = step(id, tm)
    if not cont:
        return newMsg

    if len(msgArr) == 1:
        newTM = ""
    else:
        newTM = msgArr[0] + " "

    return "!tm " + newTM + newMsg

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")

@client.event
async def on_message(message):
    if message.content.startswith("!tm "):
        newMsg = getNewMessage(message.content[4:])
        if newMsg != "":
            await message.channel.send(newMsg)

client.run(os.getenv('TOKEN'))