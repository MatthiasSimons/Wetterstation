import machine
from machine import Pin, I2C
from time import sleep
import BME280
import network
import urequests
import gc

#ssid und passwort eingeben
ssid = "****"
password = "****"

#Ort auskommentieren
ort = "Euskirchen"
#ort = "Muetzenich"
#ort = "Schmidt"

api_key = "hx4Kost4kKLMu-9-op7_8HdBTOMJVSljQShm7W_fJsb"
post = "https://maker.ifttt.com/trigger/"+ort+"/with/key/hx4Kost4kKLMu-9-op7_8HdBTOMJVSljQShm7W_fJsb"

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print("connection successful")
print(station.ifconfig())
print('waiting 10 s')
sleep(10)

i2c = I2C(scl=Pin(5), sda=Pin(4), freq=10000)

while True:
  try:
    #Messwerte auslesen
    bme = BME280.BME280(i2c=i2c)
    temp = bme.temperature
    hum = bme.humidity
    pres = bme.pressure
    #Messwerte in Dictionary speichern
    sensore_readings = {"value1": temp, "value2": hum, "value3": pres}
    
    #mit IFTTT API verbinden und Request mit Messwerten senden
    request_headers = {"Content-Type": "application/json"}
    request = urequests.post(
    "http://maker.ifttt.com/trigger/"+ort+"/with/key/"+api_key,
    json=sensore_readings,
    headers = request_headers)
    request.close()  
    
    # Deep Sleep
    rtc = machine.RTC()
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)

    if machine.reset_cause() == machine.DEEPSLEEP_RESET:

      print('woke from a deep sleep')
    rtc.alarm(rtc.ALARM0, 3600000)
    machine.deepsleep()

  except OSError as e:
    print("Failed to read/publish sensor readings.")















