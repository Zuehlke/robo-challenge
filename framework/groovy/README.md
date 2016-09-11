# Groovy 2.4.x (with embedded Java version)
## ev3dev-lang-java
The Groovy example is based on the [ev3dev-lang-java](https://github.com/ev3dev-lang-java/ev3dev-lang-java/) Java package for the EV3. 


## API documentation
- Java language bindings: http://ev3dev-lang-java.github.io/docs/api/
- ev3dev language bindings: http://ev3dev-lang.readthedocs.io/en/latest/

## Setting up the EV3 brick
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


## Development environment
It's up to you how you want to develop. This section is just a suggestion how you could setting up your Java environment.

First download the latest Java SE (JDK) version (http://www.oracle.com/technetwork/java/javase/downloads/index.html).

Next you need IDE, you could use InteliJ IDEA community version (https://www.jetbrains.com/idea/) or eclipse (https://eclipse.org).

### Execute the program

1.) Copy the start script (robot_groovy.sh) and the Groovy program (Robot.groovy) to the EV3 brick.

2.) Make the start script executable.
```bash
chomd 755 robot_groovy.sh
```



__Note:__ For a faster execution you might consider to compile the Groovy code

### Grab (Dependency management)

To automatically import the _ev3dev-lang-java_ dependencies you can use Grab (http://docs.groovy-lang.org/latest/html/documentation/grape.html). Just add to the first import 
statement the following annotations.

```java
@GrabResolver(name = "jitpack.io", root = "https://jitpack.io")
@Grab(group = "com.github.jabrena", module = "ev3dev-lang-java", version = "v0.2.0")
```

### Compile Groovy code
groovyc is the Groovy compiler command line tool. It allows you to compile Groovy 
sources into bytecode (http://groovy-lang.org/groovyc.html).

Or you can use the gmavenplus Maven plugin (https://github.com/groovy/GMavenPlus/wiki).
```xml
<build>
    <plugins>
      
      <plugin>
        <groupId>org.codehaus.gmavenplus</groupId>
        <artifactId>gmavenplus-plugin</artifactId>
        <version>1.4</version>
        <executions>
          <execution>
            <goals>
              <goal>compile</goal>
              <goal>testCompile</goal>
            </goals>
          </execution>
        </executions>
      </plugin>
      </plugins>
</build>
```  

## Basic Robot Example
An example program that is written in Groovy and that uses the ev3dev-lang-java lib can be found here. 
- [Robot.groovy](Robot.groovy)