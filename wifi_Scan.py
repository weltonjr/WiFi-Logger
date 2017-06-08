import re
import os
import time
import MySQLdb

interface = 'wlxc83a35c8d61a';
tempo = 60;

def pushDB( ssid, address, quality, level, channel, frequency, lastBeacon ):   
    con = MySQLdb.connect(host="192.168.0.62", user='root', passwd="1", db="wifiscan");
    cursor = con.cursor();
    cursor.execute("INSERT INTO `wifiscan`.`scan` (`SSID`, `MAC`, `QUALITY`, `SIGNAL`, `CHANNEL`, `FREQUENCY`, `BEACON`) VALUES ('"+ssid+"','"+address+"',"+quality+","+level+","+channel+","+frequency+","+lastBeacon+")");
    con.commit()

#METODO QUE RETORNA O VALOR EM PORCENTAGEM, NA BASE 70
def calculateQualityPercent( quality ):
    number = int(str(quality));
    return (number * 100)/70;

b=0
while(b < 10):
    #PEGA  AS SAIDAS DO TERMINAL E JOGA EM UM ARQUIVO DE TEXTO
    os.system('iwlist %s scanning > res.txt' % interface);
    
    #LE O ARQUIVO E ARMAZENA O TEXTO EM UMA LISTA
    arq = open('res.txt', 'r');
    list = arq.readlines();
    
    #SEPARA A LEITURA FEITA DO ARQUIVO COM REGEX EM VARIAS LISTAS 
    ssid        = re.findall( r'(ESSID:")([A-z0-9\s]*)' , str(list) );
    address     = re.findall( r'(Address:) ([A-Z0-9][A-Z0-9]:[A-Z0-9][A-Z0-9]:[A-Z0-9][A-Z0-9]:[A-Z0-9][A-Z0-9]:[A-Z0-9][A-Z0-9]:[A-Z0-9][A-Z0-9])' , str(list) );
    quality     = re.findall( r'(Quality=[0-9][0-9])' , str(list) );
    level       = re.findall( r'(level=-[0-9][0-9])' , str(list) );
    channel     = re.findall( r'(Channel:[0-9][0-1]?)' , str(list) );
    frequency   = re.findall( r'(Frequency:[0-9]*.[0-9]?[0-9]?[0-9]?)' , str(list) );
    lastBeacon  = re.findall( r'(beacon: [0-9]*)' , str(list) );

    #APRESENTA OS VALORES NA TELA, MAS PODE SER USADO PARA MONTAR O COMANDO SQL E ENVIAR PARA O SERVIDOR
    x=0
    nElem = len(ssid);
    while(x < nElem):

        s  = ssid[x][1]
        a  = address[x][1]
        q  = quality[x].split('=')[1]
        n  = level[x].split('=')[1]
        c  = channel[x].split(':')[1]
        f  = frequency[x].split(':')[1]
        lb = lastBeacon[x].split(':')[1]

        print('nome - ' + ssid[x][1]);
        print('endereco - ' + address[x][1]);
        print('qualidade - ' + quality[x].split('=')[1]) ;
        print('nivel - ' + level[x].split('=')[1]);
        print('canal - ' + channel[x].split(':')[1]);
        print('frequencia - ' + frequency[x].split(':')[1]);
        print('last beacon - ' + lastBeacon[x].split(':')[1]);
        print();

        pushDB( s, a, q, n, c, f, lb );
        x+=1;

    b+=1;
    # A CADA UM MINUTO REFAZ TODO O PROCESSO
    time.sleep(tempo);
