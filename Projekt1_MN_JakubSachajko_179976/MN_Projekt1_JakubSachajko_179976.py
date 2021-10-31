import pandas as pd
import jupyter
from matplotlib import pyplot as plt

#MACD - moving average convergence/divergence 
#EMA - exponential moving average
#SIGNAL - linia sygnału

#Wskaźnik MACD składa się z 2 wykresów
#Miejsce, w którym MACD przecina SIGNAL od dołu jest sygnałem do zakupu akcji
#Miejsce, w którym MACD przecina SIGNAL od góry, jest sygnałem do sprzedaży akcji

def EMA(numberOfEMA,numberOfSample,listOfValues):
	EMAValue=0
	EMABase=0
	counterMathHelper=0
	for i in range(numberOfSample,numberOfSample - numberOfEMA,-1):
		if i<0:
			break
		EMAValue = pow(1-(2/(numberOfEMA+1)),counterMathHelper)*listOfValues[i] + EMAValue
		EMABase = pow(1-(2/(numberOfEMA+1)),counterMathHelper) + EMABase
		counterMathHelper += 1
	EMAValue = EMAValue / EMABase
	return EMAValue

def MACD(numberOfSampleMACD):
	return EMA(12,numberOfSampleMACD,df.Otwarcie)-EMA(26,numberOfSampleMACD,df.Otwarcie)

def SIGNAL(numberOfSampleSIGNAL):
	return EMA(9,numberOfSampleSIGNAL,MACDValues)

df = pd.DataFrame(pd.read_csv('cdr.csv'))

MACDValues = []
SIGNALValues = []
realValues = []
checkIfGoesUpOrDown = []
shouldIBuy = []

kapital = 1000
liczbaAkcji = 0

print("kapitał początkowy wynosi :",kapital)
print("liczba akcji wynosi :",liczbaAkcji)
print("----------------------------")

listOfThousand = list(range(1,1001))
for i in range (1000):
	MACDValues.append(MACD(i))
	SIGNALValues.append(SIGNAL(i))
	realValues.append(df.Otwarcie[i])
	if i==0:
		checkIfGoesUpOrDown.append(0)
		shouldIBuy.append(0)
	else:
		checkIfGoesUpOrDown.append(realValues[i]-realValues[i-1])
		if(i>=33):
			if MACDValues[i] < SIGNALValues[i] and MACDValues[i-1] > SIGNALValues[i-1]:
				shouldIBuy.append(-1)
				kapital = kapital + (liczbaAkcji * realValues[i])
				liczbaAkcji = 0
			elif MACDValues[i] > SIGNALValues[i] and MACDValues[i-1] < SIGNALValues[i-1]:
				shouldIBuy.append(1)
				liczbaAkcji = liczbaAkcji + (kapital//realValues[i])
				kapital = kapital - (liczbaAkcji * realValues[i])
			else:
				shouldIBuy.append(0)
		else:
			shouldIBuy.append(0)

	#print("Nr:",i+1,"posiada akcji:",liczbaAkcji,"posiada kapitał:",kapital,"wartość akcji:",realValues[i])

if liczbaAkcji != 0:
	kapital += liczbaAkcji*realValues[999]
	liczbaAkcji = 0

print("----------------------------")
print("kapitał końcowy wynosi :",kapital)
print("liczba akcji wynosi :",liczbaAkcji)

plt.subplot(2,2,1)
plt.plot(listOfThousand,SIGNALValues)
plt.plot(listOfThousand,MACDValues)
plt.title("wykres MACD/SIGNAL od numberu próbki")
plt.xlabel('numberOfSample')
plt.ylabel('value')
plt.legend(['SIGNAL','MACD'])
plt.subplot(2,2,2)
plt.title("wykres Wartości od numberu próbki")
plt.xlabel('numberOfSample')
plt.ylabel('value')
plt.plot(listOfThousand,realValues)
plt.subplot(2,2,3)
plt.title("wykres zmian od numberu próbki")
plt.xlabel('numberOfSample')
plt.ylabel('valueDifference')
plt.plot(listOfThousand,checkIfGoesUpOrDown)
plt.axhline(y=0, color='k',linestyle='--')
plt.subplot(2,2,4)
plt.title("wykres [ 1 - kupuj | -1 - sprzedaj ]")
plt.xlabel('numberOfSample')
plt.ylabel('buyOrSell')
plt.axhline().remove()
plt.scatter(listOfThousand,shouldIBuy)
plt.show()