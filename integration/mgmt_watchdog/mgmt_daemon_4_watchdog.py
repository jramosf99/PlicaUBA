#!/usr/bin/env python3

"""
mgmt_daemon PLICA
Version: 0.4.1
Fecha: 2020/09/21
Autores: Mario Sanz Rodrigo
"""

import sys
import time
import logging
import configparser
import json
import shutil
import os

from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.utils.dirsnapshot import DirectorySnapshot
from watchdog.utils.dirsnapshot import DirectorySnapshotDiff

from json.decoder import JSONDecodeError

def read_config(param):
	"""
	Lee la configuracion del archivo pasado por parámetro
	"""

	config = configparser.ConfigParser()
	config.read(param)
	print(">> Configuracion: {}".format(param))
	conf = {}

	try:
		conf["mgmt_path"] = config["mgmt_path"].get("MGMT_PATH")
		conf["archive_directory"] = config["archive_directory"].get("DIRECTORY")

	except KeyError as e:
		print("Error al leer la configuracion: {}".format(e))
		sys.exit(1)

	print(">> Path a monitorizar: {}".format(conf["mgmt_path"] ))
	print(">> Directorio de archivo: {}".format(conf["archive_directory"]))

	return conf

class EmptyDirectorySnapshot(object):
	"""
	Clase que genera un snapshot inicial del directorio
	"""

	def __init__(self):
		self._stat_info = {}
		self._inode_to_path = {}

	@property
	def stat_snapshot(self):
		return {}

	def stat_info(self, path):
		return None

	@property
	def paths(self):
		return set()

	def path(self, id):
		return self._inode_to_path.get(id)


def process_file(file, archive_dir):
	"""
	Lectura de contenido de un fichero de configuracion y accion asociada
	"""

	errors=False
	origin=str(file).split("'")

	if errors==False:
		try:
			destname = format(origin[0].split("/")[-1])
			shutil.move(origin[0], archive_dir+"/"+destname)
		except shutil.Error:
			print("No se pudo mover el archivo a {}".format(archive_dir))

	print("Matando watchdog PLICA")
	os.system("bash /opt/plica/watchdog/src/kill_watchdog.sh")
	print("Lanzando watchdog PLICA")
	os.system("sh /opt/plica/watchdog/src/launch_watchdog.sh")

def process_mgmt_file(initial_snap, conf):
	"""
	Comprueba periodicamente el directorio monitorizado y captura los
	archivos nuevos generados.
	"""

	snapshot = DirectorySnapshot(conf["mgmt_path"], recursive = False)
	diff = DirectorySnapshotDiff(initial_snap, snapshot)
	diff_created = diff.files_created
	if diff_created:
		print("Detectados nuevos archivos: {}".format(diff_created))

	for file_to_process in diff_created:
		process_file(file_to_process,conf["archive_directory"])

def initialize_observer(path):
	"""
	Inicializa el observador para monitorizar el directorio.
	"""
	logging.basicConfig(level=logging.INFO,
							format='%(asctime)s - %(message)s',
							datefmt='%Y-%m-%d %H:%M:%S')

	event_handler = LoggingEventHandler()
	observer = Observer()
	observer.schedule(event_handler, path, recursive=False)
	observer.start()

	return observer

if __name__=="__main__":

	# Carga de la configuración
	conf = read_config(sys.argv[1])

	# Creación del directorio de archivo (si no existe)
	if not os.path.exists(conf["archive_directory"]):
		os.makedirs(conf["archive_directory"])

	# Inicializacion del monitorización de directorio
	observer = initialize_observer(conf["mgmt_path"])

	# Bucle principal del programa
	try:
		while True:

			# Se genera un snapshot inicial y se procesan y envian los cambios
			initial_snap = EmptyDirectorySnapshot()
			process_mgmt_file(initial_snap, conf)

	except KeyboardInterrupt:
		observer.stop()

	observer.join()
