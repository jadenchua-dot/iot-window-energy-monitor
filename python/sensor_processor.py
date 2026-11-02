#serial comm library
import serial
#pymysql library for Python
import pymysql

#read serial data coming from Arduino
ser = serial.Serial('/dev/ttyACM0', 9600)

#connecting to a MySQLdb
db=pymysql.connect(user='Nypuser',
passwd='password', host='localhost', db='Part2Data')
cursor = db.cursor()

time_open = 0

try:
    while True:
        Limit = ser.readline()
        Limit = Limit.decode('utf-8', errors='ignore')
        Limit = Limit.rstrip()
        Limit = Limit[11:] 
        Limit = float(Limit)

        Window = ser.readline()
        Window = Window.decode('utf-8', errors='ignore')
        Window = Window.rstrip()
        Window = Window[14:] 
        Window = float(Window)

        if Window == 0:
            Room_Status = "System Secure"
            Alert_Msg = "Alert: OFF"
            time_open = 0
            ser.write(b'L')
        else:
            Room_Status = "Open"
            time_open = time_open + 1
            if time_open > Limit:
                Alert_Msg = "Alert: ON (Time Exceeded!)"
                ser.write(b'H')
            else:
                Alert_Msg = "Alert: OFF (Ventilating)"
                ser.write(b'L')

        #write sensor info to MariaDB
        cursor.execute("Insert into Part2Data(Rotary_Limit, IR_State, Room_Status, Alert_Msg) \
        Values(%s, %s, %s, %s)", (Limit, Window, Room_Status, Alert_Msg) )

        print ("Time Limit: " + str(Limit))
        print ("Window State: " + str(Window))
        print ("\nDatabase updated Successfully")
        
        db.commit()

except Exception as e:
       print("Error: ", e)
       db.rollback()

#Terminate database connection
db.close()
