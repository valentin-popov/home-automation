
#include <dht.h> 
dht DHT;
int datafromUser=0;
unsigned long timpParcurs;
bool alarm;

int relayPin = 13;
int alarmPin = 12;
int DHTpin = 2;
int buzzerPin = 11;

void setup() {
  pinMode(relayPin, OUTPUT); 
  pinMode(buzzerPin, OUTPUT);
  pinMode(alarmPin, INPUT); 
  pinMode(DHTpin, INPUT); 
  Serial.begin(9600); 
  
}

void loop() {   //se executa incontinuu
  timpParcurs = millis();
  if(Serial.available() > 0)   
  {
    datafromUser=Serial.read(); 
  }
  if (timpParcurs % 1000 == 0) 
  {
    DHT.read11(DHTpin);
    Serial.print(int(DHT.temperature));
    Serial.print(',');
    Serial.println(int(DHT.humidity));
  }

  
  if(datafromUser == '1')
  {
    digitalWrite(relayPin, HIGH );
  }
  else if(datafromUser == '0')
  {
    digitalWrite(relayPin, LOW);
  }

  else if(datafromUser == '2')
  {
    alarm = true;
  }
  else if(datafromUser == '3')
  {
    alarm = false;
  }
    //se trimite semnal HIGH daca intre bratele senzorului exista un obiect.
      //un obiect intre bratele senzorului simuleaza usa inchisa.
      //daca alarma e pornita, difuzorul suna cand usa se deschide, adica
      //atunci cand obiectul iese dintre bratele senzorului
  if (alarm) {
      if (digitalRead(alarmPin) == LOW) {
      tone(buzzerPin, 200);
      delay(200);
      noTone(buzzerPin);
      delay(200);
      
      tone(buzzerPin, 300);
      delay(200);
      noTone(buzzerPin);
      delay(200);
      
      tone(buzzerPin, 400);
      delay(200);
      noTone(buzzerPin);
      delay(200);
      
      tone(buzzerPin, 500);
      delay(200);
      noTone(buzzerPin);
      delay(200);
      while (digitalRead(alarmPin) == LOW);
       //dupa ce a cantat melodia, sistemul asteapta cat timp
      //intre bratele senzorului nu este nimic - cat timp usa e deschisa
    }
  }
}
      
