#include <OneWire.h>
#include <DallasTemperature.h>

//28FF6C4C6D140489
/********************************************************
 * PID Basic Example
 * Reading analog input 0 to control analog PWM output 3
 ********************************************************/

#include <PID_v1.h>

#define PIN_INPUT 0
#define PIN_OUTPUT 9

// Data wire is conntec to the Arduino digital pin 4
#define ONE_WIRE_BUS 2
#define TEMPERATURE_PRECISION 9


//Define Variables we'll be connecting to
double Setpoint, Input, Output;

//Specify the links and initial tuning parameters
double Kp=1, Ki=2, Kd=0;
PID myPID(&Input, &Output, &Setpoint, Kp, Ki, Kd, DIRECT);


// Setup a oneWire instance to communicate with any OneWire devices
OneWire oneWire(ONE_WIRE_BUS);

// Pass our oneWire reference to Dallas Temperature sensor 
DallasTemperature sensors(&oneWire);

// arrays to hold device addresses
DeviceAddress insideThermometer = { 0x28, 0xFF, 0x6C, 0x4C, 0x6D, 0x14, 0x04, 0x89 };
// Assign address manually. The addresses below will need to be changed
// to valid device addresses on your bus. Device address can be retrieved
// by using either oneWire.search(deviceAddress) or individually via
// sensors.getAddress(deviceAddress, index)
// DeviceAddress insideThermometer = { 0x28, 0x1D, 0x39, 0x31, 0x2, 0x0, 0x0, 0xF0 };
// DeviceAddress outsideThermometer   = { 0x28, 0x3F, 0x1C, 0x31, 0x2, 0x0, 0x0, 0x2 };


int compt =0;


void setup() {

    // set the resolution to 9 bit per device
  sensors.setResolution(insideThermometer, TEMPERATURE_PRECISION);
  // Start serial communication for debugging purposes
  Serial.begin(9600);
  // Start up the library
  sensors.begin();
  //initialize the variables we're linked to
  Input =  sensors.getTempCByIndex(0);
  Setpoint = 60;

  //turn the PID on
  myPID.SetMode(AUTOMATIC);


  
}

void loop() {
  // Call sensors.requestTemperatures() to issue a global temperature and Requests to all devices on the bus
  sensors.requestTemperatures(); 
  
  Input = sensors.getTempC(insideThermometer);
 // Input = analogRead(PIN_INPUT);
  myPID.Compute();
  analogWrite(PIN_OUTPUT, Output);
  // read the input on analog pin 0:
  int sensorValue = analogRead(A0);



  delay(10);
  compt++;
  if (compt == 10){
      // print out the value you read:
   Serial.print(Setpoint);
  Serial.print("  ");
  
  Serial.print(Output);
  Serial.print("  ");
  
  Serial.print(Input);
  Serial.print("  ");
  Serial.println(sensorValue);   
  compt = 1;
    }
  
}
