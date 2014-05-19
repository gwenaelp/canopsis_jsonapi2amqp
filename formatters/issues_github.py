import json
import pprint
pp = pprint.PrettyPrinter(indent=4)

def do_format(request_response):
	request_response = json.loads(request_response.text)

	canopsis_events= []

	for issue in request_response:
		new_event = {}
		new_event["output"] = issue["title"]

		new_event["component"] = "issues"
		new_event["resource"] = "github" + str(issue["id"])

		if issue["state"] == "open":
			new_event["state"] = 0
		else:
			new_event["state"] = 2

		canopsis_events.append(new_event)

	return canopsis_events