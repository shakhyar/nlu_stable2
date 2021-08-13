import json
import threading
import requests


from client_config import *


class Client:
	def __init__(self):
		self.text = ""
		self.inference_list = []
		self.token = TOKEN
		self.head = HEAD
		pass

	def _ask_input(self, text):
		self.text = text
		try:
			self.raw_data = requests.get(f'{self.head}?token={self.token}&query={self.text}')
			self.data = json.loads(self.raw_data.text)
			self.inference_list = self.data['response']
			return self.inference_list
		except Exception as e:
			print(e)
			return [None, None]

	def _understand_intent(self, inference_list):
		self.inference_list = inference_list
		if self.inference_list[1] == "":
			return None
		else:
			return self.inference_list[1]
