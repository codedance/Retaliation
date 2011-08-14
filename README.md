
## RETALIATION - A Jenkins "Extreme Feedback" Contraption

### Summary

Retaliation is a <a href="http://jenkins-ci.org/">Jenkins CI</a> build monitor that 
automatically coordinates a foam missile counter-attack against the developer who "breaks 
the build". It does this by playing a preprogrammed control sequence to a *Cheeky Dream USB 
Thunder Foam Missle Lanucher* to target the offending code monkey.

**Lava Lamps are for pussies. You need Retaliation!**

<img src="https://github.com/codedance/Retaliation/raw/master/img/launcher.jpg">

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
> could never deliver! We've seen a 22.871% decrease in build breakage since its 
> implementation.</em>
> 
>    **Will, Chief Code Hacker**
***
> <em>Does what it says on the box. We've seen improvements and we haven't even installed it
> yet! Just the shear threat has kicked my team's coders into line.</em>
> 
>    **Tom, Head Code Captain**
***
> <em>Honestly, would you work in a dev team with a Lava Lamp build notifier? What next?
> Nyan Cat mouse mats? Real coders work under the treat of Retaliation!</em>
> 
>    **Matt, Coding Machine**
***
 
### How to Use

  1.  Mount your Dream Cheeky Thunder missile launcher in a central and 
      fixed location.

  2.  Copy this script onto the system connected to your missile lanucher.

  3.  Modify your `COMMAND_SETS` in the `retaliation.py` script to define your targeting 
      commands for each one of your build-braking coders (their user ID as listed 
      in Jenkins).  A command set is an array of move and fire commands. It is recommend
      to start each command set with a "reset" command.  This parks the launcher in a known
      position (bottom-left).  You can then use "up" and "right" followed by a time (in 
      milliseconds) to position your fire.
 
      You can test a set by calling retaliation.py with the target name. e.g.:  

           retaliation.py "[developer's user name]"

      Trial and error is the best approch. Consider doing this secretly after hours!

  4.  Setup the Jenkins <a href="https://wiki.jenkins-ci.org/display/JENKINS/Notification+Plugin">notification plugin</a>. 
      Define a `UDP` endpoint on port `22222`.

  5.  Start listening for failed build events by running the command:

           retaliation.py stalk

      (Consider setting this up as a boot/startup script)

  6.  Let the games begin!

####  Requirements:

  * A <a href="http://www.dreamcheeky.com/thunder-missile-launcher">Dream Cheeky Thunder USB Missile Launcher</a>. It may work with other models but only tested with this one.
  * Python 2.6+
  * Python PyUSB Support (on Mac use brew to "brew install libusb")

Thanks to the dev team at <a href="http://www.papercut.com/">PaperCut</a> writing print 
management software for "coping a few in the head" during testing!

*Tip:* If your dev team is down under and you're finding Retaliation is loosing its affect,
try dipping each missile in roo poo for some added punch :-)

