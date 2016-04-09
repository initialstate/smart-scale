#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections
import time
import bluetooth
import sys
import subprocess
from ISStreamer.Streamer import Streamer
from random import randint

# --------- User Settings ---------
BUCKET_NAME = ":apple: My Weight History"
BUCKET_KEY = "weight11"
ACCESS_KEY = "PLACE YOUR INITIAL STATE ACCESS KEY HERE"
METRIC_UNITS = False
WEIGHT_SAMPLES = 500
THROWAWAY_SAMPLES = 100
WEIGHT_HISTORY = 7
# ---------------------------------

# Wiiboard Parameters
CONTINUOUS_REPORTING = "04"  # Easier as string with leading zero
COMMAND_LIGHT = 11
COMMAND_REPORTING = 12
COMMAND_REQUEST_STATUS = 15
COMMAND_REGISTER = 16
COMMAND_READ_REGISTER = 17
INPUT_STATUS = 20
INPUT_READ_DATA = 21
EXTENSION_8BYTES = 32
BUTTON_DOWN_MASK = 8
TOP_RIGHT = 0
BOTTOM_RIGHT = 1
TOP_LEFT = 2
BOTTOM_LEFT = 3
BLUETOOTH_NAME = "Nintendo RVL-WBC-01"


class EventProcessor:
    def __init__(self):
        self._measured = False
        self.done = False
        self._measureCnt = 0
        self._events = range(WEIGHT_SAMPLES)
        self._weights = range(WEIGHT_HISTORY)
        self._times = range(WEIGHT_HISTORY)
        self._unit = "lb"
        self._weightCnt = 0
        self._prevWeight = 0
        self._weight = 0
        self._weightChange = 0
        self.streamer = Streamer(bucket_name=BUCKET_NAME,bucket_key=BUCKET_KEY,access_key=ACCESS_KEY)

    def messageWeighFirst(self, weight, unit):
        weight = float("{0:.2f}".format(weight))
        msg = []
        msg.append("What do vegan zombies eat? Gggggrrrraaaaaaaiiiiinnnnnssssss❗️ You weigh " + str(weight) + " " + unit + "!")
        msg.append("Guys that wear skinny jeans took the phrase, getting into her pants, the wrong way. 👖 You weigh " + str(weight) + " " + unit + "!")
        msg.append("Why do watermelons have fancy weddings? Because they cantaloupe. 🍉 You weigh " + str(weight) + " " + unit + "!")
        msg.append("Why did the can crusher quit his job? Because it was soda pressing. 😜 You weigh " + str(weight) + " " + unit + "!")
        msg.append("My friend thinks he is smart. He told me an onion is the only food that makes you cry, so I threw a coconut at his face. You = " + str(weight) + " " + unit)
        msg.append("Turning vegan is a big missed steak. 😜 You weigh " + str(weight) + " " + unit + "!")
        msg.append("Is there anything more capitalist than a peanut with a top hat, cane, and monocle selling you other peanuts to eat? You weigh " + str(weight) + " " + unit + "!")
        msg.append("How has the guy who makes Capri Sun straw openings not been up for a job performance review? You weigh " + str(weight) + " " + unit + "!")
        msg.append("How do I like my eggs? Umm, in a cake. 🍰 You weigh " + str(weight) + " " + unit + "!")
        msg.append("Billy has 32 pieces of bacon and eats 28. What does he have now? Happiness. Billy has happiness. You weigh " + str(weight) + " " + unit + "!")
        msg.append("Diet day 1: I have removed all the bad food from the house. It was delicious. You weigh " + str(weight) + " " + unit + "!")
        msg.append("When I see you, I am happy, I love you not for what you look like, but for what you have inside. -Me to my fridge. You weigh " + str(weight) + " " + unit + "!")
        msg.append("Netflix has 7 letters. So does foooood. Coincidence? I think not. You weigh " + str(weight) + " " + unit + "!")
        msg.append("Studies show that if there is going to be free food, I will show up 100 percent of the time. You weigh " + str(weight) + " " + unit + "!")
        msg.append("I can multitask. I can eat breakfast and think about lunch at the same time. You weigh " + str(weight) + " " + unit + "!")
        return msg[randint(0, len(msg)-1)]

    def messageWeighLess(self, weight, weightChange, unit):
        weight = float("{0:.2f}".format(weight))
        weightChange = float("{0:.2f}".format(weightChange))
        msg = []
        msg.append("You're getting so skinny that if someone slaps you, they'll get a paper cut. 👋 You lost " + str(abs(weightChange)) + " " + unit + " since last time (" + str(weight) + " " + unit + ").")
        msg.append("Wow that Lean Cuisine really filled me up - Said No One Ever. 🍲 You lost " + str(abs(weightChange)) + " " + unit + " since last time (" + str(weight) + " " + unit + ").")
        msg.append("Whoever said nothing tastes as good as skinny feels has clearly never had 🍕 or 🍷 or 🍰. You lost " + str(abs(weightChange)) + " " + unit + " (" + str(weight) + " " + unit + ").")
        msg.append("I know milk does a body good, but damn, how much have you been drinking? 😍 You lost " + str(abs(weightChange)) + " " + unit + " since last time (" + str(weight) + " " + unit + ").")
        msg.append("Are you from Tennessee? Because you're the only ten I see! 😍 You lost " + str(abs(weightChange)) + " " + unit + " since last time (" + str(weight) + " " + unit + ").")
        msg.append("If you were words on a page, you'd be what they call FINE PRINT! 📖 You lost " + str(abs(weightChange)) + " " + unit + " since last time (" + str(weight) + " " + unit + ").")
        msg.append("If you were a transformer, you'd be a HOT-obot, and your name would be Optimus Fine! 😍 You lost " + str(abs(weightChange)) + " " + unit + " (" + str(weight) + " " + unit + ").")
        msg.append("WTF! (where's the food) 🍗 You lost " + str(abs(weightChange)) + " " + unit + " since last time (" + str(weight) + " " + unit + ").")
        msg.append("It's a lot easier to stop eating carbs once you've come to terms with living a joyless life full of anger and sadness. U lost " + str(abs(weightChange)) + " " + unit + " (" + str(weight) + " " + unit + ")")
        msg.append("The Roomba just beat me to a piece of popcorn on the floor. This is how the war against the machines begins. U lost " + str(abs(weightChange)) + " " + unit + " (" + str(weight) + " " + unit + ")")
        msg.append("I won't be impressed with technology until I can download food. You lost " + str(abs(weightChange)) + " " + unit + " since last time (" + str(weight) + " " + unit + ").")
        msg.append("I choked on a carrot today and all I could think was I bet a doughnut wouldn't have done this to me. U lost " + str(abs(weightChange)) + " " + unit + " (" + str(weight) + " " + unit + ")")
        msg.append("Asking me if I am hungry is like asking me if I want money. You lost " + str(abs(weightChange)) + " " + unit + " since last time (" + str(weight) + " " + unit + ").")
        msg.append("I think my soulmate might be carbs. You lost " + str(abs(weightChange)) + " " + unit + " since last time (" + str(weight) + " " + unit + ").")
        msg.append("Great job! We made a video about your progress. Check it out at https://youtu.be/dQw4w9WgXcQ. U lost " + str(abs(weightChange)) + " " + unit + " (" + str(weight) + " " + unit + ").")
        return msg[randint(0, len(msg)-1)]

    def messageWeighMore(self, weight, weightChange, unit):
        weight = float("{0:.2f}".format(weight))
        weightChange = float("{0:.2f}".format(weightChange))
        msg = []
        msg.append("You are in shape ... round is a shape 🍩. You gained " + str(weightChange) + " " + unit + " since last time (" + str(weight) + " " + unit + ").")
        msg.append("You gained " + str(weightChange) + " " + unit + " since last time (" + str(weight) + " " + unit + "). I didn't want to sugarcoat it b/c I was afraid you would eat that too. 🍦")
        msg.append("You gained " + str(weightChange) + " " + unit + " since last time (" + str(weight) + " " + unit + "). I hated telling you that b/c you apparently have enough on your plate. 🍽")
        msg.append("Stressed spelled backwards is desserts, but I bet you already knew that. 🍰 You gained " + str(weightChange) + " " + unit + " since last time (" + str(weight) + " " + unit + ").")
        msg.append("You gained " + str(weightChange) + " " + unit + " since last time (" + str(weight) + " " + unit + "). You probably just forgot to go to the gym. That's like what, 8 years in a row now? 🏋")
        msg.append("You gained " + str(weightChange) + " " + unit + " since last time (" + str(weight) + " " + unit + "). The good news is that you are getting easier to see! 🔭")
        msg.append("You gained " + str(weightChange) + " " + unit + " since last time (" + str(weight) + " " + unit + "). YOLO! (You Obviously Love Oreos) 💛")
        msg.append("You should name your dog Five Miles so you can honestly say you walk Five Miles every day. 🐶 You gained " + str(weightChange) + " " + unit + " (" + str(weight) + " " + unit + ")")
        msg.append("Instead of a John, call your bathroom a Jim so you can honstely say you go to the Jim every morning. 🚽 You gained " + str(weightChange) + " " + unit + " (" + str(weight) + " " + unit + ")")
        msg.append("You gained " + str(weightChange) + " " + unit + " since last time (" + str(weight) + " " + unit + "). The good news is that there is more of you to love! 💛")
        msg.append("You gained " + str(weightChange) + " " + unit + " since last time (" + str(weight) + " " + unit + "). 💩")
        msg.append("You gained " + str(weightChange) + " " + unit + " since last time (" + str(weight) + " " + unit + "). I gave up desserts once. It was the worst 20 minutes of my life. 🍪 ")
        msg.append("When you phone dings, do people think you are backing up? 🚚 You gained " + str(weightChange) + " " + unit + " since last time (" + str(weight) + " " + unit + ").")
        msg.append("Always eat alone. If people never see you eat, they might believe you when you say you have a thyroid problem. You gained " + str(weightChange) + " " + unit + " (" + str(weight) + ")")
        msg.append("After exercising, I always eat a pizza ... just kidding, I don't exercise. 🍕 You gained " + str(weightChange) + " " + unit + " since last time (" + str(weight) + " " + unit + ").")
        msg.append("If you are what you eat, perhaps you should eat a skinny person. 😱 You gained " + str(weightChange) + " " + unit + " since last time (" + str(weight) + " " + unit + ").")
        msg.append("I never run with scissors. OK, those last two words were unnecessary. ✂️ You gained " + str(weightChange) + " " + unit + " since last time (" + str(weight) + " " + unit + ").")
        msg.append("You gained " + str(weightChange) + " " + unit + " since last time (" + str(weight) + " " + unit + "). I am sure it is all muscle. 💪 ")
        msg.append("Yeah, I'm into fitness... Fit'ness whole burger in my mouth. 🍔👅 You gained " + str(weightChange) + " " + unit + " since last time (" + str(weight) + " " + unit + ").")
        return msg[randint(0, len(msg)-1)]

    def messageWeighSame(self, weight, weightChange, unit):
        weight = float("{0:.2f}".format(weight))
        weightChange = float("{0:.2f}".format(weightChange))
        msg = []
        msg.append("Congratulations on nothing ... you practically weigh the same since last time. " + str(weight) + " " + unit + " (" + str(weightChange) + " " + unit + " change)")
        msg.append("What do you call a fake noodle? An impasta. 🍝 Your weight didn't change much since last time. " + str(weight) + " " + unit + " (" + str(weightChange) + " " + unit + " change)")
        msg.append("Bacon is low-carb and gluten-free ... just sayin'. 🐷 Your weight didn't change much since last time. " + str(weight) + " " + unit + " (" + str(weightChange) + " " + unit + " change)")
        msg.append("I may look like I am deep in thought, but I'm really just thinking about what I'm going to eat later. " + str(weight) + " " + unit + " (" + str(weightChange) + " " + unit + " change)")
        msg.append("I haven't eaten an apple in days. The doctors are closing in. My barricade won't last. Tell my family I love th-. " + str(weight) + " " + unit + " (" + str(weightChange) + " " + unit + " change)")
        msg.append("Ban pre-shredded cheese. Make America grate again. 🧀 Your weight didn't change much since last time. " + str(weight) + " " + unit + " (" + str(weightChange) + " " + unit + " change)")
        msg.append("If I share my food with you, it's either because I love you a lot or because it fell on the floor. " + str(weight) + " " + unit + " (" + str(weightChange) + " " + unit + " change)")
        msg.append("The sad moment you lose a chip in the dip so you send in a recon chip and that breaks too. " + str(weight) + " " + unit + " (" + str(weightChange) + " " + unit + " change)")
        msg.append("I only want two things: 1 - To lose weight. 2 - To eat. " + str(weight) + " " + unit + " (" + str(weightChange) + " " + unit + " change)")
        msg.append("I enjoy long, romantic walks to the fridge. " + str(weight) + " " + unit + " (" + str(weightChange) + " " + unit + " change)")
        msg.append("I just don't wanna look back and think, I could have eaten that. " + str(weight) + " " + unit + " (" + str(weightChange) + " " + unit + " change)")
        msg.append("Most people want a perfect relationship. I just want a hamburger that looks like the one in commercials. " + str(weight) + " " + unit + " (" + str(weightChange) + " " + unit + " change)")
        msg.append("Love is in the air ... or is that bacon? 🐷 Your weight didn't change much since last time. " + str(weight) + " " + unit + " (" + str(weightChange) + " " + unit + " change)")
        msg.append("That is too much bacon. -Said No One Ever 🐷 Your weight didn't change much since last time. " + str(weight) + " " + unit + " (" + str(weightChange) + " " + unit + " change)")
        return msg[randint(0, len(msg)-1)]

    def mass(self, event):
        if (event.totalWeight > 2):
            if self._measureCnt < WEIGHT_SAMPLES:
                if self._measureCnt == 1:
                    self.streamer.log("Update", "Measuring ...")
                    self.streamer.flush()

                if METRIC_UNITS:
                    self._events[self._measureCnt] = event.totalWeight
                    self._unit = "kg"
                else:
                    self._events[self._measureCnt] = event.totalWeight*2.20462
                    self._unit = "lb"
                self._measureCnt += 1
                if self._measureCnt == WEIGHT_SAMPLES:

                    # Average multiple measurements to get the weight and stream it
                    self._prevWeight = self._weight
                    self._sum = 0
                    for x in range(THROWAWAY_SAMPLES, WEIGHT_SAMPLES-1):
                        self._sum += self._events[x]
                    self._weight = self._sum/(WEIGHT_SAMPLES-THROWAWAY_SAMPLES)
                    if self._measured:
                        self._weightChange = self._weight - self._prevWeight
                        if self._weightChange < -0.4:
                            self._msg = self.messageWeighLess(self._weight, self._weightChange, self._unit)
                        elif self._weightChange > 0.4:
                            self._msg = self.messageWeighMore(self._weight, self._weightChange, self._unit)
                        else:
                            self._msg = self.messageWeighSame(self._weight, self._weightChange, self._unit)
                    else:
                        self._msg = self.messageWeighFirst(self._weight, self._unit)
                    print self._msg
                    self.streamer.log("Update", self._msg)
                    tmpVar = "Weight(" + self._unit + ")"
                    self.streamer.log(str(tmpVar), float("{0:.2f}".format(self._weight)))
                    tmpVar = time.strftime("%x %I:%M %p")
                    self.streamer.log("Weigh Date", tmpVar)
                    self.streamer.flush()

                    # Store a small history of weights and overwite any measurement less than 2 hours old (7200 seconds)
                    if self._weightCnt > 0:
                        if (time.time() - self._times[self._weightCnt-1]) < 7200:
                            self._tmpVar = time.time() - self._times[self._weightCnt-1]
                            self._weightCnt -= 1
                    self._weights[self._weightCnt] = self._weight
                    self._times[self._weightCnt] = time.time()
                    self._weightCnt += 1
                    # Send an extra update at the end of WEIGHT_HISTORY
                    if self._weightCnt == WEIGHT_HISTORY:
                        self._weightCnt = 0
                        self._weightChange = self._weights[WEIGHT_HISTORY-1] - self._weights[0]
                        self._weightChange = float("{0:.2f}".format(self._weightChange))
                        timeChange = (self._times[WEIGHT_HISTORY-1] - self._times[0])/86400
                        timeChange = float("{0:.1f}".format(timeChange))
                        if self._weightChange > 0:
                            self._msg = "🕒 You gained " + str(self._weightChange) + " " + self._unit + " in the last " + str(timeChange) + " days!"
                        else:
                            self._msg = "🕒 You lost " + str(abs(self._weightChange)) + " " + self._unit + " in the last " + str(timeChange) + " days!"
                        self.streamer.log("Update", self._msg)
                        self.streamer.flush()

                    # Keep track of the first complete measurement
                    if not self._measured:
                        self._measured = True
        else:
            self._measureCnt = 0

    @property
    def weight(self):
        if not self._events:
            return 0
        histogram = collections.Counter(round(num, 1) for num in self._events)
        return histogram.most_common(1)[0][0]


class BoardEvent:
    def __init__(self, topLeft, topRight, bottomLeft, bottomRight, buttonPressed, buttonReleased):

        self.topLeft = topLeft
        self.topRight = topRight
        self.bottomLeft = bottomLeft
        self.bottomRight = bottomRight
        self.buttonPressed = buttonPressed
        self.buttonReleased = buttonReleased
        #convenience value
        self.totalWeight = topLeft + topRight + bottomLeft + bottomRight

class Wiiboard:
    def __init__(self, processor):
        # Sockets and status
        self.receivesocket = None
        self.controlsocket = None

        self.processor = processor
        self.calibration = []
        self.calibrationRequested = False
        self.LED = False
        self.address = None
        self.buttonDown = False
        for i in xrange(3):
            self.calibration.append([])
            for j in xrange(4):
                self.calibration[i].append(10000)  # high dummy value so events with it don't register

        self.status = "Disconnected"
        self.lastEvent = BoardEvent(0, 0, 0, 0, False, False)

        try:
            self.receivesocket = bluetooth.BluetoothSocket(bluetooth.L2CAP)
            self.controlsocket = bluetooth.BluetoothSocket(bluetooth.L2CAP)
        except ValueError:
            raise Exception("Error: Bluetooth not found")

    def isConnected(self):
        return self.status == "Connected"

    # Connect to the Wiiboard at bluetooth address <address>
    def connect(self, address):
        if address is None:
            print "Non existant address"
            return
        self.receivesocket.connect((address, 0x13))
        self.controlsocket.connect((address, 0x11))
        if self.receivesocket and self.controlsocket:
            print "Connected to Wiiboard at address " + address
            self.status = "Connected"
            self.address = address
            self.calibrate()
            useExt = ["00", COMMAND_REGISTER, "04", "A4", "00", "40", "00"]
            self.send(useExt)
            self.setReportingType()
            print "Wiiboard connected"
        else:
            print "Could not connect to Wiiboard at address " + address

    def receive(self):
        while self.status == "Connected" and not self.processor.done:
            data = self.receivesocket.recv(25)
            intype = int(data.encode("hex")[2:4])
            if intype == INPUT_STATUS:
                # TODO: Status input received. It just tells us battery life really
                self.setReportingType()
            elif intype == INPUT_READ_DATA:
                if self.calibrationRequested:
                    packetLength = (int(str(data[4]).encode("hex"), 16) / 16 + 1)
                    self.parseCalibrationResponse(data[7:(7 + packetLength)])

                    if packetLength < 16:
                        self.calibrationRequested = False
            elif intype == EXTENSION_8BYTES:
                self.processor.mass(self.createBoardEvent(data[2:12]))
            else:
                print "ACK to data write received"

    def disconnect(self):
        if self.status == "Connected":
            self.status = "Disconnecting"
            while self.status == "Disconnecting":
                self.wait(100)
        try:
            self.receivesocket.close()
        except:
            pass
        try:
            self.controlsocket.close()
        except:
            pass
        print "WiiBoard disconnected"

    # Try to discover a Wiiboard
    def discover(self):
        print "Press the red sync button on the board now"
        address = None
        bluetoothdevices = bluetooth.discover_devices(duration=6, lookup_names=True)
        for bluetoothdevice in bluetoothdevices:
            if bluetoothdevice[1] == BLUETOOTH_NAME:
                address = bluetoothdevice[0]
                print "Found Wiiboard at address " + address
        if address is None:
            print "No Wiiboards discovered."
        return address

    def createBoardEvent(self, bytes):
        buttonBytes = bytes[0:2]
        bytes = bytes[2:12]
        buttonPressed = False
        buttonReleased = False

        state = (int(buttonBytes[0].encode("hex"), 16) << 8) | int(buttonBytes[1].encode("hex"), 16)
        if state == BUTTON_DOWN_MASK:
            buttonPressed = True
            if not self.buttonDown:
                print "Button pressed"
                self.buttonDown = True

        if not buttonPressed:
            if self.lastEvent.buttonPressed:
                buttonReleased = True
                self.buttonDown = False
                print "Button released"

        rawTR = (int(bytes[0].encode("hex"), 16) << 8) + int(bytes[1].encode("hex"), 16)
        rawBR = (int(bytes[2].encode("hex"), 16) << 8) + int(bytes[3].encode("hex"), 16)
        rawTL = (int(bytes[4].encode("hex"), 16) << 8) + int(bytes[5].encode("hex"), 16)
        rawBL = (int(bytes[6].encode("hex"), 16) << 8) + int(bytes[7].encode("hex"), 16)

        topLeft = self.calcMass(rawTL, TOP_LEFT)
        topRight = self.calcMass(rawTR, TOP_RIGHT)
        bottomLeft = self.calcMass(rawBL, BOTTOM_LEFT)
        bottomRight = self.calcMass(rawBR, BOTTOM_RIGHT)
        boardEvent = BoardEvent(topLeft, topRight, bottomLeft, bottomRight, buttonPressed, buttonReleased)
        return boardEvent

    def calcMass(self, raw, pos):
        val = 0.0
        #calibration[0] is calibration values for 0kg
        #calibration[1] is calibration values for 17kg
        #calibration[2] is calibration values for 34kg
        if raw < self.calibration[0][pos]:
            return val
        elif raw < self.calibration[1][pos]:
            val = 17 * ((raw - self.calibration[0][pos]) / float((self.calibration[1][pos] - self.calibration[0][pos])))
        elif raw > self.calibration[1][pos]:
            val = 17 + 17 * ((raw - self.calibration[1][pos]) / float((self.calibration[2][pos] - self.calibration[1][pos])))

        return val

    def getEvent(self):
        return self.lastEvent

    def getLED(self):
        return self.LED

    def parseCalibrationResponse(self, bytes):
        index = 0
        if len(bytes) == 16:
            for i in xrange(2):
                for j in xrange(4):
                    self.calibration[i][j] = (int(bytes[index].encode("hex"), 16) << 8) + int(bytes[index + 1].encode("hex"), 16)
                    index += 2
        elif len(bytes) < 16:
            for i in xrange(4):
                self.calibration[2][i] = (int(bytes[index].encode("hex"), 16) << 8) + int(bytes[index + 1].encode("hex"), 16)
                index += 2

    # Send <data> to the Wiiboard
    # <data> should be an array of strings, each string representing a single hex byte
    def send(self, data):
        if self.status != "Connected":
            return
        data[0] = "52"

        senddata = ""
        for byte in data:
            byte = str(byte)
            senddata += byte.decode("hex")

        self.controlsocket.send(senddata)

    #Turns the power button LED on if light is True, off if False
    #The board must be connected in order to set the light
    def setLight(self, light):
        if light:
            val = "10"
        else:
            val = "00"

        message = ["00", COMMAND_LIGHT, val]
        self.send(message)
        self.LED = light

    def calibrate(self):
        message = ["00", COMMAND_READ_REGISTER, "04", "A4", "00", "24", "00", "18"]
        self.send(message)
        self.calibrationRequested = True

    def setReportingType(self):
        bytearr = ["00", COMMAND_REPORTING, CONTINUOUS_REPORTING, EXTENSION_8BYTES]
        self.send(bytearr)

    def wait(self, millis):
        time.sleep(millis / 1000.0)


def main():
    processor = EventProcessor()

    board = Wiiboard(processor)
    if len(sys.argv) == 1:
        print "Discovering board..."
        address = board.discover()
    else:
        address = sys.argv[1]

    try:
        # Disconnect already-connected devices.
        # This is basically Linux black magic just to get the thing to work.
        subprocess.check_output(["bluez-test-input", "disconnect", address], stderr=subprocess.STDOUT)
        subprocess.check_output(["bluez-test-input", "disconnect", address], stderr=subprocess.STDOUT)
    except:
        pass

    print "Trying to connect..."
    board.connect(address)  # The wii board must be in sync mode at this time
    board.wait(200)
    # Flash the LED so we know we can step on.
    board.setLight(False)
    board.wait(500)
    board.setLight(True)
    board.receive()

if __name__ == "__main__":
    main()
