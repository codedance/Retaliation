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
# A Jenkins "Extreme Feedback" Contraption
#
#    Lava Lamps are for pussies! Retaliate to a broken build with a barrage 
#    of foam missiles.
#
# Steps to use:
#
#  1.  Mount your Dream Cheeky Thunder missile launcher in a central and 
#      fixed location.
#
#  2.  Copy this script onto the system connected to your missile lanucher.
#
#  3.  Modify your COMMAND_SETS so there is a target defined for each of 
#      your build-braking coders (their user ID as listed in Jenkins).  
#      You can test a set by calling it with the command:  
#          retaliation.py "[developer name]"
#      Trial and error is the best approch. Consider doing this secretly
#      after hours!
#
#  4.  Setup the Jenkins "notification" plugin. Define a UDP endpoint 
#      on port 22222.
#
#  5.  Start listening for failed build events by running the command:
#          retaliation.py stalk
#      (Consider setting this up as a boot script)
#
#  6.  Let the games begin!
#
#
#  Requirements:
#   * A Dream Cheeky Thunder USB Missile Launcher
#   * Python 2.6+
#   * Python PyUSB Support (on Mac use brew to "brew install libusb")
#
#  Author: Chris Dance <chris.dance@papercut.com>
#
############################################################################

import sys
import time
import socket
import urllib
import re
import json

import usb.core
import usb.util

##########################  CONFIG   #########################

#
# Define a dictionary of "command sets" that map usernames to a sequence 
# of commands to target the user.  It's suggested that each set started and 
# end with a "zero" command. The timing is in milli-seconds. 
#
COMMAND_SETS = {
    "will.rayner" : (
        ("zero", 0),
        ("right", 2200),
        ("up", 600),
        ("fire", 4),
        ("zero", 0),
    ),
    "chris" : (
        ("right", 2200),
        ("pause", 2000),
        ("up", 500),
        ("left", 2200),
        ("down", 500),
        ("zero", 0),
    )
}

#
# The UDP port to listen to Jenkins events on (supplied by Jenkins 
# "notification" plugin)
#
JENKINS_NOTIFICATION_UDP_PORT   = 22222

#
# The URL of your Jenkins server - used to callback to determin who broke 
# the build.
#
JENKINS_SERVER                  = "http://localhost:23456"

##########################  ENG CONFIG  #########################


# Protocol command bytes
DOWN    = 0x01
UP      = 0x02
LEFT    = 0x04
RIGHT   = 0x08
FIRE    = 0x10
STOP    = 0x20

DEVICE = None

def usage():
    print "Usage: [command] [value]"
    print "   commands:"
    print "     stalk - sit around waiting for a Jenkins CI failed build"
    print "             notification, then attack the perpetrator."
    print ""
    print "     command_set - run a defined command_set (i.e. target)"
    print ""
    print "     up      - move up <value> milliseconds"
    print "     down    - move down <value> milliseconds"
    print "     right   - move right <value> milliseconds"
    print "     left    - move left <value> milliseconds"
    print "     fire    - fire <value> times (between 1-4)"
    print "     zero    - park at zero position (bottom-left)"
    print "     pause   - pause <value> milliseconds"
    print ""

def setup_usb():
    # Tested only works with the Cheeky Dream Thunder
    global DEVICE 
    DEVICE = usb.core.find(idVendor=0x2123, idProduct=0x1010)

    if DEVICE is None:
        raise ValueError('Missile device not found')

    DEVICE.set_configuration()


def send_cmd(cmd):
    DEVICE.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, cmd, 0x00,0x00,0x00,0x00,0x00,0x00])


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
    elif command == "zero" or command == "park":
        # Move to bottom-left
        send_move(DOWN, 2000)
        send_move(LEFT, 8000)
    elif command == "pause" or command == "sleep":
        time.sleep(value / 1000.0)
    elif command == "fire" or command == "shoot":
        if value < 1 or value > 4:
            value = 1
        # Stabilize prior to shot and allow reload time after
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
    for key in COMMAND_SETS:
        if key.lower() == user.lower():
            # We have a command set that targets our user to got for it!
            run_command_set(COMMAND_SETS[key])
            match = True
            break
    if not match:
        print "WARNING: No target command set defined for user %s" % user


def jenkins_get_responsible_user(job_name):
    # Call back to Jenkins and determin who broke the build.
    # We do this by crudly parsing the changes on the last failed build

    changes_url = JENKINS_SERVER + "/job/" + job_name + "/lastFailedBuild/changes"
    changedata = urllib.urlopen(changes_url).read()

    # Look for the /user/[name] link
    m = re.compile('"/user/([^/"]+)').search(changedata)
    if m:
        return m.group(1)
    else:
        return None


def jenkins_wait_for_event():

    # Data in the format: 
    #   {"name":"Project", "url":"JobUrl", "build":{"number":1, "phase":"STARTED", "status":"FAILED" }}

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', JENKINS_NOTIFICATION_UDP_PORT))

    while True:
        data, addr = sock.recvfrom(8 * 1024)
        try:
            notification_data = json.loads(data)
            if notification_data["build"]["status"] == "FAILED":
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
