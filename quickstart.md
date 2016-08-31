# Quickstart
Welcome to the Zühlke RoboChallenge. You have received the following components for the challenge:
* Lego Mindstorms Education Kit. ([What are the difference between education and retail kit](http://robotsquare.com/2013/11/25/difference-between-ev3-home-edition-and-education-ev3/))
* Wifi dongle
* SD card with pre-installed [ev3dev](http://www.ev3dev.org) (Debian Linux-based operating system)

###First steps
The [ev3dev tutorial](http://www.ev3dev.org/docs/getting-started/) is a good way to get started with your ev3 brick. We have already prepared step 1 (download the image) and step 2 (install the image on the sd card). 


### Connecting to the ev3 brick
Step 5 describes how you can connect to your ev3 brick. The easiest way is to connect with SSH over USB cable or wifi network. (Hint: when you enabled your wifi connection you should change your password)

The default settings are:
* username: _robot_
* password: _maker_

To chnage the password use the _passwd_ command.
```
passwd robot
```

### Choose your language
You should use one of the official [language bindings](https://github.com/ev3dev/ev3dev-lang) or a recommended [libraries](http://www.ev3dev.org/docs/libraries/). 
The official language binidings should implement the language binding [specification](http://ev3dev-lang.readthedocs.io).

We have already provided some basic examples to get you started very quickly. 
* [Python](framework/python) (recommended)
* [JavaScript](framework/javascript) (recommended)
* [Java](framework/java)
* [Bash](framework/bash)


### Development & Deployment 
You should consider an easy solution to test and deploy your code to the ev3 brick. 

Tools which you can use to connect to your ev3 brick. 
- __ssh__ command (Linux & Mac), http://linuxcommand.org/man_pages/ssh1.html
- http://www.putty.org/ (Windows)


Tools for transfering files to your ev3 brick.
- __scp__ command (Linux & Mac), http://linux.die.net/man/1/scp
- https://cyberduck.io/ (Mac)
- https://winscp.net/eng/index.php (Windows)


### Start you engine (or program)
In development mode you can start your program over SSH (cable or wifi) but during the challenges you must start your program from the ev3 file browser menu. To achive that your program must be executable. 

To make your script executable just use the _chmod_ command and add [shebang](https://bash.cyberciti.biz/guide/Shebang) at the top of your script. 
The shebang should point to your intepreter (Python, Node, etc.). 

```
chomod a+x your_script
```

For Java or other compiled languages create a executable shell script as wrapper.

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

All sensors must be connected to the numbered ev3 ports (1,2,3 or 4). 

### Motors
The education kit has the following motors:
- 2x EV3 Large Servo Motor
- 1x EV3 Medium Servo Motor

All motors must be connected to the alphabetic ev3 ports (A,B,C or D). 

### Sound
How to speak or play sound with your ev3dev is described [here](https://github.com/ev3dev/ev3dev/wiki/Using-Sound).

### Useful links
* Basic Linux commands - http://www.comptechdoc.org/os/linux/usersguide/linux_ugbasics.html
* Debian Linux reference - https://www.debian.org/doc/manuals/debian-reference/
* Setting up Push-to-Deploy with git - http://krisjordan.com/essays/setting-up-push-to-deploy-with-git
* How To Set Up Automatic Deployment with Git - https://www.digitalocean.com/community/tutorials/how-to-set-up-automatic-deployment-with-git-with-a-vps

