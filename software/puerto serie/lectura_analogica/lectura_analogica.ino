void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

}

void loop() {
  // put your main code here, to run repeatedly:
  float sensorValue = analogRead(A0);
  float voltaje = 6*sensorValue/1024 ;
  
  Serial.println(voltaje);
  Serial.flush();

  delay(100);

}
