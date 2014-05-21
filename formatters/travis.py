import json
import pprint
pp = pprint.PrettyPrinter(indent=4)

def do_format(request_response):
	request_response = json.loads(request_response.text)

	canopsis_events= []

	for build in request_response:
		new_event = {}
		new_event["commit"] = build["commit"]

		new_event["component"] = build["branch"]
		new_event["resource"] = "travis_" + str(build["id"])

		new_event["branch"] = build["branch"]
		new_event["state"] = build["result"]

		new_event["output"] = build["message"]


		canopsis_events.append(new_event)

	return canopsis_events