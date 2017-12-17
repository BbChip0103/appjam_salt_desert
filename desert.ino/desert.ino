#include <Wire.h>
#define SLAVE 4

void setup() {
  Wire.begin(SLAVE);
  Wire.onRequest(sendValue);
  randomSeed(analogRead(7));
  pinMode(2,OUTPUT);
}

void changeColor(int color[3]);
void loop() {
  int color[3] = {random(225), random(225), random(225)};
  changeColor(color);
  delay(10000);
}

int set[3] = {0,0,0};
int pins[3] = {6,9,11};

void changeColor(int color[3])
{
  if (analogRead(A0) < 150) {
    digitalWrite(2,HIGH);
    if (color[0] + color[1] + color[2] < 20)
    {
      int c[3] = {random(225), random(225), random(225)};
      return changeColor(c);
    }
    else {
      for (int i = 0; i < 3; i ++) {
        
        if (set[i] > color[i]) {
          for (int j = set[i]; j > color[i]; j--) {
            analogWrite(pins[i], j);
            delay(4);
          }
        }
        
        else {
              for (int j = set[i]; j < color[i]; j++) {
              analogWrite(pins[i], j);
              delay(4);
            }
          }
          
        set[i] = color[i];
      
      }
    }
  }
  else
  {
    digitalWrite(2,LOW);
    for (int i = 0; i < 3; i++)
    {
      analogWrite(pins[i], 0);
    }
  }
}

void sendValue() {
  Wire.write((byte)map(analogRead(A3), 0, 300, 0, 255));
}
