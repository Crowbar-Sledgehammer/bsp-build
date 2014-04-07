#!/usr/bin/env python3

import os
from pprint import pprint
import subprocess

class bspBuild(object):
	"""docstring for bspBuild"""

	platform = {
		# Non-Windows
		'posix': {
			'steamdir': os.path.expanduser('~/.steam/steam/'),
			'steamcommon': os.path.expanduser('~/.steam/steam/SteamApps/common/'),
			'binary': 'hl2_linux',
			'copy': 'cp',
		},
		# Windows
		'nt': {
			'steamdir': 'C:/Program Files (x86)/Steam/',
			'steamcommon': 'C:/Program Files (x86)/Steam/SteamApps/common/',
			'binary': 'hl2.exe',
			'copy': 'COPY',
		}, 
	}

	game_config = {
		'Team Fortress 2': {
			# 'game_folder': platform[os.name]['steamcommon'] + 'Team Fortress 2/',
			'gamedir': platform[os.name]['steamcommon'] + 'Team Fortress 2/tf/',
			'game': platform[os.name]['steamcommon'] + 'Team Fortress 2/' + platform[os.name]['binary'],
			'bspdir': platform[os.name]['steamcommon'] + 'Team Fortress 2/tf/maps/',
			'buildtools': {
				'posix': {
					'vbsp': os.path.abspath('./lib/Team Fortress 2/bin/vbsp.exe'),
					'vvis': os.path.abspath('./lib/Team Fortress 2/bin/vvis.exe'),
					'vrad': os.path.abspath('./lib/Team Fortress 2/bin/vrad.exe'),
				},
				'nt': {
					'vbsp': platform['nt']['steamcommon'] + 'Team Fortress 2/bin/vbsp.exe',
					'vvis': platform['nt']['steamcommon'] + 'Team Fortress 2/bin/vvis.exe',
					'vrad': platform['nt']['steamcommon'] + 'Team Fortress 2/bin/vrad.exe',
				},
			},
		},
	}

	build_presets = {
		'vbsp': '%(vbsp)s -game %(gamedir)s %(path)s/%(file)s',
		'copy': '%(copy)s %(path)s/%(file)s.bsp %(bspdir)s/%(file)s.bsp',
		'game': '%(game)s -sw -w 1024 -h 768 -dev -console -allowdebug -game %(gamedir)s +map %(file)s',
	}

	build_config = {
		'Default': [
			build_presets['vbsp'],
			'%(vvis)s -game %(gamedir)s %(path)s/%(file)s',
			'%(vrad)s -game %(gamedir)s %(path)s/%(file)s',
			build_presets['copy'],
			build_presets['game'],
		],
		'Fast': [
			build_presets['vbsp'],
			'%(vvis)s -fast -game %(gamedir)s %(path)s/%(file)s',
			'%(vrad)s -bounce 2 -noextra -game %(gamedir)s %(path)s/%(file)s',
			build_presets['copy'],
			build_presets['game'],
		],
		'HDR Full Compile': [
			build_presets['vbsp'],
			'%(vvis)s -both -game %(gamedir)s %(path)s/%(file)s',
			'%(vrad)s -game %(gamedir)s %(path)s/%(file)s',
			build_presets['copy'],
			build_presets['game'],
		],
		'HDR Full Compile -final (slow!)': [
			build_presets['vbsp'],
			'%(vvis)s -both -final -game %(gamedir)s %(path)s/%(file)s',
			'%(vrad)s -game %(gamedir)s %(path)s/%(file)s',
			build_presets['copy'],
			build_presets['game'],
		],
		'Only Entities': [
			'%(vbsp)s -onlyents %(gamedir)s %(path)s/%(file)s',
			build_presets['copy'],
			build_presets['game'],
		],
	}

	def __init__(this, arg):
		super(bspBuild, this).__init__()
		this.arg = arg[1:]
		
		# pprint(this.arg)
		# Iterate over .vmf files
		for vmf_file in [ elem for elem in this.arg if '.vmf' in elem ]:
			this.build_vmf(vmf_file)

	def build_vmf(this, 
		vmf_file, 
		game='Team Fortress 2', 
		shell_out=build_config['Default']
	):
		if not os.path.isfile(vmf_file):
			raise IOError('System could not resolve: ' + vmf_file)
			return 1

		if vmf_file.endswith('.vmf'):
			vmf_file = vmf_file[:-4]

		vmf_path, vmf_file = os.path.split(os.path.abspath(vmf_file))

		# Define variables avaiable in copy script
		build_vars = {
			'vbsp': this.game_config[game]['buildtools'][os.name]['vbsp'],
			'vrad': this.game_config[game]['buildtools'][os.name]['vrad'],
			'vvis': this.game_config[game]['buildtools'][os.name]['vvis'],
			'file': vmf_file,
			'path': vmf_path,
			'copy': this.platform[os.name]['copy'],
			'game': this.game_config[game]['game'],
			'gamedir': this.game_config[game]['gamedir'],
			'bspdir': this.game_config[game]['bspdir'],
		}
		# pprint(build_vars)

		for cmd in shell_out:
			cmd = [li % build_vars for li in cmd.split()]
			print('** Executing...')
			print('** Command: ' + cmd[0])
			print('** Parameters: ' + ' '.join('"' + li + '"' if os.path.exists(os.path.split(li)[0]) else li for li in cmd[1:]))
			print('')
			process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
			stdout, stderr = process.communicate()
			print('')

		#todo compute shaw1 of input & outpul fiels involved http://stackoverflow.com/questions/1869885/calculating-sha1-of-a-file
		

if __name__ == '__main__':
	import sys
	bspBuild(sys.argv)