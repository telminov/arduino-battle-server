
char data; 

void setup()
{
  Serial.begin(9600); #связь с портом
}

void loop()
{
  if (Serial.available() > 0)
  {
    data = Serial.read(); //считывание с порта
    Serial.println(data);   //отправка обратно
  }
}
