from math import sqrt

def vorz(a):
    if a/abs(a) < 0:
        return "-"
    else:
         return "+"

class Quat():
    ##Rechenregeln und Funktionen sind von: https://mathepedia.de/Quaternionen.html
    def __init__(self,Koordinaten):
        if isinstance(Koordinaten,tuple) and len(Koordinaten) == 4:
            self._Koordinaten = Koordinaten
        elif isinstance(Koordinaten,str):
            def isnumber(ch):
                if ch == ".":
                    return 1
                for i in range(0,10):
                    if ch == str(i):
                        return 1
                return 0
            def find_1(str, start, ch):
                i = start
                while i < len(str):
                    if str[i] == ch:
                        return i
                    i = i +1
                return -1
            def find_2(str, start, ch):
                i = start
                while i < len(str):
                    if str[i] == ch:
                        return i
                    i = i +1
                return i
            def findnumber(str, start):
                i = start
                while i < len(str):
                    if isnumber(str[i]):
                        return max(i,start)
                    i = i + 1
                return i
            def endnumber(str, start):
                i = start
                while i < len(str):
                    if not isnumber(str[i]):
                        return i -1
                    i = i + 1
                return i
            def sfloat(str):
                String = str
                if not find_1(String, 0, ".") + 1:
                    return int(String)

                else:
                    Zahl = int(String[0:find_1(String, 0, ".")])
                    String = String[find_1(String, 0, ".") + 1:len(String)]
                    Zahl = Zahl + (10**-len(String)) * int(String)
                    return Zahl

            Liste = [0,0,0,0]
            Basis = ["","i","j","k"]
            Teilwörter = []
            a1 = 0
            a2 = 0
            w1= True
            while w1:
                a1 = a2
                a2 = min(min(find_2(Koordinaten,a1 + 1,"+"),find_2(Koordinaten,a1 + 1,"-")),len(Koordinaten)-1)
                if a2 == len(Koordinaten) - 1:
                    w1 = False
                    a2 = a2  + 1
                Teilwörter.append(Koordinaten[a1:a2])
            for i in range(0,len(Teilwörter)):
                w2 = True
                for j in range(1,4):
                    if find_1(Teilwörter[i],0,Basis[j]) != -1:
                        b1 = findnumber(Teilwörter[i],0)
                        b2 = endnumber(Teilwörter[i],b1)
                        vorz = 1
                        if (Teilwörter[i])[0] == "-":
                            vorz = -1
                        if b1 == len(Teilwörter[i]):
                            Liste[j] = Liste[j] + vorz * 1
                        else:
                            Liste[j] = Liste[j] + vorz * sfloat((Teilwörter[i])[b1:b2 + 1])
                        w2 = False
                        break
                if w2:
                    b1 = findnumber(Teilwörter[i],0)
                    b2 = endnumber(Teilwörter[i],b1)
                    if (Teilwörter[i])[0] == "-":
                        Liste[0] = Liste[0] - sfloat((Teilwörter[i])[b1:b2 + 1])
                    else:
                        Liste[0] = Liste[0] + sfloat((Teilwörter[i])[b1:b2 + 1])
            self._Koordinaten = tuple(Liste)
            #leider ergibt Quat("ik") einfach nur i, das fehlt noch
        else: raise TypeError ("Bitte geben sie das Quaterion durch ein Tupel mit vier Einträgen oder als Zeichenkette ein")
    def __str__(self):
        Basis = ["","i","j","k"]
        bez = ""
        Koordinaten = self._Koordinaten
        if Koordinaten[0] != 0:
            bez = bez + str(Koordinaten[0])
        for i in range(1,4):
            if Koordinaten[i] != 0:
                if bez != "":
                    bez = bez + " " + vorz(Koordinaten[i]) + " "
                elif vorz(Koordinaten[i]) == "-":
                    bez = "-"
                if abs(Koordinaten[i]) == 1:
                    bez = bez + Basis[i]
                else:
                    bez = bez + str(abs(Koordinaten[i])) + Basis[i]
        if bez == "":
            return "0"
        else:
            return bez
    def __add__(self,other):
        if isinstance(other,Quat):
            Liste = []
            for i in range(0,4):
                Liste.append(self._Koordinaten[i] + other._Koordinaten[i])
            return Quat(tuple(Liste))
        elif isinstance(other,(int,float)):
            Liste = list(self._Koordinaten)
            Liste[0] = Liste[0] + other
            return Quat(tuple(Liste))
        elif isinstance(other,complex):
            Liste = list(self._Koordinaten)
            Liste2 = [other.real,other.imag]
            for i in range(0,2):
                Liste[i] = Liste[i] + Liste2[i]
            return Quat(tuple(Liste))
        else:
             raise TypeError()
    def __radd__(self,other):
        return self.__add__(other)
    def __sub__(self,other):
        return self + ( other * -1 )
    def __rsub__(self,other):
        return other + ( self * -1 )
    def __mul__(self,other):
        #Graßmannprodukt
        if isinstance(other,Quat):
            a = self._Koordinaten
            b = other._Koordinaten
            c = [0,0,0,0]
            c[0] = a[0]*b[0] - a[1]*b[1] - a[2]*b[2] - a[3]*b[3]
            c[1] = a[0]*b[1] + a[1]*b[0] + a[2]*b[3] - a[3]*b[2]
            c[2] = a[0]*b[2] + a[2]*b[0] + a[3]*b[1] - a[1]*b[3]
            c[3] = a[0]*b[3] + a[3]*b[0] + a[1]*b[2] - a[2]*b[1]
            return Quat(tuple(c))
        elif isinstance(other,(int,float)):
            Liste = list(self._Koordinaten)
            for i in range(0,4):
                Liste[i] = Liste[i] * other
            return Quat(tuple(Liste))
        elif isinstance(other,complex):
            return self * Quat((other.real,other.imag,0,0))
        else:
            raise TypeError()
    def __rmul__(self,other):
        if isinstance(other,(int,float)):
            Liste = list(self._Koordinaten)
            for i in range(0,4):
                Liste[i] = other * Liste[i]
            return Quat(tuple(Liste))
        elif isinstance(other,complex):
            return Quat((other.real,other.imag,0,0)) * self
        else:
            raise TypeError()
    def __GassGProd__(self,other):
        #Gaßmann-Geradenprodukt
        s = self._Koordinaten
        o = other._Koordinaten
        Liste = [0,0,0,0]
        Liste[0] = s[0] * o[0] + s[1] * o[1] + s[2] * o[2] +s[3] * o[3]
        Liste[1] = s[0] * o[1] + s[2] * o[1]
        Liste[2] = s[0] * o[2] + s[2] * o[0]
        Liste[3] = s[0] * o[3] + s[3] * o[0]
        return(Quat(tuple(Liste)))
    def __GrassUgProd__(self,other):
        #Graßmann-Ungeradenprodukt oder auch kreuzprodukt genannt
        s = self._Koordinaten
        o = other._Koordinaten
        Liste = [0,0,0,0]
        Liste[1] = s[2] * o[3] - s[3] * o[2]
        Liste[2] = s[3] * o[1] - s[1] * o[3]
        Liste[3] = s[1] * o[2] - s[2] * o[1]
        return Quat(tuple(Liste))
    def __EuklidProd__(self,other):
        return self * other.__konj__()
    def __EuklidUgProd__(self,other):
        #Euklidisches Ungeradenprodukt
        s = self._Koordinaten
        o = other._Koordinaten
        Liste = [0,0,0,0]
        Liste[1] = s[0] * o[1] - s[1] * o[0] + s[3] * o[2] - s[2] * o[3]
        Liste[2] = s[0] * o[2] - s[2] * o[0] + s[1] * o[3] - s[3] * o[1]
        Liste[3] = s[0] * o[3] - o[3] * s[0] + s[2] * o[1] - s[1] * o[2]
        return Quat(tuple(Liste))
    def __pow__(self,other):
        Quaterion = self
        if not isinstance(other,int):
            raise TypeError()
        if other < 0:
            Quaterion = Quaterion **abs(other)
            Quaterion = Quaterion.__konj__() * (abs(Quaterion) ** -2)
        elif other == 0:
            Quaterion = Quat("1")
        elif other > 0:
            for i in range(1,other):
                Quaterion = Quaterion * self
        return Quaterion
    def __ska__(self,other):
        #gibt das Skalarprodukt der beiden Quaterionen aus
        #wird auch Euklidisches Geradenprodukt genannt
        K1 = self._Koordinaten
        K2 = other._Koordinaten
        return K1[0] * K2[0] + K1[1] * K2[1] + K1[2] * K2[2] + K1[3] * K2[3]
    def __abs__(self):
        Koordinaten = self._Koordinaten
        return sqrt(self.__ska__(self))
    def __norm__(self):
        #normiert das Quaterion
        return self * (self.__abs__())**-1
    def __konj__(self):
        #gibt die Konjugation des Quaterions aus
        Koordinaten = self._Koordinaten
        return Quat((Koordinaten[0], -1 * Koordinaten[1], -1 * Koordinaten[2], -1 * Koordinaten[3]))




