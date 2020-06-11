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

import logging

# -- Logging -----------------------------------------------------------------

#: Sets application-wide loglevel
LOG_LEVEL = logging.DEBUG

#: Set logger message format
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# -- MQTT --------------------------------------------------------------------

broker = "localhost"
broker_port = 1883
broker_user = None
broker_pass = None

# MQTT Topics for system properties. The string expects to be formatted ('{0}') 
# with a variable hostname value

cpu_temp_topic = "system/{0}/cputemp"
cpu_usage_topic = "system/{0}/cpuusage"
disk_usage_topic = "system/{0}/diskusage"
mem_usage_topic = "system/{0}/memusage"

# Message topic: this topic sends all cumulative data in JSON format. Used for 
# integrating with web services or event hubs and similar

message_topic = "system/{0}/message"

# Frequency of updates (delay in seconds)

diag_sleep = 20
