# Quickstart
Welcome to the Zuehlke Robo Challenge. You have received the following components for the robo challenge:
* Lego Mindstorms Education Kit. ([What are the difference between education and retail kit](http://robotsquare.com/2013/11/25/difference-between-ev3-home-edition-and-education-ev3/))
* Wifi dongle
* SD card with pre-installed [ev3dev](http://www.ev3dev.org) (Debian Linux-based operating system)

The [ev3dev tutorial](http://www.ev3dev.org/docs/getting-started/) is a good way to get started with your ev3 brick. We have already prepared step 1 (download the image) and step 2 (install the image on the sd card). 


## Connecting to the ev3 brick
Step 4 describes how you can connect to your ev3 brick. The easiest way is to connect with SSH over USB cable or wifi network. (Hint: when you enabled your wifi connection you should change your password)

The default settings are:
* username: _robot_
* password: _maker_

## Choose your language
You should use one of the official [language bindings](https://github.com/ev3dev/ev3dev-lang) or recommend [libraries](http://www.ev3dev.org/docs/libraries/).

We have already provded some basic examples to get you started very quickly. 
* [Python](framework/python)
* [JavaScript](framework/javascript)
* [Java](framework/java)
* [Bash](framework/bash)

## Deployment 
You should consider a easy soultion to deploy your code to the ev3 brick. A good solution ist to create a git repository on your ev3 brick with a git hoock. 
- see http://www.ev3dev.org/docs/tutorials/setting-up-python-pycharm/


## Start you engine (or program)
In development mode you can start your program over SHH (cable or wifi) but during the challenges you must start your program from the ev3 file browser menu. To start your program form the file browser your program must be executable. 

To make your a script executable just use the _chmod_ command and add [shebang[(https://en.wikipedia.org/wiki/Shebang_(Unix)) at the top of your script. 
The shebang should point to your intepreter (python, node, etc.) The following example should work

```
chomod a+x your_script
```

For java or other compiled language create a executable shell script which calls your program.

```
#/bin/bash
java -jar path_to_your_jar
```

## Sensors
The ev3dev provides a list of all supported sensors with the supported modes and values. You should only consider the EV3 sensors.
- http://www.ev3dev.org/docs/sensors/

## Engineering
tbd

## Useful links
* Basic Linux commands - http://www.comptechdoc.org/os/linux/usersguide/linux_ugbasics.html
* Debian Linux reference - https://www.debian.org/doc/manuals/debian-reference/
* Setting up Push-to-Deploy with git - http://krisjordan.com/essays/setting-up-push-to-deploy-with-git
* How To Set Up Automatic Deployment with Git - https://www.digitalocean.com/community/tutorials/how-to-set-up-automatic-deployment-with-git-with-a-vps

