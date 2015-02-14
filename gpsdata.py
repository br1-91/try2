

from serial import Serial
from decimal import *

#import locale
#locale.setlocale(locale.LC_ALL, 'en_GB.utf8')
def configure():
    port=Serial("/dev/ttyAMA0",9600)
    port.close()
    port.open()

def read():
    gga=True
    vtg=True
    latitude = 0
    latNS = ''
    longitude = 0
    lonEW = ''
    status = ''
    nsatellites = 0
    altitude = 0
    grspeed = 0
    while gga and vtg:
        rcv=port.readline()

        if rcv[0:6]=='$GPGGA':
            coma=0
            ind1=[]
            gga=False
            for index in range(len(rcv)):
                if rcv[index]==',':
                    coma=coma+1
                    ind1.append(index)

            if rcv[ind1[5+1]]!='0':
                latitude = Decimal(rcv[ind1[1]+1:ind1[2]])
                latNS = rcv[ind1[2]+1:ind1[3]]
                longitude = Decimal(rcv[ind1[3]+1:ind1[4]])
                lonEW = rcv[ind1[4]+1:ind1[5]]
                status = rcv[ind1[5]+1]
                nsatellites = Decimal(rcv[ind1[6]+1:ind1[7]])
                altitude = Decimal(rcv[ind1[8]+1:ind1[9]])

        elif rcv[0:6]=='$GPVTG':
            coma=0
            ind1=[]
            vtg=False
            for index in range(len(rcv)):
                if rcv[index]==',':
                    coma=coma+1
                    ind1.append(index)
            grspeed=Decimal(rcv[ind1[6]+1:ind1[7]])

    return(latitude,latNS,longitude,lonEW,status,nsatellites,altitude,grspeed)
