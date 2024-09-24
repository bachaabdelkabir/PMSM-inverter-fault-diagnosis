const int Pin_inline_current_Phase1=0;
const int Pin_inline_current_Phase2=1;
const int Pin_DC_Bus_Voltage=2;
const int Pin_DC_Bus_Current=3;
const int Pin_Temperature_HBridge1=4;
const int Pin_Temperature_HBridge2=5;
const int Pin_Temperature_HBridge3=6;
const int Pin_Driver_voltage=7;



void setup() {
  // put your setup code here, to run once:
Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
int inline_current_Phase1= analogRead(Pin_inline_current_Phase1);
int inline_current_Phase2= analogRead(Pin_inline_current_Phase2);
int DC_Bus_Voltage= analogRead (Pin_DC_Bus_Voltage);
int DC_Bus_Current= analogRead(Pin_DC_Bus_Current);
int Temperature_HBridge1= analogRead(Pin_Temperature_HBridge1);
int Temperature_HBridge2= analogRead(Pin_Temperature_HBridge2);
int Temperature_HBridge3= analogRead(Pin_Temperature_HBridge3);
int Driver_voltage= analogRead(Pin_Driver_voltage);


Serial.print(inline_current_Phase1);
Serial.print("  ");
Serial.print(inline_current_Phase2);
Serial.print("  ");
Serial.print(DC_Bus_Voltage);
Serial.print("  ");
Serial.print(DC_Bus_Current);
Serial.print("  ");
Serial.print(Temperature_HBridge1);
Serial.print("  ");
Serial.print(Temperature_HBridge2);
Serial.print("  ");
Serial.print(Temperature_HBridge3);
Serial.print("  ");
Serial.print(Driver_voltage);
Serial.println("  ");
delay(100);

}
