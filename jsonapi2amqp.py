import json
import os
import imp
import requests

from send_event import send_event

modules_path = os.path.expanduser('./formatters')
formatters = {}


def read_config():
	"""reads connector config, from file config.json"""

	filename = "config.json"

	file_object = open(filename, "r")

	return json.loads(file_object.read())


def import_json_formatters():
	modules = {}

	for module in os.listdir(modules_path):
		print "module:" + str(module)

		if module[0] != '.':
			modname, ext = os.path.splitext(module)

		if ext == '.py':
			print "py file"
			abspath = os.path.join(modules_path, module)
			formatters[modname] = imp.load_source(modname, abspath)

	# for modname in formatters:
	# 	module = modules[modname]
	# 	print "modname:" + modname

def send_request(requestconfig):
	print "got one request to send \n" + str(requestconfig) + "\n" + requestconfig["url"]

	if requestconfig['url'] is None or requestconfig['url'] == "":
		raise Exception("url not set in request" + str(requestconfig))

	r = requests.get(requestconfig.get('url'))

	return r


if __name__ == '__main__':
	config = read_config()
	import_json_formatters()

	for request in config.get('requests', []):
		request_response = send_request(request)

		if request.get("formatter") is not None:
			request_response = formatters[request.get("formatter")].do_format(request_response)


		if isinstance(request_response, (list, tuple)):
			for event in request_response:
				send_event(event)