import requests

basePath = r"http://192.168.1.135/api/xREOsUlYetInkIHuxDldgzqJYLZySU6xDIaobRsx/lights/1/state"
requests.put(basePath,data='{"on":true,"bri":254,"sat":121,"hue":8597 }')
