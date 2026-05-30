#define CLK 2
#define ADDR 3
#define OUT_ENABLE 4
#define D0 5
#define D1 6
#define D2 7
#define D3 8
#define D4 9
#define D5 10
#define D6 11
#define D7 12

void load_address(unsigned short address) {
  address = address & 0x7FFF;
  for (int i = 0; i < 16; i++) {
    //Setup bit to shift in
    digitalWrite(ADDR, (address >> (15 - i) & 1));
    digitalWrite(CLK, HIGH);
    digitalWrite(CLK, LOW);
  }
}

byte read_data() {
  byte data = 0x00;
  for (int i = D0; i <= D7; i++) {
    data += digitalRead(i) << (i -5);
  }
  return data;
}

void setup() {
  Serial.begin(115200);
  
  //Initialize address pins
  pinMode(CLK, OUTPUT);
  pinMode(ADDR, OUTPUT);
  pinMode(OUT_ENABLE, OUTPUT);
  digitalWrite(OUT_ENABLE, LOW);
  
  //Initialize data pins to input
  for (int i = D0; i <= D7; i++) {
    pinMode(i, INPUT);
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  //Dump ROM
  Serial.print("Start of ROM");
  for (unsigned short address = 0; address < 32768; address++) {
    load_address(address);
    Serial.write(read_data());
  }
  Serial.println("Reached End of ROM");
}
