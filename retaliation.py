#!/usr/bin/python
#
# Copyright 2011 PaperCut Software Int. Pty. Ltd. http://www.papercut.com/
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
# 

############################################################################
# 
# RETALIATION - A Jenkins "Extreme Feedback" Contraption
#
#    Lava Lamps are for pussies! Retaliate to a broken build with a barrage 
#    of foam missiles.
#
# Steps to use:
#
#  1.  Mount your Dream Cheeky Thunder USB missile launcher in a central and 
#      fixed location.
#
#  2.  Copy this script onto the system connected to your missile lanucher.
#
#  3.  Modify your `COMMAND_SETS` in the `retaliation.py` script to define 
#      your targeting commands for each one of your build-braking coders 
#      (their user ID as listed in Jenkins).  A command set is an array of 
#      move and fire commands. It is recommend to start each command set 
#      with a "zero" command.  This parks the launcher in a known position 
#      (bottom-left).  You can then use "up" and "right" followed by a 
#      time (in milliseconds) to position your fire.
# 
#      You can test a set by calling retaliation.py with the target name. 
#      e.g.:  
#
#           retaliation.py "[developer's user name]"
#
#      Trial and error is the best approch. Consider doing this secretly 
#      after hours for best results!
#
#  4.  Setup the Jenkins "notification" plugin. Define a UDP endpoint 
#      on port 22222 pointing to the system hosting this script.
#      Tip: Make sure your firewall is not blocking UDP on this port.
#
#  5.  Start listening for failed build events by running the command:
#          retaliation.py stalk
#      (Consider setting this up as a boot/startup script. On Windows 
#      start with pythonw.exe to keep it running hidden in the 
#      background.)
#
#  6.  Wait for DEFCON 1 - Let the war games begin!
#
#
#  Requirements:
#   * A Dream Cheeky Thunder USB Missile Launcher
#   * Python 2.6+
#   * Python PyUSB Support and its dependencies 
#      http://sourceforge.net/apps/trac/pyusb/
#      (on Mac use brew to "brew install libusb")
#   * Should work on Windows, Mac and Linux
#
#  Author:  Chris Dance <chris.dance@papercut.com>
#  Version: 1.0 : 2011-08-15
#
############################################################################

import sys
import platform
import time
import socket
import re
import json
import urllib2
import base64

import usb.core
import usb.util

##########################  CONFIG   #########################

#
# Define a dictionary of "command sets" that map usernames to a sequence 
# of commands to target the user (e.g their desk/workstation).  It's 
# suggested that each set start and end with a "zero" command so it's
# always parked in a known reference location. The timing on move commands
# is milli-seconds. The number after "fire" denotes the number of rockets
# to shoot.
#
COMMAND_SETS = {
    "will" : (
        ("zero", 0), # Zero/Park to know point (bottom-left)
        ("led", 1), # Turn the LED on
        ("right", 3250),
        ("up", 540),
        ("fire", 4), # Fire a full barrage of 4 missiles
        ("led", 0), # Turn the LED back off
        ("zero", 0), # Park after use for next time
    ),
    "tom" : (
        ("zero", 0), 
        ("right", 4400),
        ("up", 200),
        ("fire", 4),
        ("zero", 0),
    ),
    "chris" : (      # That's me - just dance around and missfire!
        ("zero", 0),
        ("right", 5200),
        ("up", 500),
        ("pause", 5000),
        ("left", 2200),
        ("down", 500),
        ("fire", 1),
        ("zero", 0),
    ),
}

#
# The UDP port to listen to Jenkins events on (events are generated/supplied 
# by Jenkins "notification" plugin)
#
JENKINS_NOTIFICATION_UDP_PORT   = 22222

#
# The URL of your Jenkins server - used to callback to determine who broke 
# the build.
#
JENKINS_SERVER                  = "http://192.168.1.100:23456"

#
# If you're Jenkins server is secured by HTTP basic auth, sent the
# username and password here.  Else leave this blank.
HTTPAUTH_USER                   = ""
HTTPAUTH_PASS                   = ""

##########################  ENG CONFIG  #########################

# The code...

# Protocol command bytes
DOWN    = 0x01
UP      = 0x02
LEFT    = 0x04
RIGHT   = 0x08
FIRE    = 0x10
STOP    = 0x20

DEVICE = None
DEVICE_TYPE = None

def usage():
    print "Usage: retaliation.py [command] [value]"
    print ""
    print "   commands:"
    print "     stalk - sit around waiting for a Jenkins CI failed build"
    print "             notification, then attack the perpetrator!"
    print ""
    print "     up    - move up <value> milliseconds"
    print "     down  - move down <value> milliseconds"
    print "     right - move right <value> milliseconds"
    print "     left  - move left <value> milliseconds"
    print "     fire  - fire <value> times (between 1-4)"
    print "     zero  - park at zero position (bottom-left)"
    print "     pause - pause <value> milliseconds"
    print "     led   - turn the led on or of (1 or 0)"
    print ""
    print "     <command_set_name> - run/test a defined COMMAND_SET"
    print "             e.g. run:"
    print "                  retaliation.py 'chris'"
    print "             to test targeting of chris as defined in your command set."
    print ""


def setup_usb():
    # Tested only with the Cheeky Dream Thunder
    # and original USB Launcher
    global DEVICE 
    global DEVICE_TYPE

    DEVICE = usb.core.find(idVendor=0x2123, idProduct=0x1010)

    if DEVICE is None:
        DEVICE = usb.core.find(idVendor=0x0a81, idProduct=0x0701)
        if DEVICE is None:
            raise ValueError('Missile device not found')
        else:
            DEVICE_TYPE = "Original"
    else:
        DEVICE_TYPE = "Thunder"

    

    # On Linux we need to detach usb HID first
    if "Linux" == platform.system():
        try:
            DEVICE.detach_kernel_driver(0)
        except Exception, e:
            pass # already unregistered    

    DEVICE.set_configuration()


def send_cmd(cmd):
    if "Thunder" == DEVICE_TYPE:
        DEVICE.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, cmd, 0x00,0x00,0x00,0x00,0x00,0x00])
    elif "Original" == DEVICE_TYPE:
        DEVICE.ctrl_transfer(0x21, 0x09, 0x0200, 0, [cmd])

def led(cmd):
    if "Thunder" == DEVICE_TYPE:
        DEVICE.ctrl_transfer(0x21, 0x09, 0, 0, [0x03, cmd, 0x00,0x00,0x00,0x00,0x00,0x00])
    elif "Original" == DEVICE_TYPE:
        print("There is no LED on this device")

def send_move(cmd, duration_ms):
    send_cmd(cmd)
    time.sleep(duration_ms / 1000.0)
    send_cmd(STOP)


def run_command(command, value):
    command = command.lower()
    if command == "right":
        send_move(RIGHT, value)
    elif command == "left":
        send_move(LEFT, value)
    elif command == "up":
        send_move(UP, value)
    elif command == "down":
        send_move(DOWN, value)
    elif command == "zero" or command == "park" or command == "reset":
        # Move to bottom-left
        send_move(DOWN, 2000)
        send_move(LEFT, 8000)
    elif command == "pause" or command == "sleep":
        time.sleep(value / 1000.0)
    elif command == "led":
        if value == 0:
            led(0x00)
        else:
            led(0x01)
    elif command == "fire" or command == "shoot":
        if value < 1 or value > 4:
            value = 1
        # Stabilize prior to the shot, then allow for reload time after.
        time.sleep(0.5)
        for i in range(value):
            send_cmd(FIRE)
            time.sleep(4.5)
    else:
        print "Error: Unknown command: '%s'" % command


def run_command_set(commands):
    for cmd, value in commands:
        run_command(cmd, value)


def jenkins_target_user(user):
    match = False
    # Not efficient but our user list is probably less than 1k.
    # Do a case insenstive search for convenience.
    for key in COMMAND_SETS:
        if key.lower() == user.lower():
            # We have a command set that targets our user so got for it!
            run_command_set(COMMAND_SETS[key])
            match = True
            break
    if not match:
        print "WARNING: No target command set defined for user %s" % user


def read_url(url):
    request = urllib2.Request(url)

    if HTTPAUTH_USER and HTTPAUTH_PASS:
        authstring = base64.encodestring('%s:%s' % (HTTPAUTH_USER, HTTPAUTH_PASS))
        authstring = authstring.replace('\n', '')
        request.add_header("Authorization", "Basic %s" % authstring)

    return urllib2.urlopen(request).read()


def jenkins_get_responsible_user(job_name):
    # Call back to Jenkins and determin who broke the build. (Hacky)
    # We do this by crudly parsing the changes on the last failed build
    
    changes_url = JENKINS_SERVER + "/job/" + job_name + "/lastFailedBuild/changes"
    changedata = read_url(changes_url)

    # Look for the /user/[name] link
    m = re.compile('/user/([^/"]+)').search(changedata)
    if m:
        return m.group(1)
    else:
        return None


def jenkins_wait_for_event():

    # Data in the format: 
    #   {"name":"Project", "url":"JobUrl", "build":{"number":1, "phase":"STARTED", "status":"FAILURE" }}

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', JENKINS_NOTIFICATION_UDP_PORT))

    while True:
        data, addr = sock.recvfrom(8 * 1024)
        try:
            notification_data = json.loads(data)
            status = notification_data["build"]["status"].upper()
            phase  = notification_data["build"]["phase"].upper()
            if phase == "FINISHED" and status.startswith("FAIL"):
                target = jenkins_get_responsible_user(notification_data["name"])
                if target == None:
                    print "WARNING: Could not identify the user who broke the build!"
                    continue

                print "Build Failed! Targeting user: " + target
                jenkins_target_user(target)
        except:
            pass
                

def main(args):

    if len(args) < 2:
        usage()
        sys.exit(1)

    setup_usb()

    if args[1] == "stalk":
        print "Listening and waiting for Jenkins failed build events..."
        jenkins_wait_for_event()
        # Will never return
        return

    # Process any passed commands or command_sets
    command = args[1]
    value = 0
    if len(args) > 2:
        value = int(args[2])

    if command in COMMAND_SETS:
        run_command_set(COMMAND_SETS[command])
    else:
        run_command(command, value)


if __name__ == '__main__':
    main(sys.argv)
