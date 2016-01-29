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
}

// void MotorGo();
// void MotorGoesBack();
// void MotorBrake();
// void MotorGoesRight();
// void MotorGoesLeft();

//---------------------------------------------//
void loop()
{  
 if (Serial.available() > 0) // если что-то пришло с com порта
 {    
    char cur_data_port = Serial.read();
    Serial.print(last_data_port);
    Serial.print(cur_data_port);
    Serial.println('w');
    if (last_data_port != cur_data_port ) 
    { 
      char last_data_port = cur_data_port;
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
  }
}

