const int LED_PIN = 13;
const int BUZZER_PIN = 3;
const int rotaryPin = A0;
const int irPin = 2;

void setup() {
  Serial.begin(9600);
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(rotaryPin, INPUT);
  pinMode(irPin, INPUT);
}

void loop() {
  int r = analogRead(rotaryPin);
  int timeLimit = map(r, 0, 1023, 5, 60);

  int irState = digitalRead(irPin);

  Serial.print("Time_Limit:");
  Serial.println(timeLimit);

  Serial.print("Window_Status:");
  Serial.println(irState);

  if (Serial.available() > 0) {
    char command = Serial.read();

    if (command == 'H') {
      digitalWrite(LED_PIN, HIGH);
      digitalWrite(BUZZER_PIN, HIGH);
    } 
    else if (command == 'L') {
      digitalWrite(LED_PIN, LOW);
      digitalWrite(BUZZER_PIN, LOW);
    }
  }
  delay(1000);
}
