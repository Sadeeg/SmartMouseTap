import paho.mqtt.client as mqttClient
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import datetime
import os

lastmail = {}
emailServer = os.getenv('EMAIL_SERVER')
emailUser = os.getenv('EMAIL_USER')
emailPassword = os.getenv('EMAIL_PASSWORD')
mqttServer = os.getenv('MQTT_SERVER')
to = os.getenv('TO')
print('Configuration')
print('emailServer = '+os.getenv('EMAIL_SERVER'))
print('emailUser ='+ os.getenv('EMAIL_USER'))
print('emailPassword ='+ os.getenv('EMAIL_PASSWORD'))
print('mqttServer ='+ os.getenv('MQTT_SERVER'))
print('to ='+ os.getenv('TO'))
  
def on_connect(client, userdata, flags, rc):
  
    if rc == 0:
  
        print("Connected to broker")
  
        global Connected                #Use global variable
        Connected = True                #Signal connection 
  
    else:
  
        print("Connection failed")

def sendMail(subject, message):
 msg = MIMEMultipart()
 password = emailPassword
 username = emailUser
 smtphost = emailServer
 msg['From'] = username
 msg['To'] = to
 msg['Subject'] = subject
 msg.attach(MIMEText(message, 'plain'))
 server = smtplib.SMTP(smtphost)
 server.starttls()
 server.login(username, password)
 server.sendmail(msg['From'], to.split(','), msg.as_string())
 server.quit()
 print ("Successfully sent email message to %s:" % (msg['To']))
        
def checkAndSendMoveMessage(topic):
    if(topic not in lastmail.keys() or lastmail[topic] < (datetime.datetime.now() - datetime.timedelta(minutes = 5))):
       sendMail("Move in Mousetrap","Move in MouseTrap"+topic);
       lastmail[topic] = datetime.datetime.now()
       print(lastmail[topic])
    
def on_message(client, userdata, message):
    topic = message.topic[11:]
    currentmessage = message.payload.decode("utf-8")
    if currentmessage == "MOVE":
    	checkAndSendMoveMessage(topic)
    print(topic)
    print("Message received: ")
    print(message.payload.decode("utf-8"))
  
Connected = False   #global variable for the state of the connection
  
broker_address= mqttServer  #Broker address
port = 1883                         #Broker port
#user = "yourUser"                    #Connection username
#password = "yourPassword"            #Connection password
  
client = mqttClient.Client("Python")               #create new instance
#client.username_pw_set(user, password=password)    #set username and password
client.on_connect= on_connect                      #attach function to callback
client.on_message= on_message                      #attach function to callback
  
client.connect(broker_address, port=port)          #connect to broker
  
client.loop_start()        #start the loop
  
while Connected != True:    #Wait for connection
    time.sleep(0.1)
  
client.subscribe("/mousetrap/+")
  
try:
    while True:
        time.sleep(1)
  
except KeyboardInterrupt:
    print( "exiting")
    client.disconnect()
    client.loop_stop()
