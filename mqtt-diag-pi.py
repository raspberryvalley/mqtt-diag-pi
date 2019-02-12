#!/usr/bin/env python

#======================================================================
#
# Python Module to send Raspberry Pi system diagnostics to MQTT  
# * CPU Temperature [C]
# * CPU Load Percentage [%]
# * Disk Usage Percentage [%]
# * Memory Usage Percentage [%]
#
# Messages are published to the topic: system/<hostname>/<measurementname>
#
# Channels and parameters are defined in config.py
#
# Created at Raspberry Valley
#
# This code is in the public domain and may be freely copied and used
# No warranty is provided or implied
#
# Pre-Requisites:
# install Mosquitto: sudo apt-get install mosquitto mosquitto-clients
# install psutil: pip install psutil (or: sudo apt-get install python-psutil)
# install paho: paho sudo pip install paho-mqtt
# install logzero: pip install logzero
#
#======================================================================

try:
    import paho.mqtt.client as paho # https://raspberry-valley.azurewebsites.net/Mosquitto/
    import psutil # https://psutil.readthedocs.io/en/latest/
    from logzero import logger # https://www.metachris.com/2017/06/logzero---simplified-logging-for-python-2-and-3/
except ImportError:
    exit("This script requires the following modules (Install with):\n sudo pip install paho-mqtt\n sudo pip install psutil\n sudo pip install logzero")

import config
from subprocess import check_output
from re import findall
import socket, sys, time

#======================================================================
# MQTT broker code

MQTT_SERVER = config.broker
MQTT_PORT = config.broker_port

logger.info("Starting Paho MQTT client ('pidiag') at server '%s', port '%s'", MQTT_SERVER, MQTT_PORT)
logger.info("sending every {0} seconds".format(config.diag_sleep))

pidiagClient = paho.Client("pidiag")
pidiagClient.connect(MQTT_SERVER, MQTT_PORT)

#======================================================================
# Diagnostics functions

def get_hostname():
    return(socket.gethostname())

def get_temp():
    temp = check_output(["vcgencmd","measure_temp"]).decode("UTF-8")
    return(findall("\d+\.\d+",temp)[0])

def get_disk_usage():
    return str(psutil.disk_usage('/').percent)

def get_memory_usage():
    return str(psutil.virtual_memory().percent)

def get_cpu_usage():
    return str(psutil.cpu_percent(interval=None))

#======================================================================
# Main Loop

try:
    computer_name = get_hostname()
    logger.info("initializing Raspberry Valley MQTT system logger for {0}".format(computer_name))
    # prepare topics
    cpuTempTopic = config.cpu_temp_topic.format(computer_name)
    cpuUsageTopic = config.cpu_usage_topic.format(computer_name)
    diskUsageTopic = config.disk_usage_topic.format(computer_name)
    memUsageTopic = config.mem_usage_topic.format(computer_name)
    messageTopic = config.message_topic.format(computer_name)
    # run system measurements in continuous loop
    while True:
        temp = get_temp()
        cpu_usage = get_cpu_usage()
        disk_usage = get_disk_usage()
        memory_usage = get_memory_usage()

        pidiagClient.publish(cpuTempTopic, temp)
        pidiagClient.publish(cpuUsageTopic, cpu_usage)
        pidiagClient.publish(diskUsageTopic, disk_usage)
        pidiagClient.publish(memUsageTopic, memory_usage)

        logger.info("system diagnostics [{0}]: CPU temp {1}[C], CPU usage {2}[%], Disk usage {3}[%], Memory usage {4}[%]".format(computer_name, temp, cpu_usage, disk_usage, memory_usage))
        time.sleep(config.diag_sleep)
except KeyboardInterrupt:
    logger.info ("Raspberry Valley MQTT system logger shutdown")
