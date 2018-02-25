#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  client.py
#  
#  Copyright 2018 Garrett J Wedge <gjd36@lapaz.cs.unh.edu>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import socket
import pygame

PORT = 8000
IP = "127.0.0.1"
MESSAGE = "hello"

# test sending a message
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(MESSAGE, (IP, PORT))

pygame.init()  # init pygame
pygame.joystick.init()  # init pygame joysticks
joysticks = pygame.joystick.Joystick(x)

joycount = pygame.joystick.get_count()
print( joycount )
for x in range(0, joycount):
    print(joysticks)  # print list of connected controllers

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
# If the button says 1 on it, then the code has it as button 0
# There are 10 buttons in this manner
#
# There's also a d-pad, which I think pygame calls a "hat", but it hasn't been tested yet
#
# This code will be compatible with other controllers, but the behavior is not guaranteed,
# don't go to competition without verifying the controller works the way it is expected to
# in the hardware it is running in
#


def handlebutton(number, value):
    if value == 0:  # button has been pressed. most methods will activate on this condition
        if number == 0:   # on the steelseries gamepad, this in the top button on the right
            senddata(b'\xB1')
        elif number == 1: # on the steelseries gamepad, this in the right button on the right
            senddata(b'\xB2')
        elif number == 2: # on the steelseries gamepad, this in the bottom button on the right
            senddata(b'\xB3')
        elif number == 3: # on the steelseries gamepad, this in the left button on the right
            senddata(b'\xB4')
        elif number == 4: # on the steelseries gamepad, this in the trigger button on the left
            senddata(b'\xB5')
        elif number == 5: # on the steelseries gamepad, this in the trigger button on the right
            senddata(b'\xB6')
        elif number == 6: # on the steelseries gamepad, this in the bumper button on the left
            senddata(b'\xB7')
        elif number == 7: # on the steelseries gamepad, this in the bumper button on the right
            senddata(b'\xB8')
        elif number == 8: # on the steelseries gamepad, this is the left middle button
            senddata(b'\xB9')
        elif number == 9: # on the steelseries gamepad, this is the right middle button
            senddata(b'\xB0')
        elif number == 10: # on the steelseries gamepad, this is pressing the left control stick in
            senddata(b'\xBA')
        elif number == 11: # on the steelseries gamepad, this is pressing the right control stick in
            senddata(b'\xBB')
        else:
            print("This isn't a supported button!")
            print("This shouldn't do anything")


def handleaxis(number, value):
    if number == 0: # left stick's left to right
        if value < -0.5:
            print("Moving left")
            senddata( b'\xD9')
        elif value > 0.5:
            print("Moving right")
            senddata( b'\xD7')
        #else:
            #   senddata( b'\xD1')
            #   print("Left stick LR neutral")
    if number == 1: # left stick's up to down
        if value < -0.5:
            print("Moving forward")
            senddata( b'\xD6')
        elif value > 0.5:
            print("Moving backward")
            senddata( b'\xD8')
        #else:
            #    senddata( b'\xD5')
            #    print("Left stick UD neutral")
    if number == 2: # right stick's left to right
        if value < -0.5:
            print("Right stick left")
            senddata( b'\xDE')
        elif value > 0.5:
            print("Right stick right")
            senddata( b'\xDC')
        #else:
            #    senddata( b'\xDA')
            #    print("Right stick LR neutral")
    if number == 3: # right stick's up to down
        if value < -0.5:
            senddata( b'\xDB')
            print("Right stick up")
        elif value > 0.5:
            senddata( b'\xDD')
            print("Right stick down")
        #else:
            #senddata( b'\xDA')
            #    print("Right stick UD neutral")


def handlehat(number, value):
    if number == 0: # left stick's left to right
        if value < -0.5:
            print("Moving left")
            senddata( b'\xD4')
        elif value > 0.5:
            print("Moving right")
            senddata( b'\xD2')
        #else:
            #    senddata( b'\xD0')
            #    print("Left hat LR neutral")
    if number == 1: # left stick's up to down
        if value < -0.5:
            print("Moving forward")
            senddata( b'\xD1')
        elif value > 0.5:
            print("Moving backward")
            senddata( b'\xD3')
        #else:
            #   senddata( b'\xD0')
            #    print("Left hat UD neutral")


def handlecontrol( number, value, conttype = "button" ):
    """

    :param number: the ID number of the button, axis, or other control
    :param value:   the value inputted. the meaning will depend on control type.
                    button values are down and up for pressed and released
                    respectively
    :param conttype: default is "button". there is also "axis"
    :return:
    """
    if conttype == "button":
        handlebutton(number, value)
    elif conttype == "axis":
        handleaxis(number, value)
    elif conttype == "hat":
        handlehat(number, value)


def senddata( message ):
    sock.sendto( message, ( IP, PORT))

while True:  # during control loop
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    # command handling. events should be sent to server
    for event in pygame.event.get():
        if event.type == pygame.JOYAXISMOTION:
            handlecontrol(event.axis,event.value,"axis")
        if event.type == pygame.JOYBUTTONDOWN:
            handlecontrol(event.button,0,"button")
        if event.type == pygame.JOYBUTTONUP:
            handlecontrol(event.button,1,"button")
        if event.type == pygame.JOYHATMOTION:
            handlecontrol(event.hat,event.value,"hat")

