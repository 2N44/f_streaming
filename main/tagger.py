import util
from mutagen.id3 import ID3, APIC, COMM, TIT2, TPE1, TPE2, TALB, TDRC, TEXT, TRCK, TCOM, TCON, TPUB, TYER, USLT
from mutagen import File

class Tagger():

	def __init__(self, saved_par: dict, file_path, art_path):

		file_type_name = ['MP3', 'AAC', 'OGG']
		self.file_type = file_type_name[saved_par['format_index']]
		self.monoartist = saved_par['monoartist']
		self.file_path = file_path
		self.art_path = art_path

	def _tag_standard(self, metadata: dict):

		if self.file_type == 'MP3':

			self.tags = ID3(self.file_path)

			#artist
			self.tags.add(TPE1(encoding=3, text=metadata['artist']))

			#album artist
			self.tags.add(TPE2(encoding=3, text=metadata['album artist']))

			#album
			self.tags.add(TALB(encoding=3, text=metadata['album']))

			#track
			self.tags.add(TRCK(encoding=3, text=str(metadata['track'])+'/'+str(metadata['total track'])))

			#composer
			self.tags.add(TCOM(encoding=3, text=metadata['composer']))

			#publisher
			self.tags.add(TPUB(encoding=3, text=metadata['publisher']))

			#genre
			self.tags.add(TCON(encoding=3, text=metadata['genre']))

			#date
			self.tags.add(TDRC(encoding=3, text=metadata['date']))
			self.tags.add(TYER(encoding=3, text=metadata['year']))

			#lyrics
			self.tags.add(USLT(encoding=3, lang=u'eng', desc=u'desc', text=metadata['lyrics']))

			#writer/lyricist
			self.tags.add(TEXT(encoding=3, text=metadata['text writer']))

			#comment
			self.tags.add(COMM(encoding=3, lang=u'eng', desc=u'Genius description annoation', text=metadata['desc']))

			#album art
			if self.art_path is None:

				cover_art = util.img_from_url(metadata['art url'])
				self.tags.add(
					APIC(
						encoding=3,
						mime='image/'+metadata['art url'].split('.')[-1],
						type=3,
						desc=u'Cover',
						data=cover_art.read()
					)
				)

			else:

				with open(self.art_path, 'rb') as cover_art:

					self.tags.add(
						APIC(
							encoding=3,
							mime='image/'+self.art_path.split('.')[-1],
							type=3,
							desc=u'Cover',
							data=cover_art.read()
						)
					)

		elif self.file_type == 'AAC':

			#no convention for tagging, will be added later
			pass

		elif self.file_type == 'OGG':

			#no convention for tagging, will be added later
			pass

	def _tag_title(self, metadata: dict):

		if self.monoartist:

			if self.file_type == 'MP3':

				#title
				self.tags.add(TIT2(encoding=3, text=metadata['title ft']))

			elif self.file_type == 'AAC':

				#not ready
				pass

			else:

				#not ready
				pass

		else:

			if self.file_type == 'MP3':

				#title
				self.tags.add(TIT2(encoding=3, text=metadata['title']))

			elif self.file_type == 'AAC':

				#not ready
				pass

			else:

				#not ready
				pass			

	def tag(self, metadata: dict):

		self._tag_standard(metadata)
		self._tag_title(metadata)

		try:

			self.tags.save()
			print('tagged')

		except:

			#don't tag
			pass


# saved_par={
#     'monoartist': False,
#     'path': '',
#     'token genius': 'Token Genius',
#     'spotify client id': 'Spotify ID',
#     'spotify client secret': 'Spotify Secret',
#     'bitrate_index': 2,
#     'format_index': 0,
# }
# file_path = '14 - Xxxtentacion - I don’t even speak spanish lol.mp3'
# metadata = {
#             'title' :             'ala',
#             'title ft' :          'ala ft.',
#             'album' :             'tu connais',
#             'artist' :          ['luther'],
#             'album artist':       'luther',
#             'track' :              2,
#             'total track' :        3,
#             'date' :              '2022-02-23',
#             'publisher' :       [''],
#             'lyrics' :            'rappeur conscient',
#             'genre' :           'Rap; rap fr',
#             'length' :             3,
#             'language' :          'fr',
#             'composer' :        'le boss; moi',
#             'text writer' :     'luther',
#             'year' :               '2022',
#             'art url' :           'qzedqd',
#             'art_path':			'best_friend.png',
#             'desc':				'de la frappe',
#             'album_path' :      'music',
# }
# file_tag = Tagger(saved_par, file_path)
# file_tag.tag(metadata)