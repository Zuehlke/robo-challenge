# Groovy 2.4.x (with embedded Java version)
## ev3dev-lang-java
The Groovy example is based on the [ev3dev-lang-java](https://github.com/ev3dev-lang-java/ev3dev-lang-java/) Java package for the EV3. 


## API Documentation
- Java language bindings: http://ev3dev-lang-java.github.io/docs/api/
- ev3dev language bindings: http://ev3dev-lang.readthedocs.io/en/latest/

## Setting Up the EV3 Brick
First, you need to set up up a JVM on the EV3 brick. 

1.) Have a look at our [Java](../java/) code example, how to set up a JVM on the EV3 brick. 

2.) Download the latest Groovy SDK (apache-groovy-sdk-2.4.7.zip) from http://www.groovy-lang.org

3.) Copy apache-groovy-sdk-2.4.7.zip to the EV3 

4.) Install the 'unzip' command with 'apt-get' on the EV3 brick. 
```bash
sudo apt-get install unzip
```

5.) Then unzip the Groovy SDK. 
```bash
unzip apache-groovy-sdk-2.4.7.zip
```

5.) Add the PATH, GROOVY_HOME and JAVA_HOME variable in your start script.

```bash
export JAVA_HOME=/home/robot/ejre1.7.0_60
export GROOVY_HOME=/home/robot/groovy-2.4.7

export PATH=$PATH:$JAVA_HOME/bin:$GROOVY_HOME/bin
```



## Development Environment
It's up to you how you want to develop. This section is just a suggestion how you could setting up your Java environment.

First download the latest Java SE (JDK) version (http://www.oracle.com/technetwork/java/javase/downloads/index.html).

Next you need IDE, you could use InteliJ IDEA community version (https://www.jetbrains.com/idea/) or eclipse (https://eclipse.org).

### Build & execute the program
For a better and easier deployment we have provided you with a Maven [pom.xml](pom.xml) which bundles all required libraries (ev3-lang-java-*.jar, etc.) into one big jar file (ueber jar file). Then you have just to copy one big jar file.

1.) Just build the application with Apache Maven:
```bash
mvn clean package
```

2.) Then copy the ueber-*.jar (_uber-ev3-robot-jdk-1.0-SNAPSHOT.jar_) to the EV3 brick.

### Grab settings
