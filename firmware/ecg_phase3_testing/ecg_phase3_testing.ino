/*
 * CardioSense ECG acquisition test
 *
 * Reads the AD8232 analogue output using an ESP32 and
 * prints the samples through Serial for visualization.
 */

const int ECG_PIN = 36;   // AD8232 OUTPUT -> ESP32 GPIO36 (VP)
const int LO_PLUS = 32;   // AD8232 LO+ -> ESP32 GPIO32
const int LO_MINUS = 35;  // AD8232 LO- -> ESP32 GPIO35

void setup() {
  Serial.begin(115200);

  pinMode(LO_PLUS, INPUT);
  pinMode(LO_MINUS, INPUT);

  Serial.println("AD8232 ECG Test Started");
}

void loop() {
  // A HIGH signal indicates that an electrode lead is disconnected.
  if (digitalRead(LO_PLUS) == HIGH ||
      digitalRead(LO_MINUS) == HIGH) {
    Serial.println("Leads Off");
  } else {
    int ecgValue = analogRead(ECG_PIN);
    Serial.println(ecgValue);
  }

  // Approximately 200 samples per second.
  delay(5);
}
