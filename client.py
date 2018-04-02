#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  client.py
#
#  
#  
import socket
import pygame

PORT = 8000
IP = "127.0.0.1"

# test sending a message
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.sendto(MESSAGE, (IP, PORT))

pygame.init()  # init pygame
pygame.joystick.init()  # init pygame joysticks
joysticks = pygame.joystick.Joystick(0)

joycount = pygame.joystick.get_count()
print( joycount )
for x in (0, joycount):
    print(joysticks)  # print list of connected controllers


def senddata(message):
    """ This command uses the socket library to send a 2 byte message parameter
    :param message: the data that gets sent to the arduino, to be handled and control the motors
    :return: no return
    """
    sock.sendto(message, (IP, PORT))

# The steelseries gamepad used to set this up has the following characteristics
# When running the controller test program, the axes are as follows:
#
# 0: Left stick's left-to-right. Left is -1, right is 1
# 1: Left stick's up-to-down. Up is -1, down is 1
# **When the mode light on the controller is red
# 2: Right stick's left-to-right. Left is -1, right is 1
# 3: Right stick's up-to-down. Up is -1, down is 1
#
# The buttons are straightforward. Each button has a number on it, n, and
# and number that represents in in the code, m.
# m = n - 1
# If the button says 1 on it, then the client code has it as button 0
# There are 12 buttons in this manner, 1-12 or 0-11
#
#
# This code will be compatible with other controllers, but the behavior is not guaranteed,
# don't go to competition without verifying the controller works the way it is expected to
# on the hardware it is running in
#


def handlebutton(number, value):
    """
    This command takes information from the pygame library button events to send the correct 2 byte sequence
    :param number: the number of the button, as represented as m
    :param value: pressed or released
    :return no return. prints what button was pressed though
    """
    if value == 0:  # button has been pressed. most methods will activate on this condition
        if number == 0:   # on the steelseries gamepad, this in the top button on the right
            print("1 pressed")
            senddata(b'\xB1')
        elif number == 1: # on the steelseries gamepad, this in the right button on the right
            print("2 pressed")
            senddata(b'\xB2')
        elif number == 2: # on the steelseries gamepad, this in the bottom button on the right
            print("3 pressed")
            senddata(b'\xB3')
        elif number == 3: # on the steelseries gamepad, this in the left button on the right
            print("4 pressed")
            senddata(b'\xB4')
        elif number == 4: # on the steelseries gamepad, this in the trigger button on the left
            print("5 pressed")
            senddata(b'\xB5')
        elif number == 5: # on the steelseries gamepad, this in the trigger button on the right
            print("6 pressed")
            senddata(b'\xB6')
        elif number == 6: # on the steelseries gamepad, this in the bumper button on the left
            print("7 pressed")
            senddata(b'\xB7')
        elif number == 7: # on the steelseries gamepad, this in the bumper button on the right
            print("8 pressed")
            senddata(b'\xB8')
        elif number == 8: # on the steelseries gamepad, this is the left middle button
            print("9 pressed")
            senddata(b'\xB9')
        elif number == 9: # on the steelseries gamepad, this is the right middle button
            print("10 pressed")
            senddata(b'\xB0')
        elif number == 10: # on the steelseries gamepad, this is pressing the left control stick in
            print("11 pressed")
            senddata(b'\xBA')
        elif number == 11: # on the steelseries gamepad, this is pressing the right control stick in
            print("12 pressed")
            senddata(b'\xBB')
        else:
            print("This isn't a supported button!")
            print("This shouldn't do anything")


def handleaxis(number, value):
    """
    This command takes information from the pygame library axis events to send the correct 2 byte sequence
    :param number: number of axis. there are two axes per control stick
    :param value: value representing where along the axis the control stick lies
    :return no return. prints information about control stick movements
    """
    if number == 0: # left stick's left to right
        if value < -0.5:
            print("Left stick to the left")
            senddata( b'\xD9')
        elif value > 0.5:
            print("Left stick to the right")
            senddata( b'\xD7')
        #else:
            #   senddata( b'\xD1')
            #   print("Left stick LR neutral")
    elif number == 1: # left stick's up to down
        if value < -0.5:
            print("Left stick forward")
            senddata( b'\xD6')
        elif value > 0.5:
            print("Left stick backward")
            senddata( b'\xD8')
        #else:
        #    senddata( b'\xD5')
        #    print("Left stick UD neutral")
        elif number == 2: # right stick's left to right
            if value < -0.5:
                print("Right stick left")
                senddata( b'\xDE')
            elif value > 0.5:
                print("Right stick right")
                senddata( b'\xDC')
        #else:
        #    senddata( b'\xDA')
        #    print("Right stick LR neutral")
    elif number == 3: # right stick's up to down
        if value < -0.5:
            senddata( b'\xDB')
            print("Right stick up")
        elif value > 0.5:
            senddata( b'\xDD')
            print("Right stick down")
        #else:
        #senddata( b'\xDA')
        #    print("Right stick UD neutral") '''


def handlehat(number, value):
    """
    This command takes information from the pygame library hat (or dpad) events to send the correct 2 byte sequence
    :param number: which
    :param value: contains two values, which work together similar to two bits to define 4 dpad positions
    :return: no return. prints output for each dpad action.
    """
    if number == 0: # the only dpad
        if value[0] == 0 and value[1] == 1:  # this value indicates up
            print("DPad up")
            senddata(b'\xD1')
        elif value[0] == 1 and value[1] == 0:  # this value indicates right
            print("DPad right")
            senddata(b'\xD2')
        elif value[0] == 0 and value[1] == -1:  # this value indicates down
            print("DPad down")
            senddata(b'\xD3')
        elif value[0] == -1 and value[1] == 0:  # this value indicates left
            print("DPad left")
            senddata(b'\xD4')


def handlecontrol(number, value, conttype="button"):
    """
    This command forwards the relevant event information to the correct handler functions.
    All commands go through this function first.
    :param number: the ID number of the button, axis, or other control
    :param value:   the value inputted. the meaning will depend on control type.
                    button values are down and up for pressed and released
                    respectively
    :param conttype: short for control type. default is "button". there is also "axis" and "hat"
    :return:
    """
    if conttype == "button":
        handlebutton(number, value)
    elif conttype == "axis":
        handleaxis(number, value)
    elif conttype == "hat":
        handlehat(number, value)


# Main Control Loop Below #

def main():
    """
    This is the first thing that runs in client.py. It's an infinite loop to handle all controller events
    by sending important information from them to the relevant commands.
    :return: no return
    """
    while True:  # during control loop
        joystick = pygame.joystick.Joystick(0)  # assume the first joystick found was the one intended to use
        joystick.init()                         # initialize the event handlers for the controller
        # command handling. events should be sent to server
        for event in pygame.event.get():        # pygame.event is a queue of commands sent from a controller
            if event.type == pygame.JOYAXISMOTION:  # if the command is from a joystick moving
                handlecontrol(event.axis,event.value,"axis")
            if event.type == pygame.JOYBUTTONDOWN:  # if the command is a button being pressed
                handlecontrol(event.button,0,"button")
            if event.type == pygame.JOYBUTTONUP:    # if the command is a button being released
                handlecontrol(event.button,1,"button")
            if event.type == pygame.JOYHATMOTION:   # if the command is a d-pad being pressed
                handlecontrol(event.hat,event.value,"hat")


main()