## RETALIATION - A Jenkins "Extreme Feedback" Contraption

*Status boards are for ‘project managers’! Retaliate to a broken build with a barrage of foam missiles.*

### Summary

Retaliation is a <a href="http://jenkins-ci.org/">Jenkins CI</a> build monitor that 
automatically coordinates a foam missile counter-attack against the developer who "breaks 
the build". It does this by playing a pre-programmed control sequence to a *USB Foam 
Missile Launcher* to target the offending code monkey.

<img src="https://github.com/codedance/Retaliation/raw/master/img/launcher.jpg" />&nbsp;&nbsp;&nbsp;<a href="http://www.youtube.com/watch?v=1EGk2rvZe8A"><img src="https://github.com/codedance/Retaliation/raw/master/img/demo-video.jpg" /></a>

### In Detail

At a deeper level <strong>Retaliation</strong> is more than just a "simple python script". 
It's a radical rethink into how to manage software development teams and the software 
development life cycle.  It works on a deep psychological level to offer productivity 
improvements unseen in all those other "extreme programming" things external consultants 
speak about. The primal threat of mutually assured destruction lurking in every coder's 
psyche ensures that even your sloppiest developers will never forget to "checkin that 
missing file" again!

### Testimonials

***
> <em>Retaliation brought us the productivity improvement pair-programming promised but 
> could never deliver! We've seen a 13.37% decrease in build breakage since its 
> implementation.</em>
> 
>    **Will, Chief Code Hacker**
***
> <em>Honestly, would you work in a dev team with a Lava Lamp build notifier? What next?
> Nyan Cat mouse mats? Real coders work under the threat of Retaliation!</em>
> 
>    **Matt, Coding Machine**
***
> <em>Does what it says on the box. I've seen improvements in my team and we haven't even 
> installed it yet! Just the sheer threat has kicked my team's coding into line.</em>
> 
>    **Tom, Head Code Captain**
***

You can see *Retaliation* in action <a href="http://www.youtube.com/watch?v=1EGk2rvZe8A">
in this video</a>.
 
### How to Use

  1.  Mount your <a href="http://www.dreamcheeky.com/thunder-missile-launcher">Dream Cheeky Thunder USB Missile Launcher</a> 
      in a central and fixed location.

  2.  Download the <a href="https://github.com/codedance/Retaliation/raw/master/retaliation.py">retaliation.py</a> 
      script onto the system connected to your missile launcher.

  3.  Modify your `COMMAND_SETS` in the `retaliation.py` script to define your targeting 
      commands for each one of your build-braking coders (their user ID as listed 
      in Jenkins).  A command set is an array of move and fire commands. It is recommend
      to start each command set with a "zero" command.  This parks the launcher in a known
      position (bottom-left).  You can then use "up" and "right" followed by a time (in 
      milliseconds) to position your fire.
 
      You can test a set by calling retaliation.py with the target name. e.g.:  

           python retaliation.py "[developer's user name]"

      Trial and error is the best approach. Consider doing this secretly after hours for
      best results!

  4.  Setup the Jenkins <a href="https://wiki.jenkins-ci.org/display/JENKINS/Notification+Plugin">notification plugin</a>. 
      Define a `UDP` endpoint on port `22222` pointing to the system hosting 
      `retaliation.py`.  *Tip:* Make sure your firewall is not blocking UDP on this port.

  5.  Start listening for failed build events by running the command:

           python retaliation.py stalk

      (Consider setting this up as a boot/startup script. On Windows start with `pythonw.exe`
      to keep it running hidden in the background.)

  6.  Wait for DEFCON 1 - Let the war games begin!

####  Requirements:

  * A <a href="http://www.dreamcheeky.com/thunder-missile-launcher">Dream Cheeky Thunder USB Missile Launcher</a>. 
    It may work with other models but I've only tested with this one.
  * Python 2.6+
  * Python PyUSB Support (on Mac use brew to "brew install libusb")
  * Should work on Windows, Mac and Linux

Thanks to the dev team at <a href="http://www.papercut.com/">PaperCut</a> (working on print 
management software) for "coping a few in the head" during testing!

### Tips

  * Carefully select the mounting location. Pick a central location in your office space. 
    Endeavor to maximize angular separation between targets. This will reduce the likelihood
    of friendly fire incidents... but then again this is comes with the territory and is all
    part of the fun!
    
  * Consider sticking down the launcher using double-sided tape to lock its position. This
    reduces the chance of someone using a "physical hack" to disrupt the coordinate 
   targeting system.


  * If your build breaking perpetrator is at point-blank range, for health and safety
    reasons we suggest targeting their keyboard or monitor rather than their head.

  * If you have a wide area to cover, consider multiple missile launches (e.g. cluster
    support!). Set the script up on multiple machines and configure multiple endpoint 
    notifications in Jenkins.

  * To get this working on Windows, you'll need to install 
    <a href="http://sourceforge.net/apps/trac/pyusb/">PyUSB</a> and
    <a href="http://sourceforge.net/apps/trac/libusb-win32/wiki">libusb-win32</a>.
    This can be a little tricky but if you've mastered CI build scripts then this
    should be easy!

  * If your dev team is Down Under and you're finding Retaliation is loosing its 
    effect, try dipping each missile in some <a href="http://en.wikipedia.org/wiki/Vegemite">Vegemite</a>
    for some added punch :-)

### News

  * Great to see Retaliation mashed up with the 
   <a href="http://www.raspberrypi.org/archives/tag/open-webos">Raspberry Pi</a>. 
    It's also got a metion in the 
   <a href="http://www.guardian.co.uk/technology/2012/nov/04/12-things-to-make-raspberry-pi?INTCMP=SRCH">Guardian</a> as the 4th best thing to do with the Pi!

### Future

  * Should we also make a version compatible with Hudson? :-)

### Other Uses
 
`retaliation.py` also doubles as a command-line scripting API for the *Dream Cheeky 
USB Missile Launcher*.  You can invoke it to control the device from a script or 
command-line as follows:

      retaliation.py reset
      retaliation.py right 3000
      retaliation.py up 700
      retaliation.py fire 1

If you do come up with some other cool uses or ideas for retaliation, please share 
your story!
        
