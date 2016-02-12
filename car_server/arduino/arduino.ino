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
int movingSpeed = MAX_SPEED;
bool isLedBlink = false;
char command[MAX_COMMAND_LENGTH] = "";
int commandIndex = 0;

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

  if (isLedBlink)
    blinkLed();
}

void setup() {
  Serial.begin(9600);
  servo.attach(SERVO_PIN);
  pinMode(MOTOR_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT);
}


void loop() {
  if (Serial.available() > 0 ) {
    char ch = Serial.read();
    if (ch == '\n') {
      processCommand();
      clearCommand();
      commandIndex = 0;
    } else {
      command[commandIndex] = ch;
      commandIndex++;
    }
  }
  
}

void processCommand() {
  Serial.println(command);
  
  isMoveForward = command[0] == '1';
  isMoveBackward = command[1] == '1';
  isMoveLeft = command[2] == '1';
  isMoveRight = command[3] == '1';

  int speed = command[4] - '0';
  if (speed > MIN_SPEED && speed < MAX_SPEED)
      movingSpeed = speed;

  isLedBlink = command[5] == '1';
  
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

