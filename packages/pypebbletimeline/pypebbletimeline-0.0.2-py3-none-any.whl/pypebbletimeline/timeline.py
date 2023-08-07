import requests

class Timeline():
	def __init__(self, token) -> None:
		self.token = token
	def pushPin(self, title, body, subtitle, time):
		# valid times are:
		# 1 - Instant
		# 2 - In 30 min. (Timeline Subscription)
		# 3 - In 60 min. 
		# 4. - In 3 hours (Free)
		pin = {
		"time":f"{time}",
		"layout":{
			"type": "genericPin",
			"title": f"{title}",
			"body": f"{body}",
			"subtitle": f"{subtitle}",
			"tinyIcon": "system://images/NOTIFICATION_GENERIC"}
			,"token": self.token
		}
		r = requests.post('https://willow.systems/pinproxy-ifttt/', data=pin)
		if r.status_code == 200:
			return 200
		else:
			return f"{r.status_code} {r.body}"
