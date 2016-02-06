const int MOTOR_PIN = 3;
//const int SERVO_PIN = 9;

boolean isMoveForward = 0;
boolean isMoveBackward = 0;
boolean isMoveLeft = 0;
boolean isMoveRight = 0;


void comply() {
  if (isMoveForward == 1)
    moveForward();
//  else if (isMoveBackward == 1)
//    moveBackward();
  else
    stopMoving();
}

void setup() {
  Serial.begin(9600);

}

char command[4] = "";
int i = 0;

void loop() {
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
  analogWrite(MOTOR_PIN, 150);
}

void stopMoving() {
  analogWrite(MOTOR_PIN, 0);
}

void clearCommand() {
  for (int i = 0; i < 4; i++) {
    command[i] = '0';
  }
}

