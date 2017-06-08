import subprocess
import time
import re


#efetua o scan e recupera os valores
def scan(): 
    arq = open('res.txt', 'r')
    saida = arq.readlines()

    ssid = re.findall( r'(ESSID:")([A-z0-9\s]*)' , str(saida) )
    address = re.findall( r'(Address:) ([A-Z0-9]+:[A-Z0-9]+:[A-Z0-9]+:[A-Z0-9]+:[A-Z0-9]+:[A-Z0-9]+)' , str(saida) )
    quality = re.findall( r'(Quality=[0-9][0-9])' , str(saida) )
    level = re.findall( r'(level=-[0-9][0-9])' , str(saida) )
    channel = re.findall( r'(Channel:[0-9][0-1]?)' , str(saida) )
    frequency = re.findall( r'(Frequency:[0-9]*.[0-9]?[0-9]?[0-9]?)' , str(saida) )
    lastBeacon  = re.findall( r'(beacon: [0-9]*)' , str(saida) )

#envia ao banco
def db(ssid, address, quality, level, channel, frequency, lastBeacon):
con = MySQLdb.connect(host="", user='root', passwd="root", db="redes")
cursor = con.cursor()
cursor.execute("INSERT INTO `redes`.`wifi` (`ssid`, `mac`, `quality`, `signal`, `channel`, `frequency`, `beacon`) VALUES ('"+ssid+"','"+address+"',"+quality+","+level+","+channel+","+frequency+","+lastBeacon+")")
con.commit()

#APP
while(true):
    #saida = subprocess.Popen(["iwlist", interface, "scan"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #saida = saida.stdout.read().decode('utf-8')
    scan()

    time.sleep(120)
