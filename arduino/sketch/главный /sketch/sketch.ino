// мотор
const int EN1 = 3; // упр 1-ым enA
const int IN1 = 4; // контролер 1 для левого мотора - (певый)
const int IN2 = 5; // контролер 2 для левого мотора

const int EN2 = 6; // упр 1-ым мотором  enB
const int IN3 = 7; // управление вторым мотором
const int IN4 = 8;

int i = 0;

void setup()
{ 
  //выхода для мотора
  for (int i=3; i<=8; i++)
  {
    pinMode (i, OUTPUT);
  }

  //usb порт
  Serial.begin(9600); //скорость соединения с com портом
}

// void MotorGo();
// void MotorGoesBack();
// void MotorBrake();
// void MotorGoesRight();
// void MotorGoesLeft();


void MotorGo ()
{ 
  MotorBrake(); //пока так
  
  digitalWrite (IN2, HIGH);
  digitalWrite (IN1, LOW); 
  digitalWrite (IN4, HIGH);
  digitalWrite (IN3, LOW); 
  for (i = i; i <= 180; +30)
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
  for (i = i; i <= 180; i+=30)
  {
      analogWrite(EN1, i);
      analogWrite(EN2, i);
      delay(10);
  }
}

//Stops motor
void MotorBrake ()
{
  digitalWrite (IN2, HIGH);
  digitalWrite (IN1, LOW); 
  digitalWrite (IN4, HIGH);
  digitalWrite (IN3, LOW); 
  for (i = i; i <= 0; i-=30)
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
  for (i = i; i <= 180; i++)
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
  for (i = i; i <= 180; i++)
  {
      analogWrite(EN1, i);
      analogWrite(EN2, i);
      delay(10);
  }
}


void loop()
{
 if (Serial.available() > 0) // если что-то пришло с com порта
 { 
  char data_port = Serial.read();
  Serial.println(data_port);
  switch (data_port) //читаем переменную (по 1 символу) с порта
  { 
    case 'w':
    {
      MotorGo();
    }
  
    case 's':
    {
      MotorGoesBack();
    }
  
    case ' ':
    {
        MotorBrake();
    }
      
    case 'd':
    { 
      MotorGoesRight();
    }
    case 'a':
    { 
      MotorGoesLeft();
    }
  } 
}
}

