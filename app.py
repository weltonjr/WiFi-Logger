import subprocess
import time
import re
import MySQLdb


#efetua o scan e recupera os valores
def scan(): 
    print "scan"
    saida = subprocess.Popen(["iwlist", "{insira a interface aquiu}", "scan"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    saida = saida.stdout.read().decode('utf-8')
    #arq = open('res.txt', 'r')
    #saida = arq.readlines()

    ssid = re.findall( r'(ESSID:")([A-z0-9\s ]*)' , str(saida) )
    address = re.findall( r'(Address:) ([A-Z0-9 ]+:[A-Z0-9 ]+:[A-Z0-9 ]+:[A-Z0-9 ]+:[A-Z0-9 ]+:[A-Z0-9 ]+)' , str(saida) )
    quality = re.findall( r'(Quality=[0-9][0-9])' , str(saida) )
    level = re.findall( r'(level=-[0-9][0-9])' , str(saida) )
    channel = re.findall( r'(Channel:[0-9][0-1]?)' , str(saida) )
    frequency = re.findall( r'(Frequency:[0-9]*.[0-9]?[0-9]?[0-9]?)' , str(saida) )
    lastBeacon  = re.findall( r'(beacon: [0-9]*)' , str(saida) )

    index = 0
    while(index < len(ssid)):
        print "." + ssid[index][1]
        f_ssid  = ssid[index][1]
        f_address  = address[index][1]
        f_quality  = quality[index].split('=')[1]
        f_level  = level[index].split('=')[1]
        f_channel  = channel[index].split(':')[1]
        f_frequency  = frequency[index].split(':')[1]
        f_lastBeacon = lastBeacon[index].split(':')[1]
        
        db(f_ssid, f_address, f_quality, f_level, f_channel, f_frequency, f_lastBeacon)
        index = index + 1

#envia ao banco
def db(ssid, address, quality, level, channel, frequency, lastBeacon):
    print "db"
    con = MySQLdb.connect(host="", user='root', passwd="root", db="redes")
    cursor = con.cursor()
    cursor.execute("INSERT INTO `redes`.`wifi` (`ssid`, `mac`, `quality`, `signal`, `channel`, `frequency`, `beacon`) VALUES ('"+ssid+"','"+address+"',"+quality+","+level+","+channel+","+frequency+","+lastBeacon+")")
    con.commit()

#APP
while(1):
    scan()
    time.sleep(60)
