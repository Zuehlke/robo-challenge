#!/bin/bash
export JAVA_HOME=/home/robot/ejre1.7.0_60
export GROOVY_HOME=/home/robot/groovy-2.4.7

export PATH=$PATH:$JAVA_HOME/bin:$GROOVY_HOME/bin

groovy -Dgroovy.grape.report.downloads=true -Divy.message.logger.level=4 -Divy.cache.ttl.default=24h Robot.groovy