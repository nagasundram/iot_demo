import RPi.GPIO as GPIO
import MySQLdb
import time
import threading

class Room (threading.Thread):

  def __init__(self, room_id, room_name, room_output_pin, green, red):
    threading.Thread.__init__(self)
    #Initializing the Room Details
    self.is_occupied = 0
    self.room_output_pin = room_output_pin
    self.room_name = room_name
    self.room_id = room_id
    self.green = green
    self.red = red

    #Settting up the GPIO board and pins
    GPIO.setmode(GPIO.BOARD)

    #Setting up Motion sensor output as input
    GPIO.setup(self.room_output_pin, GPIO.IN)

    #setting up the Status LEDs
    GPIO.setup(self.green, GPIO.OUT)
    GPIO.setup(self.red, GPIO.OUT)

  def run(self):
    check_room(self)

def check_room(room):
  #DB connection
  db = MySQLdb.connect("localhost","root","root","iot_demo" )
  cursor = db.cursor()

  curr_status=prev_status=0

  while True:
    curr_status=GPIO.input(room.room_output_pin)

    if curr_status==0 and curr_status!=prev_status: #When output from motion sensor is LOW
      print room.room_name, "Available", '@', time.ctime()
      cursor.execute("select id from room_details where room_id=%s && status=1 ORDER BY id DESC LIMIT 1", room.room_id)
      occupied_id = cursor.fetchone()
      if occupied_id != None:
        cursor.execute("update room_details set out_time=%s, status=0 where id=%s", (time.strftime('%Y-%m-%d %H:%M:%S'), occupied_id[0]))
      GPIO.output(room.green, 0) #Turn OFF LED
      GPIO.output(room.red, 1)

    elif curr_status==1 and curr_status!=prev_status: #When output from motion sensor is HIGH
      print room.room_name, "Occupied", '@', time.ctime()
      cursor.execute("Insert into room_details (room_id, in_time, status) values (%s, %s, 1)", (room.room_id, time.strftime('%Y-%m-%d %H:%M:%S')))
      GPIO.output(room.green, 1) #Turn ON LED
      GPIO.output(room.red, 0)

    time.sleep(.1)
    prev_status = curr_status
    db.commit()

  GPIO.cleanup()

#Creating instances for Room object and checking the status parallel.

room1 = Room(1, "Room1", 11, 7, 8)
room2 = Room(2, "Room2", 15, 35, 36)
room3 = Room(3, "Room3", 13, 37, 38)
room1.start()
room2.start()
room3.start()
