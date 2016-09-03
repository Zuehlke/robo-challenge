# Java (JDK 8)
## ev3dev-lang-java
The Java example is based on the [ev3dev-lang-java](https://github.com/ev3dev-lang-java/ev3dev-lang-java/) Java package for the ev3. 


## API Documentation
- You must build the Javadoc by yourself. See https://github.com/ev3dev-lang-java/ev3dev-lang-java
- ev3dev language bindings: http://ev3dev-lang.readthedocs.io/en/latest/

## Setting Up the EV3 Brick
First, you need to setup a JVM on the robot. Thankfully, Oracle provides a
Java embedded version, that runs on a Mindstorms Brick.

1.) download "Oracle Java SE Embedded version 7 Update 60" from http://www.oracle.com/technetwork/java/embedded/downloads/javase/javaseemeddedev3-1982511.html

2.) copy ejre-7u60-fcs-b19-linux-arm-sflt-headless-07_may_2014.tar.gz to robot.

3.) extract compressed file (tar -xvf ejre-7u60-fcs-b19-linux-arm-sflt-headless-07_may_2014.tar.gz)

4.) remove compressed file

5.) set JAVA_HOME path




#### Execute the program

After building your program, upload your application as well as the
ev3-lang-java-0.2-SNAPSHOT.jar to your robot. After that you can execute:

```bash
java -cp <project-name>-SNAPSHOT.jar:ev3-lang-java-0.2-SNAPSHOT.jar <path-to-class-with-main>
```

## Development Environment

#### Maven dependency

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