
return
import netinit # 网络控制
import watch # 离网监控
#import time
import machine
wdt = machine.WDT(timeout=8000)
print("sta")
def initNet():
    try:
        client = netinit.initNet(wdt)
        return client
    except:
        print('main network err')

mqttClient = initNet()
# 用rtc实现
count1 = 0
count2 = 0

def callback(t):
    global count1
    global count2
    count1 = count1 + 1
    count2 = count2 + 1
    try:
        netinit.subscribeSwitch()
        if count1 == 25:
            #print("count1：40")
            netinit.uploadDeviceInfo()
            count1 = 0
        wdt.feed()
    except:
        print('main update error uploadDeviceInfo')
    if count2 == 8000:
        #print("count2：801")
        count2 = 0
        callback2()
    


def callback2():
    watch.autoWater(mqttClient)
    

tim0 = machine.Timer()

tim0.init(period = 2500,mode = machine.Timer.PERIODIC,callback=callback)

