#! /usr/bin/env python

import argparse
import os
import os.path

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

i = 0; # Keep track of how many links we added
for file in links:
	# See if this file resides in a directory, and create it if needed.
	path = os.path.dirname(links[file])
	if path and not os.path.exists(os.path.join(home, path)):
		os.makedirs(os.path.join(home, path))

	src  = os.path.join(scriptdir, file)
	dest = os.path.join(home, links[file])

	if not os.path.exists(dest):
		os.symlink(src, dest)
		i += 1

print '{:d} link{} created'.format(i, 's' if i != 1 else '')
