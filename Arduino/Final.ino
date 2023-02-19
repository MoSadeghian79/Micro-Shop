#include <Stepper.h>
#include <Servo.h>

#define STEPS 100

Stepper stepperX(STEPS, 2, 3, 4, 5);
Stepper stepperY(STEPS, 8, 9, 10, 11);
Servo myservo; 
int pos = 0;

void servoKala(int t){

   int deg = 0; // fisrt degree
   myservo.write(deg);
   for (int i=0;i<t;i++){
    
      for (deg = 0; deg <= 90; deg += 1) { // goes from 0 degrees to 90 degrees
      // in steps of 1 degree
      myservo.write(deg);              // tell servo to go to position in variable 'deg'
      delay(15);                       // waits 15ms for the servo to reach the position
      }
      for (deg = 90; deg >= 0; deg -= 1) { // goes from 90 degrees to 0 degrees
      // in steps of 1 degree
      myservo.write(deg);              // tell servo to go to position in variable 'deg'
      delay(15);                       // waits 15ms for the servo to reach the position
      }  
   }
   
  return ;
}


void move(int x,int y,int t){

  stepperX.step(x*STEPS);
  stepperY.step(y*STEPS);
  servoKala(t);
  stepperX.step(-x*STEPS);
  stepperY.step(-y*STEPS);
  
}


void setup() {

  Serial.begin(9600);
  stepperX.setSpeed(30);
  stepperY.setSpeed(30);
  myservo.attach(6);
  
}
void loop() {

  String tmp0 = Serial.readStringUntil("-");
  int a = tmp0.toInt();
  for (int i=0;i<a;i++){
    
    String tmp1 = Serial.readStringUntil("-");
    String tmp2 = Serial.readStringUntil("-");
    int b = tmp1.toInt();
    int c = tmp2.toInt();

    int x = (int) b/5 + 1;
    int y = b%5;
    if (b % 5 == 0)
      y = 5;
    move(x,y,c);

    delay(100);
    
  }
    Serial.print("hoora");
    delay(1000);
  
}
