#!/usr/bin/env python

import time
from kombu import Connection
from kombu.pools import producers

# Configurations
host = "127.0.0.1"
port = 5672
user = "guest"
password = "guest"
vhost = "canopsis"
exchange = "canopsis.events"


def send_event(event):
	event_base = {
		"timestamp":        int(time.time()),
		"connector":        "cli",
		"connector_name":   "MyWebAPP",
		"event_type":       "check",
		"source_type":      "resource",
		"component":        "NOM_de_la_machine",
		"resource":     "NOM_du_JOB",
		"state":        0,
		"state_type":       1,
		"output":       "MESSAGE",
		"display_name":     "DISPLAY_NAME"
	}

	event = dict(event_base.items() + event.items())

	print "prepare to send event:"
	print str(event)

	routing_key = "%s.%s.%s.%s.%s" % (event['connector'], event['connector_name'], event['event_type'], event['source_type'], event['component'])

	if event['source_type'] == "resource":
		routing_key += ".%s" % event['resource']

	# Connection
	with Connection(hostname=host, userid=user, virtual_host=vhost) as conn:
		# Get one producer
		with producers[conn].acquire(block=True) as producer:
			# Publish
			producer.publish(
				event,
				serializer='json',
				exchange=exchange,
				routing_key=routing_key)
