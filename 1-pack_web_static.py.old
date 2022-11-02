#!/usr/bin/python3
"""
Fabric script that generate a .tgz archive
"""
from fabric.api import *


def do_pack():
	"""
	Generate the .tgz archive
	"""
	from datetime import datetime
	import os.path

	today = datetime.now()

	tgz_file_path = 'versions/web_static_{}{}{}{}{}{}.tgz'.format(
		today.year, today.month,
		today.day, today.hour,
		today.minute, today.second
	)

	if not os.path.exists('versions'):
		os.mkdir('versions')

	print('Packing web_static to ' + tgz_file_path)
	res = local('tar  -cvzf {} {}'.format(
		tgz_file_path, 'web_static')
	)

	if res.stderr:
		return None

	file_stats = os.stat(tgz_file_path)

	print('web_static packed: {} -> {}Bytes'.format(
		tgz_file_path, file_stats.st_size))

	if not res.stderr:
		return os.path.realpath(tgz_file_path)
	else:
		return None
