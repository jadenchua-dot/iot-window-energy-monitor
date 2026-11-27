# Smart Window Energy Guard - Raspberry Pi side
#
# The Arduino sends two lines every second:
#     Time_Limit:<seconds set on the rotary knob, 5-60>
#     Window_Status:<0 = closed, 1 = open>
# For each Window_Status line this script counts how long the window has been
# open, sends 'H' (alarm on) or 'L' (alarm off) back to the Arduino, and logs
# the reading to MariaDB for the Flask dashboard (app.py).
#
# Settings can be overridden with environment variables, e.g.
#     SERIAL_PORT=/dev/ttyUSB0 DB_PASSWORD=secret python3 sensor_processor.py

import os

#serial comm library
import serial
#pymysql library for Python
import pymysql

SERIAL_PORT = os.environ.get("SERIAL_PORT", "/dev/ttyACM0")
DB_SETTINGS = {
    "user": os.environ.get("DB_USER", "Nypuser"),
    "passwd": os.environ.get("DB_PASSWORD", "password"),
    "host": os.environ.get("DB_HOST", "localhost"),
    "db": os.environ.get("DB_NAME", "Part2Data"),
}


def parse_line(raw):
    """b'Time_Limit:30\r\n' -> ('Time_Limit', 30.0). None for noise or half lines."""
    text = raw.decode("utf-8", errors="ignore").strip()
    key, sep, value = text.partition(":")
    if not sep:
        return None
    try:
        return key, float(value)
    except ValueError:
        return None


def decide(window_open, time_open, limit):
    """One reading (one second apart).

    Returns (time_open, room_status, alert_msg, command for the Arduino).
    """
    if not window_open:
        return 0, "System Secure", "Alert: OFF", b"L"
    time_open += 1
    if time_open > limit:
        return time_open, "Open", "Alert: ON (Time Exceeded!)", b"H"
    return time_open, "Open", "Alert: OFF (Ventilating)", b"L"


def main():
    #read serial data coming from Arduino
    ser = serial.Serial(SERIAL_PORT, 9600)

    #connecting to a MySQLdb
    db = pymysql.connect(**DB_SETTINGS)
    cursor = db.cursor()

    limit = None
    time_open = 0
    try:
        while True:
            # Lines are matched by name, not by position, so starting mid-stream
            # (or the Arduino resetting when the port opens) can't crash the loop.
            reading = parse_line(ser.readline())
            if reading is None:
                continue
            key, value = reading
            if key == "Time_Limit":
                limit = value
                continue
            if key != "Window_Status" or limit is None:
                continue

            window = value
            time_open, room_status, alert_msg, command = decide(window != 0, time_open, limit)
            ser.write(command)

            #write sensor info to MariaDB
            cursor.execute("Insert into Part2Data(Rotary_Limit, IR_State, Room_Status, Alert_Msg) "
                           "Values(%s, %s, %s, %s)", (limit, window, room_status, alert_msg))
            db.commit()

            print("Time Limit: " + str(limit))
            print("Window State: " + str(window))
            print("\nDatabase updated Successfully")

    except KeyboardInterrupt:
        print("Stopped.")
    except Exception as e:
        print("Error: ", e)
        db.rollback()
    finally:
        ser.write(b"L")   # never leave the alarm sounding
        #Terminate database connection
        db.close()
        ser.close()


if __name__ == "__main__":
    main()
