#======================================================================
#
# Python Module to send Raspberry Pi system diagnostics to MQTT 
#
# Created by Raspberry Valley
#
# This code is in the public domain and may be freely copied and used
# No warranty is provided or implied
#
#======================================================================

# MQTT broker setup

broker = "localhost"
broker_port = 1883
broker_user = None
broker_pass = None

# MQTT Topics for system properties. The string expects to be formatted ('{0}') with a variable hostname value
cpu_temp_topic = "system/{0}/cputemp"
cpu_usage_topic = "system/{0}/cpuusage"
disk_usage_topic = "system/{0}/diskusage"
mem_usage_topic = "system/{0}/memusage"

# Frequency of updates (delay in seconds)

diag_sleep = 5