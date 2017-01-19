import RPi.GPIO as GPIO
import MySQLdb
import time
import threading
db = MySQLdb.connect("localhost","root","root","iot_demo" )
cursor = db.cursor()
class Room (threading.Thread):

  def __init__(self, room_pin, room_name, room_id):
    threading.Thread.__init__(self)
    self.is_occupied = 0
    self.room_pin = room_pin
    self.room_name = room_name
    self.room_id = room_id
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(self.room_pin, GPIO.IN)
    GPIO.setup(7, GPIO.OUT)
    GPIO.setup(8, GPIO.OUT)

  def run(self):
    check_room(self)

def check_room(room):
  print room
  i=j=0
  while True:
    i=GPIO.input(room.room_pin)
    if i==0 and i!=j: #When output from motion sensor is LOW
      print room.room_name, "Available", '@', time.ctime()
      cursor.execute("select id from room_details where room_id=%s && status=1 ORDER BY id DESC LIMIT 1", room.room_id)
      occupied_id = cursor.fetchone()

      if occupied_id != None:
        cursor.execute("update room_details set out_time=%s, status=0 where id=%s", (time.strftime('%Y-%m-%d %H:%M:%S'), occupied_id[0]))

      GPIO.output(7, 0) #Turn OFF LED
      GPIO.output(8, 1)
      j = i
      time.sleep(.1)
    elif i==1 and i!=j: #When output from motion sensor is HIGH
      print room.room_name, "Occupied", '@', time.ctime()
      cursor.execute("Insert into room_details (room_id, in_time, status) values (%s, %s, 1)", (room.room_id, time.strftime('%Y-%m-%d %H:%M:%S')))
      GPIO.output(7, 1) #Turn ON LED
      GPIO.output(8, 0)
      time.sleep(.1)
      j = i
    db.commit()
  GPIO.cleanup()
room1 = Room(11, "Room1", 1)
room2 = Room(15, "Room2", 2)
room1.start()
room2.start()