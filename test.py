from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import random
import math
import numpy as np

def gausform(x,A,E,I):
    w=E**0.5/30+0.01
    y_new=[0]*len(x)
    for i in range(0,len(x)):
        y_new[i]=A*I/100/w*(math.pi/2)**0.5*math.exp(-2*(x[i]-E)**2/w**2)
    return y_new

def listSum(a,b):
    c = map(sum, zip(a + [0,]*(len(b)-len(a)), b + [0,]*(len(a)-len(b))))
    c=list(c)
    return c

def ChooseSpector(AllSource,name):
    finalSource=None
    for i in range(0,len(AllSource)):
        if AllSource[i].name==name:
            finalSource=AllSource[i]
    return finalSource

class Source2:
    def __init__(self,x,file,name,fon):
        self.x=x
        self.name = name
        self.file = file
        self.fon=fon
        data = np.genfromtxt(file)
        self.E=data[:,0]/1000
        self.I=data[:,2]
    def Spectr(self,A):
        yfinal=gausform(self.x,A,self.E[0],self.I[0])
        for i in range(1,len(self.E)-1):
            ynew=gausform(self.x,A,self.E[i],self.I[i])
            yfinal=listSum(ynew,yfinal)
        koeficient=sum(yfinal)/(2*sum(self.fon))
        newFon = [x * koeficient for x in self.fon]
        yfinal=listSum(newFon,yfinal)
        return yfinal




x=[]
for i in range(0,1500):
    x.append(14/1500*i)
spectr=[0]*len(x)
fon = np.genfromtxt("fon.txt")



fig, ax = plt.subplots()
graph = ax.plot(x,spectr,color = 'g')[0]
#plt.show()


#Fe56
name='Fe'
Fe=Source2(x,"Fe.txt",name,fon)

name='Ca'
Ca=Source2(x,"Ca.txt",name,fon)

name='Si'
Si=Source2(x,"Si.txt",name,fon)

name='Ni'
Ni=Source2(x,"Ni.txt",name,fon)

name='S'
S=Source2(x,"S.txt",name,fon)

name='H'
H=Source2(x,"H.txt",name,fon)
print(H.E)

name='B'
B=Source2(x,"B.txt",name,fon)

name='Cl'
Cl=Source2(x,"Cl.txt",name,fon)

AllSource=[Fe, Ca, Si, Ni, S, H, B, Cl]


eliment=input("введите element: ")
#eliment='Ni59'
FinalSource=ChooseSpector(AllSource,eliment)

if FinalSource != None:
    A=1
    def update(frame):
        global graph
        global spectr
        global A
        A+=2
        spectr=Fe.Spectr(A)
        graph.set_xdata(x)
        graph.set_ydata(spectr)
        if max(spectr) > 5000:
            maxY=max(spectr)*1.1
        else:
            maxY=5000
        plt.ylim(0,maxY)
    nim = FuncAnimation(fig, update, frames = None, interval = 300)
    plt.show()
else:
    print(0)


