#include <IRremote.h>
#include "Ultrasonic.h"

//ir
IRrecv irrecv(11); // Указываем пин, к которому подключен приемник
decode_results results;

// ультразвуковой дальномер
// Trig - 12, Echo - 13
Ultrasonic ultrasonic(12, 13);
int count_iter = 0; //параметр для правильного определения дистанции

// мотор
const int EN1 = 3; // упр 1-ым enA правое
const int IN1 = 2; // контролер 1 для левого мотора - (певый)
const int IN2 = 5; // контролер 2 для левого мотора

const int EN2 = 6; // упр 1-ым мотором  enB левое
const int IN3 = 7; // управление вторым мотором
const int IN4 = 8;

int i;
char cur_data_port = 'z'; //данные с usb порта
char last_data_port = 'z';

//функции управления мотором

void MotorBrake ()
{
  analogWrite(EN1, 0);
  analogWrite(EN2, 0);
  delay(500);
}

void MotorGo ()
{ 
  MotorBrake(); //пока так
  
  digitalWrite (IN2, HIGH);
  digitalWrite (IN1, LOW); 
  digitalWrite (IN4, HIGH);
  digitalWrite (IN3, LOW); 
  for (i = 0; i < 180; i++)
  {
      analogWrite(EN1, i);
      analogWrite(EN2, i);
      delay(10);
  }
}

void MotorGoesBack ()
{ 
  MotorBrake();
  
  digitalWrite (IN2, LOW);
  digitalWrite (IN1, HIGH); 
  digitalWrite (IN4, LOW);
  digitalWrite (IN3, HIGH); 
  for (i = 0; i <= 180; i++)
  {
      analogWrite(EN1, i);
      analogWrite(EN2, i);
      delay(10);
  }
}

void MotorGoesRight()
{
  MotorBrake();

  // проверить! 
  //крутит левое вперед, правое - назад
  digitalWrite (IN2, LOW);
  digitalWrite (IN1, HIGH); 
  
  digitalWrite (IN4, HIGH);
  digitalWrite (IN3, LOW); 
  for (i = 0; i <= 180; i++)
  {
    analogWrite(EN1, i);
    analogWrite(EN2, i);
    delay(10);
  }
}

void MotorGoesLeft()
{
  MotorBrake();

  // проверить! 
  //крутит левое вперед, правое - назад
  digitalWrite (IN2, HIGH);
  digitalWrite (IN1, LOW); 
  
  digitalWrite (IN4, LOW);
  digitalWrite (IN3, HIGH); 
  for (i = 0; i <= 180; i++)
  {
      analogWrite(EN1, i);
      analogWrite(EN2, i);
      delay(10);
  }
}

void SwitchMotors(char cur_data_port) 
{
  switch (cur_data_port) //читаем переменную (по 1 символу) с порта
  { 
    case 'w':
    {
      Serial.println(cur_data_port);
      MotorGo();
       break;
    }
  
    case 's':
    {
      Serial.println(cur_data_port);
      MotorGoesBack();
       break;
    }
  
    case 'b':
    { 
      Serial.println(cur_data_port);
      MotorBrake();
       break;
    }
      
    case 'd':
    { 
      Serial.println(cur_data_port);
      MotorGoesRight();
       break;
    }
    case 'a':
    { 
      Serial.println(cur_data_port);
      MotorGoesLeft();
       break;
    }
  } 
}

void SwitchMotorsByIrSignal(int ir_value)
{
switch (ir_value) //читаем переменную (по 1 символу) с порта
  { 
    case 0xFF18E7:
    {
      Serial.println(cur_data_port);
      MotorGo();
       break;
    }
  
    case 0xFF4AB5:
    {
      Serial.println(cur_data_port);
      MotorGoesBack();
       break;
    }
  
    case 0xFF38C7:
    { 
      Serial.println(cur_data_port);
      MotorBrake();
       break;
    }
      
    case 0xFF5AA5:
    { 
      Serial.println(cur_data_port);
      MotorGoesRight();
       break;
    }
    case 0xFF10EF:
    { 
      Serial.println(cur_data_port);
      MotorGoesLeft();
       break;
    }
  } 
}

void UltrasonicDataSendPort()
{ 
  if (millis() % 1000==0 )
  {
    if (count_iter != 5)
    {
      count_iter += 1;
      // будет массив из 5 чисел, чтоб потом взять среднее число, а очень большое значение отбросить
    }
    else
    {
      count_iter = 0;
      float dist_cm = ultrasonic.Ranging(CM);       // get distance
      Serial.println(dist_cm);                      // print the distance
    }
  }  
}
//------------------------------------------------------------------//
void setup()
{ 
  //выхода для мотора
//  for (int i=2; i<=8; i++)
//  {
//    pinMode (i, OUTPUT);
//  }
  pinMode (IN4, OUTPUT);
  pinMode (IN3, OUTPUT);
  pinMode (IN2, OUTPUT);
  pinMode (IN1, OUTPUT);
  pinMode (EN2, OUTPUT);
  pinMode (EN1, OUTPUT);

  //usb порт
  Serial.begin(9600); //скорость соединения с com портом

  //
  irrecv.enableIRIn(); // Запускаем прием
}

// void MotorGo();
// void MotorGoesBack();
// void MotorBrake();
// void MotorGoesRight();
// void MotorGoesLeft();

//---------------------------------------------//
void loop()
{
  UltrasonicDataSendPort();
  //работа с мотором
 if (irrecv.decode(&results)) // Если данные пришли 
  {
    Serial.println(results.value, HEX); // Отправляем полученную данную в консоль
    SwitchMotorsByIrSignal(results.value);
    irrecv.resume(); // Принимаем следующую команду
  }
  
 if (Serial.available() > 0) // если что-то пришло с com порта
 {    
    char cur_data_port = Serial.read(); 
    if (last_data_port != cur_data_port ) 
    { 
      char last_data_port = cur_data_port;
      SwitchMotors(cur_data_port);
    }
  }
}

