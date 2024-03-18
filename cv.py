import cv2
from util import *
from gpiozero import Robot
from bluedot import BlueDot


speed = 0.5
status = 'stop'
bd = BlueDot(cols=3, rows=3)
bd.color = 'red'
bd.square = True
robot = Robot(left=(21,20), right=(10, 9))
bd[2, 2].visible = False
bd[2, 0].visible = False
bd[0, 0].visible = False
bd[0, 2].visible = False
bd[1, 1].visible = False
bd.wait_for_press()


def up():   
    global status  
    global boolean_yellow
    if not boolean_yellow:  
        robot.forward(speed)
        status = 'up'
        print(status)
    else:
        while boolean_yellow:
            status = 'down'
            robot.backward(0.3)
            print(status)
        status = 'stop'
        robot.stop()
        print(status)

def down():   
    global status 
    global boolean_yellow 
    if not boolean_yellow:
        robot.backward(speed)
        status = 'down'
        print(status)
    else:
        while boolean_yellow:
            status = 'up'
            robot.forward(0.3)
            print(status)
        status = 'stop'
        robot.stop()
        print(status)

def right():   
    global status
    global boolean_yellow  
    if not boolean_yellow:
        robot.right(speed)
        status = 'right'
        print(status)
    else:
        while boolean_yellow:
            status = 'left'
            robot.left(0.3)
            print(status)
        status = 'stop'
        robot.stop()
        print(status)

def left():
    global status 
    global boolean_yellow 
    if not boolean_yellow:
        robot.left(speed)
        status = 'left'
        print(status)
    else:
        while boolean_yellow:
            status = 'right'
            robot.right(0.3)
            print(status)
        status = 'stop'
        robot.stop()
        print(status)

def increment():        
    global speed
    speed += 0.1
    speed = min(speed, 1.0)
    print(speed)

def decrement():        
    global speed
    speed -= 0.1
    speed = max(speed, 0.0)
    print(speed)

def stop():  
    global status
    global boolean_yellow
    if not boolean_yellow:
        robot.stop()
        status = 'stop'
        print(status)
    else:
        while boolean_yellow:
            status = 'down'
            robot.backward(0.3)
            print(status)
        status = 'stop'
        robot.stop()
        print(status)


cap = cv2.VideoCapture('http://192.168.186.106:8080/stream/video.mjpeg')
while True:
    ret,frame = cap.read()
    yellow = yellow_mask(frame)
    red = red_mask(frame)
    cropped_yellow = roi_yellow(yellow)
    cropped_red = roi_red(red)
    boolean_yellow = max_value(cropped_yellow)
    boolean_red = count_white(cropped_red)
    cv2.imshow('frame',frame)
    cv2.imshow('yellow',yellow)
    cv2.imshow('roi',cropped_red)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
    if boolean_red:
        if bd.running:
            robot.stop()
            bd.stop()
            print('server stopped')
    elif not bd.running:
        bd.start()
        print('server started')
    else:
        bd[1, 0].when_pressed = up
        bd[1, 2].when_pressed = down
        bd[0, 1].when_pressed = left
        bd[2, 1].when_pressed = right
        bd[2, 0].when_pressed = increment
        bd[2, 2].when_pressed = decrement
        bd.when_released = stop    
    

cap.release()
cv2.destroyAllWindows()


