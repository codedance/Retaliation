## Retaliation - A Jenkins "Extreme Feedback" Contraption

### Summary

Retaliation is a Jenkins CI build monitor that automatically coordinates a foam missile
counter-attack against the developer who "breaks the build". It does this by playing a
preprogrammed control sequence to a Cheeky Dream USB Thunder Foam Missle Lanucher to target
the offending code monkey.

<em>Lava Lamps are for pussies. You need Retaliation!</em>

<img src="http://codedance.github.com/Retaliation/img/launcher.jpg">

### In Death

At a deeper level <strong>Retaliation</strong> is more than just a "simple python script". 
It's a radical rethink into how to manage software development teams and the software 
development life cycle.  It works on a deep physiological level to offer productivity 
improvements unseen in all those other "extreme programming" things consultants speak 
about.  The primal threat of mutually assured destruction lurking in every coder's psyche 
ensures that even your sloppiest developers will never forget to "checkin that missing 
file" again!

### Testimonials

> Retaliation brought us the productivity improvement pair-programming promised but could 
> never deliver! We've seen a 22.871% decrease in build breakage since its implementation.
> 
> <em>Will, Chief Code Hacker</em>

> Does what it says on the box. We've seen improvements and we haven't even installed it
> yet! Just the shear threat has kicked my team's coders into line.
> 
> <em>Tom, Head Code Captain</em>

> Honestly, would you work in a dev team with a Lava Lamp build notifier? What next?
> Naan Cat mouse mats? Real coders work under the treat of Retaliation! 
> 
> <em>Matt, Coding Machine</em>

### How to use

  1.  Mount your Dream Cheeky Thunder missile launcher in a central and 
      fixed location.

  2.  Copy this script onto the system connected to your missile lanucher.

  3.  Modify your COMMAND_SETS so there is a target defined for each of 
      your build-braking coders (their user ID as listed in Jenkins).  
      You can test a set by calling it with the command:  

           `retaliation.py "[developer name]"`

      Trial and error is the best approch. Consider doing this secretly
      after hours!

  4.  Setup the Jenkins "notification" plugin. Define a UDP endpoint 
      on port 22222.

  5.  Start listening for failed build events by running the command:

           `retaliation.py stalk`

      (Consider setting this up as a boot script)

  6.  Let the games begin!

####  Requirements:

  * A <a href="http://www.dreamcheeky.com/thunder-missile-launcher">Dream Cheeky Thunder USB Missile Launcher</a>.
  * Python 2.6+
  * Python PyUSB Support (on Mac use brew to "brew install libusb")

Thanks to the team at <a href="http://www.papercut.com/">PaperCut</a> for "coping a few
in the head" during testing!

