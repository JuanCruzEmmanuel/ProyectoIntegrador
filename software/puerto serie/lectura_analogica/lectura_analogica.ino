#include <SoftwareSerial.h>


SoftwareSerial miBT(10,12); //creo un objeto para disponer de tx y rx 


#define alpha 0.1
double suavizado =0;
float filtro = 0;
double suavizado2 =0;
float filtro2 = 0;
class  FilterBuLp2
{
  public:
    FilterBuLp2()
    {
      v[0]=0.0;
      v[1]=0.0;
      v[2]=0.0;
    }
  private:
    float v[3];
  public:
    float step(float x) //class II 
    {
      v[0] = v[1];
      v[1] = v[2];
      v[2] = (2.008336556421122521e-2 * x) + (-0.64135153805756306422 * v[0]) + (1.56101807580071816339 * v[1]);
    return (v[0] + v[2]) + 2 * v[1];
    }
};
FilterBuLp2 f;


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  miBT.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  float sensorValue = analogRead(A0);
  filtro = f.step(sensorValue);
  suavizado = (alpha*sensorValue) + ((1-alpha)*suavizado);
  miBT.println(filtro);
  float sensorValue2 = analogRead(A1);
  filtro2 = f.step(sensorValue2);
  suavizado2 = (alpha*sensorValue2) + ((1-alpha)*suavizado2);
  miBT.println(filtro2);
 
  
  miBT.flush();

  delay(100);

}
