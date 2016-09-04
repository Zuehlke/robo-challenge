# Java (Embedded version)
## ev3dev-lang-java
The Java example is based on the [ev3dev-lang-java](https://github.com/ev3dev-lang-java/ev3dev-lang-java/) Java package for the ev3. 


## API Documentation
- There is no online version available, so you must build the Javadoc by yourself. See https://github.com/ev3dev-lang-java/ev3dev-lang-java
- ev3dev language bindings: http://ev3dev-lang.readthedocs.io/en/latest/

## Setting Up the EV3 Brick
First, you need to setup up a JVM on the ev3 brick. Thankfully, Oracle provides a
Java embedded version, that runs on the ev3 brick.

1.) Download "Oracle Java SE Embedded version 7 Update 60" from http://www.oracle.com/technetwork/java/embedded/downloads/javase/javaseemeddedev3-1982511.html

2.) Copy ejre-7u60-b19-ejre-7u60-fcs-b19-linux-arm-sflt-headless-07_may_2014.tar.gz to your ev3 brick.

3.) Next extract the compressed file.
```bash
tar -xvf ejre-7u60-b19-ejre-7u60-fcs-b19-linux-arm-sflt-headless-07_may_2014.tar.gz
```

4.) Remove compressed file.

5.) Adapt the PATH and JAVA_HOME variable.








## Development Environment
It's up to you how you want to develop. This section is just a suggestion how you could setting up your Java environment.

First download the latest Java SE (JDK) version (http://www.oracle.com/technetwork/java/javase/downloads/index.html).

Next you need IDE, you could use InteliJ IDEA community version (https://www.jetbrains.com/idea/) or eclipse (https://eclipse.org).

### Build & execute the program
For a better and easier deployment we have provided you with a Maven [pom.xml](pom.xml) which bundles all required libraries (ev3-lang-java-*.jar, etc.) into one big jar file (ueber jar file). Then you have just to copy one big jar file.

1.) Just build the application with Apache Maven:
```bash
mvn clean packge
```

2.) Then copy the ueber-jar to the ev3 brick.

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