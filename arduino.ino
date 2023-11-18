const int buttonPin = 2;  // Pin number where the button is connected
int lastButtonState = 1;  // Previous state of the button

void setup() {
  Serial.begin(9600);     // Initialize serial communication
  pinMode(buttonPin, INPUT_PULLUP);  // Set the button pin as input with internal pull-up resistor
}

void loop() {
  // Read the state of the button
  int buttonState = digitalRead(buttonPin);

  // Check if the button state has changed to pressed (Falling edge)
  if (buttonState == 0 && lastButtonState == 1) {
    Serial.println("B");
    delay(50);
  }

  // Update the lastButtonState
  lastButtonState = buttonState;
}
