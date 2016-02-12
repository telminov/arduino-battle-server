#include <Servo.h>

const int MOTOR_PIN = 3;
const int LED_PIN = 5;
const int SERVO_PIN = 9;
const int MIN_SPEED = 1;
const int MAX_SPEED = 3;
const int MAX_COMMAND_LENGTH = 6;

bool isMoveForward = false;
bool isMoveBackward = false;
bool isMoveLeft = false;
bool isMoveRight = false;
bool isLedBlink = false;
int movingSpeed = MAX_SPEED;
char command[MAX_COMMAND_LENGTH] = "";

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
    center();

  if (isHeartBeat)
    blinkLed();
}

void setup() {
  Serial.begin(9600);
  servo.attach(SERVO_PIN);
  pinMode(MOTOR_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  int i = 0;
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
  isLedBlink = command[4] == '1';

  int speed = command[5] - '0';
  if (speed > MIN_SPEED && speed < MAX_SPEED)
      movingSpeed = speed;
  
  comply();
}

void moveForward() {
  if (movingSpeed == 1)
    analogWrite(MOTOR_PIN, 200);
  else if (movingSpeed == 2)
    analogWrite(MOTOR_PIN, 225);
  else
    digitalWrite(MOTOR_PIN, HIGH);
}

void stopMoving() {
  analogWrite(MOTOR_PIN, 0);
}

void left() {
  servo.write(140);
};
void center() {
  servo.write(90);
};
void right() {
  servo.write(40);
};

void clearCommand() {
  for (int i = 0; i < MAX_COMMAND_LENGTH; i++) {
    command[i] = '0';
  }
}

void blinkLed() { 
  analogWrite(LED_PIN, 10);
  delay(50);
  digitalWrite(LED_PIN, LOW);
}

