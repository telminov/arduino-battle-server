#include <Servo.h>

const int MOTOR_PIN = 3;
const int SERVO_PIN = 9;

boolean isMoveForward = 0;
boolean isMoveBackward = 0;
boolean isMoveLeft = 0;
boolean isMoveRight = 0;

Servo servo;

void comply() {
  if (isMoveForward)
    moveForward();
//  else if (isMoveBackward)
//    moveBackward();
  else
    stopMoving();

  if (isMoveLeft) 
    left();
  else if (isMoveRight)
    right();
  else
    center ();
}

void setup() {
  Serial.begin(9600);
  servo.attach(SERVO_PIN);
  pinMode(MOTOR_PIN, OUTPUT);
}

char command[4] = "";
int i = 0;

void loop() {
//  moveForward();
  if (Serial.available() > 0 ) {
    char ch = Serial.read();
    if (ch == '\n') {
      processCommand();
      clearCommand();
      i = 0;
    } else {
      command[i] = ch;
      i++;
    }
  }
  
}

void processCommand() {
  Serial.println(command);
  
  isMoveForward = command[0] == '1';
  isMoveBackward = command[1] == '1';
  isMoveLeft = command[2] == '1';
  isMoveRight = command[3] == '1';
  
  comply();
}

void moveForward() {
//  analogWrite(MOTOR_PIN, 200);
  digitalWrite(MOTOR_PIN, HIGH);
}

void stopMoving() {
  analogWrite(MOTOR_PIN, 0);
}

void left() {
  servo.write(40);
};
void center() {
  servo.write(90);
};
void right() {
  servo.write(140);
};

void clearCommand() {
  for (int i = 0; i < 4; i++) {
    command[i] = '0';
  }
}

