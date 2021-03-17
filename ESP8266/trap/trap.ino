#include <ESP8266WiFi.h>
#include <PubSubClient.h>
 
const char* SSID = "WtfNet666";
const char* PSK = "AJSabf2015";
const char* MQTT_BROKER = "192.168.22.27";
 
WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;
int loopvalue = 0;

const int buttonPin = 5; 
 
void setup() {
    Serial.begin(115200);
    pinMode(buttonPin, INPUT);
    setup_wifi();
    client.setServer(MQTT_BROKER, 1883);
}
 
void setup_wifi() {
    delay(10);
    Serial.println();
    Serial.print("Connecting to ");
    Serial.println(SSID);
 
    WiFi.begin(SSID, PSK);
 
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
 
    Serial.println("");
    Serial.println("WiFi connected");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());
    
}
 
void reconnect() {
    while (!client.connected()) {
        Serial.print("Reconnecting...");
        if (!client.connect("ESP8266Client")) {
            Serial.print("failed, rc=");
            Serial.print(client.state());
            Serial.println(" retrying in 5 seconds");
            delay(5000);
        }
    }
}
void loop() {

    bool action = false;
    if (!client.connected()) {
        reconnect();
    }
    client.loop();

    loopvalue = loopvalue +1;

    if(loopvalue >= 60){
      client.publish("/mousetrap/1", "TRAPALIVE");
      loopvalue = 0;
    }


    int buttonState = digitalRead(buttonPin);
  // check if the pushbutton is pressed.
  // if it is, the buttonState is HIGH
  if (buttonState == HIGH) {
    client.publish("/mousetrap/1", "MOVE");
    action = true;
  }

  if(action){
    delay(60000);
  }else{
    delay(500);
  }
}
