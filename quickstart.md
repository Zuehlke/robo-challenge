# Quickstart
Welcome to the Zühlke RoboChallenge. You have received the following components for the challenge:
* Lego Mindstorms Education Kit. ([What are the difference between education and retail kit](http://robotsquare.com/2013/11/25/difference-between-ev3-home-edition-and-education-ev3/))
* Wirless dongle
* SD card (microSD or microSDHC) with pre-installed [ev3dev](http://www.ev3dev.org) (Debian Linux-based operating system)

###First steps
The [ev3dev tutorial](http://www.ev3dev.org/docs/getting-started/) is a good way to get started with your EV3 brick. We have already prepared step 1 (download the image) and step 2 (install the image on the sd card). 


### Connecting to the EV3 brick
Step 5 describes how you can connect to your EV3 brick. The easiest way is to connect with SSH over USB cable or wireless network. (Hint: when you enabled your wireless connection you should change your password)

The default settings are:
* username: _robot_
* password: _maker_

To change the password use the _passwd_ command.
```
passwd robot
```

### Choose your language
You should use one of the official [language bindings](https://github.com/ev3dev/ev3dev-lang) or a recommended [libraries](http://www.ev3dev.org/docs/libraries/). 
The official language bindings should implement the language binding [specification](http://ev3dev-lang.readthedocs.io).

We have already provided some basic examples to get you started very quickly. 
* see supported [Frameworks](framework) for the Zühlke RoboChallenge.



### Development & deployment 
You should consider an easy solution to test and deploy your code to the EV3 brick. 

Tools which you can use to connect to your EV3 brick. 
- __ssh__ command (Linux & Mac), http://linuxcommand.org/man_pages/ssh1.html
- PuTTY (Windows), http://www.putty.org/


Tools for copying files to your EV3 brick.
- __scp__ command (Linux & Mac), http://linux.die.net/man/1/scp
- Cyberduck (Mac & Windows), https://cyberduck.io/
- WinSCP (Windows), https://winscp.net/eng/index.php


### Start you engine (or program)
In development mode you can start your program over SSH (cable or wifi) but during the challenges you must start your program from the EV3 file browser menu. To archive that your program must be executable. 

To make your script executable just use the _chmod_ command and add [shebang](https://bash.cyberciti.biz/guide/Shebang) at the top of your script. 
The shebang should point to your interpreter (Python, Node, etc.). 

```
chomod a+x your_script
```

For Java or other compiled languages create an executable shell script as wrapper.

```
#/bin/bash
java -jar path_to_your_jar
```

### Sensors
The ev3dev project provides a list of all supported sensors with all the values and modes which can be used. You should only consider the EV3 sensors.
- http://www.ev3dev.org/docs/sensors/

In the education kit you have the following sensors:
- 1x EV3 Ultrasonic Sensor (distance)
- 1x EV3 Gyro Sensor (rotation or movement)
- 1x EV3 Color Sensor (color reflection)
- 2x EV3 Touch Sensor

All sensors (INPUT) must be connected to the numbered EV3 ports (1,2,3 or 4). 

### Motors
The ev3dev project provides a list of all supported motors with all the 
settings which can be used. You should only consider the EV3 motors.
- http://www.ev3dev.org/docs/motors/

The education kit has the following motors:
- 2x EV3 Large Servo Motor
- 1x EV3 Medium Servo Motor

All motors (OUTPUT) must be connected to the alphabetic EV3 ports (A,B,C or D). 


### Sound
How to speak or play sound with your ev3dev is described [here](https://github.com/ev3dev/ev3dev/wiki/Using-Sound).

### FAQ

#####Why is the motor 'speed_sp' property not working?
The problem might be that the 'speed_regulation' setting ist set to 'off'. So try to set 'speed_regulation' to 'on'. 

Bash:

```Bash
echo "on" > speed_regulation
```
Python:
```python
right_motor.speed_regulation_enabled = 'on'
```
JavaScript:
```javascript
motorRight.setString("speed_regulation", "on")
```

### Useful links
* Basic Linux commands, http://www.comptechdoc.org/os/linux/usersguide/linux_ugbasics.html
* Debian Linux reference, https://www.debian.org/doc/manuals/debian-reference/
* Setting up Push-to-Deploy with git, http://krisjordan.com/essays/setting-up-push-to-deploy-with-git
* How To Set Up Automatic Deployment with Git, https://www.digitalocean.com/community/tutorials/how-to-set-up-automatic-deployment-with-git-with-a-vps

