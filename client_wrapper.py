import json
import multiprocessing

from client import Client
from client_config import *
from taskmanager import TaskManager


from VoiceAssistant.wakeword.engine import Listener, WakeWordEngine, DemoAction
from VoiceAssistant.speechrecognition.engine import Listener, SpeechRecognitionEngine, DemoAction
#from VoiceAssistant.speechsynthesis.engine import TTS

# no idea about them, seems a bit complicated to me, just need a ww and sr object
# something like this:
ww = WakeWordEngine()
sr = SpeechRecognitionEngine()
tts = None # TTS class will go here instead of None


loop_not_finished = True


def loop_speech(iter_list):
	for i in iter_list:
		tts.say(i)
	loop_not_finished = False



class Wrapper(TaskManager, Client):
	def __init__(self):
		super().__init__(self)

	def start_module(self):

		while True:
			pred = ww.start_wakeword_loop() # start prediction

			if pred == 1: # if true, continue, else continue looping

	# speech recognition class returns None if nothing is recognized, so if recognized, continue..
				print('Listening...')
				self.query = sr.run_speech_recognition() # listen

				if self.query:
					self.infered_list = self._ask_input(text=self.query)
					self.intent = self._understand_intent(inference_list=self.infered_list)
					
					if not self.intent: # if no intent associated, self.intent is assigned as None
						tts.say(self.infered_list[0]) # used if the user just want to chat
					
					else:
						if '--weather' == self.intent:
							weather_description, current_temperature, current_humidity = self.weather()
							if 'humid' in self.infered_list[0] or 'sweat' in self.infered_list[0]:
								tts.say(current_humidity)

							elif 'weather' in self.infered_list[0] or 'cloud' in self.infered_list[0] or 'rain' in self.infered_list[0] or 'windy' in self.infered_list[0] or 'sunnny' in self.infered_list[0]:
								tts.say(weather_description + " " + current_temperature)

							elif 'temperature' in self.infered_list[0]:
								tts.say(current_temperature)


						elif '--news' == self.intent:
							tts.say('How many headlines do you want')
							headlines_in_words = sr.run_speech_recognition() # replace this with real speech recognition function
							news_list = self.news(headlines=headlines_in_words)
							news_loop = multiprocessing.Process(target=loop_speech, args=(news_list))
							news_loop.start()

							while loop_not_finished:
								interrupt_command = sr.run_speech_recognition()
								if "stop" in interrupt_command:
									news_loop.terminate()


						elif '--note' == self.intent:
							tts.say('What should I write?')
							self.note = sr.run_speech_recognition()
							self.take_note(self.note)
							tts.say('Noted')

						
						elif '--info' == self.intent:
							if 'who' in inference_list[0]:
								gr = inference_list[0][inference_list[0].index('who')+4:]
							elif 'whom' in inference_list[0]:
								gr = inference_list[0][inference_list[0].index('whom')+4:]
							elif 'what' in inference_list[0]:
								gr = inference_list[0][inference_list[0].index('what')+4:]
							elif 'which' in inference_list[0]:
								gr = inference_list[0][inference_list[0].index('which')+4:]
							elif 'how' in inference_list[0]:
								gr = inference_list[0][inference_list[0].index('how')+4:]
							elif 'where' in inference_list[0]:
								gr = inference_list[0][inference_list[0].index('where')+4:]

							
							try:
								g_output = self.google(gr)
								if not g_output:
									tts.say(self.wiki(gr))
								else:
									tts.say(g_output)
							except Exception as e:
								print(e)
								tts.say(e)

						elif '--youtube' == self.intent:
							link = self.parse_youtube_query(self.infered_list[0])
							self.player = multiprocessing.Process(target=self.play, args=(link))
							self.player.start()
							interrupt_command = ""

							while self.event:
								interrupt_command = sr.run_speech_recognition()
								if 'stop' in interrupt_command:
									self.player.terminate()

						
						elif '--joke' == self.intent:
							tts.say(self.joke())

						
						elif '--unsure' == self.intent:
							tts.say(self.infered_list[0])

