import time, threading, datetime, re, requests
from config import token, chat

StartTime = time.time()

class setInterval:
    def __init__(self, interval, action):
        self.interval = interval
        self.action = action
        self.stopEvent = threading.Event()
        thread = threading.Thread(target=self.__setInterval)
        thread.start()
    def __setInterval(self):
        nextTime = time.time() + self.interval
        while not self.stopEvent.wait(nextTime - time.time()):
            nextTime += self.interval
            self.action()
    def cancel(self):
        self.stopEvent.set()

def send_message(text, chat):
    global token
    params = {'chat_id': chat, 'text': text}
    response = requests.post("https://api.telegram.org/bot" + token + "/sendMessage", data=params)
    return response

def send():
    base = open("base.db", "r")
    while True:
        item = base.readline()
        if not item:
            break
        data = item.split("|")
        text = data[1]
        types = str(data[3])
        regus = str(data[2])
        timer = data[0].split(" ")
        date = str(timer[0])
        time = str(timer[1])
        today = datetime.datetime.now()
        date_time = str(today.strftime("%H:%M"))
        date_date = str(today.strftime("%Y-%m-%d"))
        id = "{} {}|{}|{}".format(date, time, text, regus)
        if date_date == date:
            if date_time == time:
                global chat
                massage = send_message(str(text), chat)
                if regus == "false":
                    with open('base.db') as f:
                        lines = f.readlines()
                    pattern = re.compile(re.escape(id))
                    with open('base.db', 'w') as f:
                        for line in lines:
                            result = pattern.search(line)
                            if result is None:
                                f.write(line)
                else:
                    if types == "0\n":
                        year = int(date.split("-")[0])
                        motc = int(date.split("-")[1])
                        day = int(date.split("-")[2])
                        newday = day + 1
                        if newday > 31:
                            newday = 1
                            if motc > 12:
                                year = year + 1
                                motc = 1
                            else:
                                motc = motc + 1
                        if motc < 10:
                            motc = "0{}".format(motc)
                        if newday < 10:
                            newday = "0{}".format(newday)
                        if motc < 10:
                            motc = "0{}".format(motc)
                        if newday == 10:
                            newday = 10
                        newid = "{} {}|{}|{}".format(year, motc, str(newday), time, text, regus)
                        with open('base.db', 'r') as f:
                            old_data = f.read()
                        new_data = old_data.replace(id, newid)
                        with open('base.db', 'w') as f:
                            f.write(new_data)
                    if types == "1\n":
                        year = int(date.split("-")[0])
                        motc = int(date.split("-")[1])
                        day = int(date.split("-")[2])
                        if day < 10:
                            day = "0{}".format(newday)
                        newmotc = motc + 1
                        if motc > 12:
                            newmotc = 1
                            year = year + 1
                        if newmotc < 10:
                            newmotc = "0{}".format(newmotc)
                        newid = "{}-{}-{} {}|{}|{}".format(year, str(newmotc), day, time, text, regus)
                        with open('base.db', 'r') as f:
                            old_data = f.read()
                        new_data = old_data.replace(id, newid)
                        with open('base.db', 'w') as f:
                            f.write(new_data)
                    if types == "2\n":
                        year = int(date.split("-")[0])
                        motc = int(date.split("-")[1])
                        day = int(date.split("-")[2])
                        newyear = year + 1
                        if motc < 10:
                            motc = "0{}".format(motc)
                        if day < 10:
                            day = "0{}".format(day)
                        newid = "{}-{}-{} {}|{}|{}".format(str(newyear), motc, day, time, text, regus)
                        with open('base.db', 'r') as f:
                            old_data = f.read()
                        new_data = old_data.replace(id, newid)
                        with open('base.db', 'w') as f:
                            f.write(new_data)
    base.close()

inter = setInterval(30, send) #30 - время обновления таймера