#include <IRremote.h>

IRrecv irrecv(11);
decode_results results;

void setup()
{
  Serial.begin(9600); // Выставляем скорость COM порта
  irrecv.enableIRIn(); // Запускаем прием
}

void loop() {
  if (irrecv.decode(&results)) // Если данные пришли 
  {
    Serial.println(results.value, HEX); // Отправляем полученную данную в консоль
    irrecv.resume(); // Принимаем следующую команду
  }
}

