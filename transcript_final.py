class AudioDownload():
	def __init__(self, link, title = None, path = 'C:\\Users\\isaac\\Desktop\\Audio Files\\'):
		self.link = link
		self.title = title
		self.path = path

		import logging
		LOG_FMT = '%(levelname)s %(asctime)s >>> %(message)s'
		logging.basicConfig(filename = 'C:\\Users\\isaac\\Desktop\\python starter projects\\logs\\youtube\\log_audioDownload.txt'
			, level = logging.DEBUG
			, format = LOG_FMT
			, filemode = 'w')
		self.log = logging.getLogger()

	def download(self): # downloads mp4 from youtube
		from pytube import YouTube, exceptions
		try:
			yt = YouTube(self.link)
		except exceptions.RegexMatchError:
			self.log.error('Bad link')
		else:
			self.log.info(f'Video Title: {yt.title}')
			if self.title == None:
				self.title = yt.title.replace(' ','_')
				self.log.info(f'title not found, title will be "{self.title}"')
			self.title = self.title.replace(' ','_')
			self.log.info(f'formated title :{self.title}')
			stream = yt.streams.first()
			stream.download(output_path = self.path, filename = 'temp') # keeps the filename as temp bc we'll delete this later, see line 30
			self.log.info('Download Complete.')

	def convert(self): # converts mp4 to mp3 and wav
		import subprocess, os

		self.log.info('ffmpeg is converting .mp4 to .wav')
		subprocess.call(['ffmpeg', '-i', f'{self.path}temp.mp4',f'{self.path}{self.title}.wav'])
		if not os.path.exists(f'{self.path}{self.title}.wav'):
			self.log.error(f'ffmeg could not convert temp.mp4 to {self.path}{self.title}.wav')
			self.wavCreated = False
		else:
			self.wavCreated = True
		self.log.info('ffmpeg is converting .mp4 to .mp3')
		subprocess.call(['ffmpeg', '-i', f'{self.path}temp.mp4',f'{self.path}{self.title}.mp3'])
		if not os.path.exists(f'{self.path}{self.title}.mp3'):
			self.log.error(f'ffmeg could not convert temp.mp4 to {self.path}{self.title}.mp3')
			self.mptCreated = False
		else:
			self.mptCreated = True

	def cleanup(self): # cleans up
			import os
			self.log.info(f'moving {self.title}.mp3 to the directory "mp3 files"')
			if self.mptCreated:
				try:
					os.replace(f'{self.path}{self.title}.mp3',f'{self.path}mp3 files\\{self.title}.mp3')
				except:
					self.log.error(f'could not move {self.title}.mp3 to the directory "mp3 files"')
			else:
				self.log.error(f'could not move {self.title}.mp3 to the directory "mp3 files" because ffmpeg could not convert')

			self.log.info(f'deleting temp.mp4')
			try:
				os.remove(f'{self.path}temp.mp4')
			except:
				self.log.error('could not delete temp.mp4')

	def main(self):
		self.download()
		self.convert()
		self.cleanup()
		self.log.info(f'MP3 Downloaded?: {self.mptCreated}')
		self.log.info(f'WAV Downloaded?: {self.wavCreated}')

class VideoDownload(object):
	def __init__(self, link,  path, title = ''):
		import logging
		LOG_FMT = '%(levelname)s %(asctime)s >>> %(message)s'
		logging.basicConfig(filename = 'C:\\Users\\isaac\\Desktop\\python starter projects\\logs\\youtube\\log_videoDownload.txt'
			, level = logging.DEBUG
			, format = LOG_FMT
			, filemode = 'w')
		self.log = logging.getLogger()
		self.link = link
		self.title = title
		self.path = path
	def main(self):
		from pytube import YouTube
		yt = YouTube(url)
		if self.title == None:
			self.title = yt.title
		self.log.info('downloading video from youtube')
		self.log.info(f'Video Title: {yt.title}')
		stream = yt.streams.first()
		stream.download(output_path = self.path, filename = self.title)
		self.log.info('download complete')

class Transcript(object):
	def __init__(self, videoID):
		self.ID = videoID

	def createTranscript(self):
		from youtube_transcript_api import YouTubeTranscriptApi

		transcript_list = YouTubeTranscriptApi.list_transcripts(self.ID)
		first = False
		for item in transcript_list:
			if first == False:
				language = item.language_code
				first = True
			else:
				pass
		try:
			transcript = transcript_list.find_manually_created_transcript([language])
			transcript_type = 'Manually created captions used.'
		except:
			transcript = transcript_list.find_generated_transcript([language])
			transcript_type = 'Generated captions used, no manually created captions found.'

		if language != 'en':
			transcript = transcript.translate('en')

		transcript = transcript.fetch()
		transcript_text = []
		for item in transcript:
			transcript_text.append(item['text'])

		for line in transcript_text:
			print(line)

		print('Quick Info:')
		print(transcript_type)
if __name__ == '__main__':
	choice = input('enter youtube video id')
	test = Transcript(choice)
	test.createTranscript()
	input('Press enter to quit')