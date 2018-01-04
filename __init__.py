from modules import app, cbpi
from uHEC import http_event_collector 
import threading
import logging
import time
import json


# Create event collector object, default SSL and HTTP Event Collector Port
http_event_collector_key = "HEC KEY HERE"
http_event_collector_host = "SPLUNK SERVER HERE"
SplunkHTTP_event = http_event_collector(http_event_collector_key, http_event_collector_host)


@cbpi.initalizer(order=8045)
def init(cbpi):
	cbpi.app.logger.info("INITIALIZE Splunk HTTP Event Logger PLUGIN")


@cbpi.backgroundtask(key="splunk_send_values", interval=2)
def splunk_send_values(api):
		# Update sensor readings
 		for count, (key, value) in enumerate(cbpi.cache["sensors"].iteritems(), 1):
 			payload = {}
 			payload.update({"index":"httpeventtest"})
			payload.update({"sourcetype":"CBPtest"})
			payload.update({"source":"CBP_Sensor"})
			payload.update({"host":"mysterymachine"})
#			event = {"action":"Splunk HTTP sensor reading update"}
			# Check data type of sensor reading, format if float
 			if type(value.instance.last_value) is float:
 				formatted_reading = '{0:.2f}'.format(value.instance.last_value)
 			else:
 				formatted_reading = value.instance.last_value
 			payload.update({"sensor":count, "reading": formatted_reading})
# 			payload.update({"event":{event}})
			SplunkHTTP_event.sendEvent(payload)
#			#cbpi.app.logger.info(payload)	
