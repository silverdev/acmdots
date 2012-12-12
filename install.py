#! /usr/bin/env python

import argparse
import os
import os.path
import shutil

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

scriptdir = os.path.dirname(os.path.realpath(__file__))
home = os.path.expanduser('~')
contained = os.path.commonprefix([scriptdir, home]) == home

def read_link_abs(path):
	"""Read the absolute path to which the symbolic link points.

	Args:
		path - path to the link
	Returns:
		the target absolute path or the empty string if path isn't a link
	"""
	if not os.path.islink(path):
		return ''

	target = os.path.join(os.path.dirname(path), os.readlink(path))
	return os.path.abspath(target)

def install(file, force=False):
	"""Install a file.

	Args:
		file - the file to install
		force - whether to overwrite existing files
	Returns:
		True if the file was installed, False otherwise
	"""
	src  = os.path.join(scriptdir, file)
	dest = os.path.join(home, links[file])
	path = os.path.dirname(dest)

	# If needed, create the directory this file resides in
	if not os.path.exists(path):
		os.makedirs(path)

	if os.path.exists(dest):
		if force:
			# Remove the destination if it exists
			if os.path.isdir(dest) and not os.path.islink(dest):
				shutil.rmtree(dest)
			else:
				os.remove(dest)
		else:
			# If a link already exists, see if it points to this file
			# to prevent extra warnings caused by previous runs
			if read_link_abs(dest) != src:
				print 'Could not link "{}" to "{}": File exists'.format(src, dest)
			return False

	# Use relative links if the dotfiles are contained in home
	if contained:
		os.chdir(home)
		src  = os.path.relpath(src, path)
		dest = links[file]

	os.symlink(src, dest)
	return True

def install_all(force=False):
	uname = os.uname()[0]
	if os.system('cc answerback.c -o answerback.' + uname) == 0:
		links['answerback.' + uname] = 'bin/answerback.' + uname
	else:
		print 'Could not compile answerback.'

	i = 0; # Keep track of how many links we added
	for file in links:
		if install(file, force):
			i += 1

	print '{:d} link{} created'.format(i, 's' if i != 1 else '')

def main():
	parser = argparse.ArgumentParser(
		formatter_class=argparse.RawDescriptionHelpFormatter,
		description= \
"""Installs symbolic links from dotfile repo into your home directory

Destination directory is "{}".
Source files are in "{}".""".format(home, scriptdir))
	parser.add_argument('-f', '--force', action='store_true',
		help='force to overwrite existing files')
	args = parser.parse_args()

	install_all(args.force)

if __name__ == '__main__':
	main()
