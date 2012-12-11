#! /usr/bin/env python

import argparse
import os
import os.path
import shutil

scriptdir = os.path.dirname(os.path.realpath(__file__))
home = os.path.expanduser('~')

parser = argparse.ArgumentParser(
	formatter_class=argparse.RawDescriptionHelpFormatter,
	description= \
"""Installs symbolic links from dotfile repo into your home directory

Destination directory is "{}".
Source files are in "{}".""".format(home, scriptdir))
parser.add_argument('-f', '--force', action='store_true',
	help='force an overwrite existing files')
args = parser.parse_args()
force = args.force

links = {
	'screenrc':   '.screenrc',
	'ackrc':      '.ackrc',
	'toprc':      '.toprc',
	'dir_colors': '.dir_colors',
	'lessfilter': '.lessfilter',

	'vim':      '.vim',
	'vimrc':    '.vimrc',
	'_vimrc':   '_vimrc',
	'gvimrc':   '.gvimrc',

	'emacsrc':  '.emacs',
	'emacs':    '.emacsdir',

	'commonsh': '.commonsh',

	'inputrc':  '.inputrc',

	'bash':         '.bash',
	'bashrc':       '.bashrc',
	'bash_profile': '.bash_profile',

	'zsh':      '.zsh',
	'zshrc':    '.zshrc',

	'ksh':      '.ksh',
	'kshrc':    '.kshrc',
	'mkshrc':   '.mkshrc',

	'shinit':   '.shinit',

	'Xdefaults':  '.Xdefaults',
	'Xresources': '.Xresources',

	'uncrustify.cfg': '.uncrustify.cfg',
	'indent.pro':     '.indent.pro',

	'xmobarrc':  '.xmobarrc',
	'xmonad.hs': '.xmonad/xmonad.hs',

	'Wombat.xccolortheme':  'Library/Application Support/Xcode/Color Themes/Wombat.xccolortheme',
#	'Wombat.dvtcolortheme': 'Library/Developer/Xcode/UserData/FontAndColorThemes/Wombat.dvtcolortheme',

	'gitconfig': '.gitconfig',
	'gitignore': '.gitignore',

	'tigrc':     '.tigrc',

	'caffeinate': 'bin/caffeinate',
	'lock':       'bin/lock',

	'git-info':            'bin/git-info',
	'git-untrack-ignored': 'bin/git-untracked-ignored',

	'gdbinit': '.gdbinit',
}

uname = os.uname()[0]
if os.system('cc answerback.c -o answerback.' + uname) == 0:
	links['answerback.' + uname] = 'bin/answerback.' + uname
else:
	print 'Could not compile answerback.'

i = 0; # Keep track of how many links we added
for file in links:
	# See if this file resides in a directory, and create it if needed.
	path = os.path.dirname(links[file])
	if path and not os.path.exists(os.path.join(home, path)):
		os.makedirs(os.path.join(home, path))

	src  = os.path.join(scriptdir, file)
	dest = os.path.join(home, links[file])

	# If a link already exists, see if it points to this file. If so, skip it.
	# This prevents extra warnings caused by previous runs of install.py.
	if not force and os.path.islink(dest):
		dest_link = os.path.join(home, path, os.readlink(dest))
		if os.path.abspath(dest_link) == src:
			continue

	# Remove the destination if it exists and we were told to force an overwrite
	if force and os.path.isdir(dest) and not os.path.islink(dest):
		shutil.rmtree(dest)
	elif force:
		os.remove(dest)

	if not os.path.exists(dest):
		os.symlink(src, dest)
		i += 1
	else:
		print 'Could not link "{}" to "{}": File exists'.format(src, dest)

print '{:d} link{} created'.format(i, 's' if i != 1 else '')
