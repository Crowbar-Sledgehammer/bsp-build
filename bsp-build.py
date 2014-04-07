#!/usr/bin/env python3

import os

class bspBuild(object):
	"""docstring for bspBuild"""

	platform = {
		'posix': {
			'steamdir': '~/.steam/steam/',
			'steamcommon': '~/.steam/steam/SteamApps/common/',
		},
		'nt': {
			'steamdir': 'C:/Program Files (x86)/Steam/',
			'steamcommon': 'C:/Program Files (x86)/Steam/SteamApps/common/',
		}, 
	}

	game_config = {
		'Team Fortress 2': {
			'game_folder': platform[os.name]['steamcommon'] + 'Team Fortress 2/',
			'game_info': platform[os.name]['steamcommon'] + 'Team Fortress 2/tf/',
			'builttools': 
				'posix': {
					'vbsp': 'lib/Team Fortress 2/bin/vbsp.exe',
					'vvis': 'lib/Team Fortress 2/bin/vvis.exe',
					'vrad': 'lib/Team Fortress 2/bin/vrad.exe',
				},
				'nt': {
					'vbsp': platform['nt']['steamcommon'] + 'Team Fortress 2/bin/vbsp.exe',
					'vvis': platform['nt']['steamcommon'] + 'Team Fortress 2/bin/vvis.exe',
					'vrad': platform['nt']['steamcommon'] + 'Team Fortress 2/bin/vrad.exe',
					},
			},
		},
	}

	def __init__(self, arg):
		super(bspBuild, self).__init__()
		self.arg = arg
		
		print('hello world')
		from pprint import pprint
		pprint(self.game_config)

if __name__ == '__main__':
	import sys
	bspBuild(sys.argv)