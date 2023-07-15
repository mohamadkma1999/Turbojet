
import math
import matplotlib.pyplot as plt
from ambiance import Atmosphere


Alt = input("Enter alt : ")
V=float(input("Enter Air speed with m/s :"))
ma = float(input ("Enter Airflow mass rate : "))
QR = float(input("Enter Fuel reaction heat : "))
PRC = float(input("Enter pressure ratio of the compressor : "))
PRF = float(input("Enter pressure ratio of the Fan : "))
PDC = float(input("Enter Pressure drop in the combustion chamber(bar): "))
B = float(input("Entar bypass ratio : "))
EI = float(input("Enter inlet efficiency : "))
IEF = float(input("Enter Isentropic efficiency of the Fan : "))
IEC = float(input("Enter Isentropic efficiency of the compressor: "))
IECC = float(input("Enter Isentropic  efficiency in the Combustion chamber: "))
ITE = float(input("Enter Isentropic turbine efficiency : "))
IEN = float(input("Enter Isentropic efficiency Nozzle : "))
Q = int(input("Do you want to enter the fuel flow rate or the static temperature of the combustion chamber outlet? 1 _ fuel flow rate / 2 _ static Temprature "))

if Q == 1 :
    mf = float(input("Entar Fuel flow rate : "))
    
elif Q == 2 :
    T04= float(input("Entar static trmptrature of the combustion chamber outlet : ")) 


atmosphere = Atmosphere([Alt])
Ta= atmosphere.temperature
Pa = atmosphere.pressure
C = atmosphere.speed_of_sound


M=V/C
R=287
g = 1.4
gh = 1.33
Pa=Pa[0]
Ta=Ta[0]
float(Pa)
float(M)
CPh = 1148
CPc = 1005


mc = B*ma/(1+B)
mh = ma-mc

print("air pressure : ",Pa)
print("air temperature : ",Ta)

 # Intake or Inlet
P0 = Pa*((1+((g-1)/2)*(M**2))**(g/(g-1)))
P01 = P0
P02 = Pa*((1+EI*((g-1)/2)*(M**2))**(g/(g-1)))
T0 = Ta*(1+((g-1)/2)*(M**2))
T02=T01=T0


# Forward fan

P08 = P02 * PRF
T08 =T02 * (1+(1/IEF)*(PRF**((g-1)/g)-1))


# Compressor
    
P03 = P08 * PRC
T03 = T08 * (1+(1/IEC)*(PRC**((g-1)/g)-1))
    

# Combustion 


P04 = P03 - PDC*10**5

if Q == 1 :
    f = mf/mh
    
    T04 = (ma*CPc*T03 +IECC*mf*QR)/mh*(1+f)*CPh

elif Q == 2 :
    f = ((mh*CPc*T03)-(mh*CPh*T04))/((CPh*T04*mh)-(mh*QR*IECC))

    mf = f*mh

#Turbine
T05 = T04 - ((CPh)*(T03-T08)+(1+B*(T08-T02)))/CPh*(1+f);
P05 = P04 * (1 - (1 / ITE) * (1 - (T05 / T04)))**(gh / (gh - 1));



# Turbine Nozzle

P06 = P05
T06 = T05

PC = P06*((1-(1/IEN)*((gh-1)/(gh+1)))**(gh/(gh-1)))

if PC > Pa :
    Hot_Nazel_status = "The nozzle is choked"
    P7 = Pa
    T7 = (2*T06)/(gh+1)
    V7 =math.sqrt(gh*R*T7)

else:
    Hot_Nazel_status = "The HOT nozzle is unchoked"
    P7 = PC
    V7 = math.sqrt(2*CPh*T06*IEN*(1-((Pa/P06)**((gh-1)/gh))))
    T7 = (2*T06)/(gh+1)
    
    
# Fan Nozzle
PC = P08*((1-(1/IEF)*((g-1)/(g+1)))**(g/(g-1)))

if PC > Pa : 
    Cold_Nazel_status = "The cold nozzle is choked"
    P9 = Pa
    T9 = (2*T08)/(g+1)
    V9 =math.sqrt(g*R*T9)
    
else: 
    cold_Nazel_status = "The cold nozzle is unchoked"
    P9 = PC
    V9 = math.sqrt((2*g*R*T08*IEF)/(g-1)*(1-((Pa/P08)**((g-1)/g))))
    T9 = (2*T08)/(g+1)
    


# Calculate the hot nozzle area
Rho7 = P7/(R*T7)
A7 = (mh+mf)/(Rho7*V7)
R7 = math.sqrt(A7/math.pi)
D7 = 2 * R7

# Calculate the cold nozzle area
Rho9 = P9/(R*T9)
A9 = (mc)/(Rho9*V9)
R9 = math.sqrt((A7+A9)/(math.pi))
D9= 2 * R9

# Thrust
meh = mf+mh

T = meh*V7+mc*V9 - ma*V + (P7-Pa)*A7 + (P9 - Pa)*A9


TSFC = mf /T


# #print
print("Inlet")
print("P0 : ", P0)
print("P01 : ", P01)
print("P02 : ",P02)
print("T0 : ",T0)
print("T01 : ",T01)
print("T02 : ",T02)
print(" ")

print("Fan")
print("P08 : ",P08)
print("T08 : ",T08)
print(" ")

print("Compressor")
print("P03 : ",P03)
print("T03 : ",T03)
print("  ")

print("Combustion")
print("P04 : ",P04)
print("T04 : ",T04)
print("f : ",f)
print("  ")

print("Turbine")
print("P05 : ",P05)
print("T05 : ",T05)
print(" ")

print("Hot Nozzle")
print(Hot_Nazel_status)
print("P7: ",P7)
print("V7 : ",V7)
print("T7 : ",T7)
print("  ")

print("Cold nozzle")
print(cold_Nazel_status)
print("P9: ",P9)
print("V9 : ",V9)
print("T9 : ",T9)
print("  ")

print("Thrust")
print("Hot nozzle area : ",A7)
print("Hot nozzle Dimeter : ", D7)
print("cold nozzle area : ",A9)
print("cold nozzle Dimeter : ", D9)
print("  ")
print("Thrust : ",T)
print("TSFC : ",TSFC)


S2 = CPc*math.log(T02/Ta) - R*math.log(P02/Pa)
S3 = CPc*math.log(T03/T02) - R*math.log(P03/P02)+ S2
S4 = CPc*math.log(T04/T03) - R*math.log(P04/P03)+ S3
S5 = CPc*math.log(T05/T04) - R*math.log(P05/P04)+ S4

S7 = CPc*math.log(T7/T06) - R*math.log(P7/P06)+ S5
S8 = CPc*math.log(T08/T02) - R*math.log(P08/P02)+ S2
S9 = CPc*math.log(T9/T08) - R*math.log(P9/P08)+ S8

S = [S2 , S3 ,S4 , S5  , S7]
T = [T02 , T03 , T04 , T05 , T7]

plt.plot(S , T , 'g--',)
plt.xlabel('Entropy')
plt.ylabel('Temperature')
plt.text(S2,T02,'P02')
plt.text(S3,T03,'P03')
plt.text(S4,T04,'P04')
plt.text(S5,T05,'P05')
plt.text(S7,T7,'P7')

plt.show()

S8 = CPc*math.log(T08/Pa) - R*math.log(P08/Pa)+S2
S9 = CPc*math.log(T9/T08) - R*math.log(P9/P08)+ S8
S = [S2,S8 , S9]
T = [T02,T08 , T9]

plt.plot(S , T , 'g--',)
plt.xlabel('Entropy')
plt.ylabel('Temperature')
plt.text(S2,T02,"P02")
plt.text(S8,T08,"P08")
plt.text(S9,T9,"P9")

plt.show()
