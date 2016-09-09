# Java 7 (Embedded version)
## ev3dev-lang-java
The Java example is based on the [ev3dev-lang-java](https://github.com/ev3dev-lang-java/ev3dev-lang-java/) Java package for the EV3. 


## API Documentation
- Java language bindings: http://ev3dev-lang-java.github.io/docs/api/
- ev3dev language bindings: http://ev3dev-lang.readthedocs.io/en/latest/

## Setting Up the EV3 Brick
First, you need to set up up a JVM on the EV3 brick. Thankfully, Oracle provides a
Java embedded version, that runs on the EV3 brick.

1.) Download "Oracle Java SE Embedded version 7 Update 60" from http://www.oracle.com/technetwork/java/embedded/downloads/javase/javaseemeddedev3-1982511.html

2.) Copy ejre-7u60-b19-ejre-7u60-fcs-b19-linux-arm-sflt-headless-07_may_2014.tar.gz to your EV3 brick.

3.) Next extract the compressed file.
```bash
tar -xvf ejre-7u60-b19-ejre-7u60-fcs-b19-linux-arm-sflt-headless-07_may_2014.tar.gz
```

4.) Remove compressed file.

5.) Add the PATH and JAVA_HOME variable to your start script.

```bash
export JAVA_HOME=/home/robot/ejre1.7.0_60
export PATH=$PATH:$JAVA_HOME/bin
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

### Maven settings (pom.xml)
When you want to build your own Maven project, you have to do the following steps.

1) add repository (in <repositories>) to your pom:

```xml
<repository>
  <id>jitpack.io</id>
  <url>https://jitpack.io</url>
</repository>
```

2) add the dependency
```xml
<dependency>
  <groupId>com.github.jabrena</groupId>
  <artifactId>ev3dev-lang-java</artifactId>
  <version>v0.2.0</version>
</dependency>
```

3) Add the moment we can only use Java 7 and so we have to set the source and target to _1.7_.
```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-compiler-plugin</artifactId>
    <version>3.5.1</version>
    <configuration>
        <!-- or whatever version you use -->
        <source>1.7</source>
        <target>1.7</target>
    </configuration>
</plugin>
```