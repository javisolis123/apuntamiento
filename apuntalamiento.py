from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, create_engine, Float, DateTime, update, Date, Time, exc
from sqlalchemy.sql import select
from sqlalchemy.sql import text as sa_text
import time
import os
import lcddriver
import random


display = lcddriver.lcd()
metadata = MetaData()
#Estructura de la tabla todo
todo = Table('todo', metadata,
             Column('id', Integer, primary_key=True),
             Column('temperatura', Float()),
             Column('humedad', Float()),
             Column('canal1', Float()),
             Column('canal2', Float()),
             Column('canal3', Float()),
             Column('canal4', Float()),
             Column('tempGabinete', Float()),
             Column('hora', Time()),
             Column('fecha', Date()),
             )

#Estructura de la tabla configuracion             
configuracion = Table('configuracion', metadata,
                      Column('id', Integer, primary_key=True),
                      Column('tipo', Integer),
                      Column('frec', Integer),
                      Column('potmax', Float()),
                      Column('potmin', Integer()),
                      Column('tempmax', Integer()),
                      Column('tempmin', Integer()),
                      Column('checkbox', String(15)),
                      Column('ip', String(15)),
                      Column('backup', String(10)),
                      Column('apunta', String(15)),
                      Column('canal', String(15))
                      )

alarmas = Table('alarmas', metadata,
                Column('id', Integer, primary_key = True),
                Column('codigo', String(10)),
                Column('descripcion', String(250)),
                Column('hora_inicial', Time()),
                Column('fec_inicial', Date()),
                Column('estado', String(10))
                )

def borrar_lcd():
    display.lcd_display_string("                    ", 1)
    display.lcd_display_string("                    ", 2)
    display.lcd_display_string("                    ", 3)
    display.lcd_display_string("                    ", 4)
def mostrar_alarmas():
    aux = 0
    query_alarmas = select([alarmas])
    resp = connection.execute(query_alarmas)
    for alarma in resp:
        if alarma.estado == "activo":
            aux += 1
    if aux == 0:
        display.lcd_display_string("Sin alarmas", 1)
    if aux > 0:
        borrar_lcd()
        query2 = select([alarmas])
        resp1 = connection.execute(query2)
        pos = 1
        cont = 1
        for alm in resp1:
            if alm.estado == "activo":
                msg = str(cont) + ".-  " + str(alm.codigo)
                display.lcd_display_string(msg, pos)
                pos += 1
                cont += 1
                if pos > 4:
                    time.sleep(1)
                    pos = 1
                    borrar_lcd()

def mostrar_actual():
    minimo = 1000
    maximo = 0
    conf = select([configuracion])
    res = connection.execute(conf)
    estado = res.fetchone()
    lista = select([todo])
    resp = connection.execute(lista)
    aux = resp.fetchone()
    if estado.canal == "1":
        for dato in resp:
            if dato.canal1 > maximo:
                maximo = dato.canal1
            if dato.canal1 < minimo:
                minimo = dato.canal1
            MSGMIN = "  Min: " + str(minimo)
            MSGMAX = "  Max: " + str(maximo)
            MSGACT = "  Act: " + str(aux.canal1)
            display.lcd_display_string("         SMR", 1)
            display.lcd_display_string(MSGMAX, 2)
            display.lcd_display_string(MSGACT, 3)
            display.lcd_display_string(MSGMIN, 4)
        else:
            for dato in resp:
                if dato.canal2 > maximo:
                    maximo = dato.canal2
                if dato.canal2 < minimo:
                    minimo = dato.canal2
            MSGMIN = "  Min: " + str(min)
            MSGMAX = "  Max: " + str(max)
            MSGACT = "  Act: " + str(aux.canal1)
            display.lcd_display_string("         SMR", 1)
            display.lcd_display_string(MSGMAX, 2)
            display.lcd_display_string(MSGACT, 3)
            display.lcd_display_string(MSGMIN, 4)  

def mostrar_conf():
    confi = select([configuracion])
    resp_confi = connection.execute(confi)
    aux = resp_confi.fetchone()
    tipo = str(aux.tipo)
    frec = str(aux.frec)
    potmax = str(aux.potmax)
    potmin = str(aux.potmin)
    tempmax = str(aux.tempmax)
    tempmin = str(aux.tempmin)
    linea1 = tipo[0:3] + "    " + frec[0:3] + "   " + potmax[0:3] + "  " + potmin[0:3]
    linea2 = "   " + tempmax[0:3] + "      " + tempmin[0:3]
    display.lcd_display_string("tip  fre  PMa  PMi", 1)
    display.lcd_display_string(linea1, 2)
    display.lcd_display_string("TempMax   TempMin", 3)
    display.lcd_display_string(linea2, 4)
    
def pantalla_inicio(num):
    if num == 0:
        borrar_lcd()
        mostrar_alarmas()
    elif num == 1:
        borrar_lcd()
        mostrar_actual()
    elif num == 2:
        borrar_lcd()
        mostrar_conf()
while True:
    #Se crea un objeto con la conexion a la base de datos de MariaDB
    engine = create_engine('mysql+pymysql://javi:javiersolis12@192.168.10.20/Tuti')
    connection = engine.connect()
    conf = select([configuracion])
    res = connection.execute(conf)
    estado = res.fetchone()    
    if estado.apunta == "activado":
        mostrar_actual()               
    else:
        num = random.randrange(3)
        print("El numero random es: " + str(num))
        pantalla_inicio(num)
    time.sleep(1)