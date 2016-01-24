#include <Servo.h> 

const int SERVO=10; //упр сервоприводом

const int EN=9;   //вход включ двигателя  подается разное напряжение для упр мощностью МОтора
const int MC1=3;  //контроль 1 h-мостом
const int MC2=2;  //контроль 2 h-мостом

Servo myServo; //делаем инстанс класса Servo, чтоб с ним работать
int servoVal = 90; // колеса установим в 90 , чтоб потом крутить колеса влево и вправо

void setup()
{   
  //мотор
  pinMode(EN, OUTPUT);
  pinMode(MC1, OUTPUT);
  pinMode(MC2, OUTPUT);
  brake(); //стопорим двигатель 
  
  // сервопривод
  myServo.attach(SERVO); //нашему инстансу сообщаем, что им управляет 9 порт
  myServo.write(servoVal); //установим в 90 , чтоб потом крутить колеса влево и вправо(диапозон 0-180 градусов)

  Serial.begin(9600); //скорость соединения с com портом
}

// void ServoTurnLeft(int servoVal);уточнить как в с++ или нет
// void ServoTurnRight(int servoVal);

void loop()

 if (Serial.available() > 0) // если что-то пришло с com порта
 {
  switch (Serial.read() ) //читаем переменную (по 1 символу) с порта
  { 
    case: 'w'
    {
      int power_motor = 50; // возможно задать переменную для увеличения скорости
      MotorGo(power_motor);
    }
  
    case: 's'
    {
      int power_motor = 50; // возможно задать переменную для увеличения скорости
      MotorGoesBack(power_motor);
    }
  
    case: ' '
    {
        MotorBrake();
    }
      
    case: 'd'
    { 
      ServoTurnRight(servoVal);
    }
    case: 's'
    { 
      ServoTurnLeft(servoVal);
    }
  }
  
}

void MotorGo (int powerMotor)
{
    digitalWrite(EN, LOW);
    digitalWrite(MC1, HIGH);
    digitalWrite(MC2, LOW);
    analogWrite(EN, powerMotor);
}

void MotorGoesBack (int powerMotor)
{
    digitalWrite(EN, LOW);
    digitalWrite(MC1, LOW);
    digitalWrite(MC2, HIGH);
    analogWrite(EN, powerMotor);
}

//Stops motor
void MotorBrake ()
{
    digitalWrite(EN, LOW);
    digitalWrite(MC1, LOW);
    digitalWrite(MC2, LOW);
    digitalWrite(EN, HIGH);
}

void ServoTurnRight(int servoVal)
{
  servoVal += 10;
  myServo.write(servoVal);
  delay(15);
}

void ServoTurnLeft(int servoVal)
{
  servoVal -= 10;
  myServo.write(servoVal);
  delay(15);
}

