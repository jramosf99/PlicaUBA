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
		conf["mgmt_path1"] = config["mgmt_path"].get("MGMT_PATH1")
		conf["archive_directory1"] = config["archive_directory"].get("DIRECTORY1")
		conf["mgmt_path2"] = config["mgmt_path"].get("MGMT_PATH2")
		conf["archive_directory2"] = config["archive_directory"].get("DIRECTORY2")

	except KeyError as e:
		print("Error al leer la configuracion: {}".format(e))
		sys.exit(1)
    
	print(">> Path a monitorizar: {}".format(conf["mgmt_path1"] ))
	print(">> Directorio de archivo: {}".format(conf["archive_directory1"]))
	print(">> Path a monitorizar: {}".format(conf["mgmt_path2"] ))
	print(">> Directorio de archivo: {}".format(conf["archive_directory2"]))
	
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


def process_file1(file, archive_dir):
	"""
	Lectura de contenido de un fichero de configuracion y accion asociada
	"""

	errors=False
	origin=str(file).split("'")

	if errors==False:
		try:
			destname = format(origin[0].split("\\")[-1])
			shutil.move(origin[0], archive_dir+"\\"+destname)
		except shutil.Error:
			print("No se pudo mover el archivo a {}".format(archive_dir))

	print("Matando watchdog PLICA")

	print("Lanzando watchdog PLICA")



def process_file2(file, archive_dir):
	"""
	Lectura de contenido de un fichero de configuracion y accion asociada
	"""

	errors=False
	origin=str(file).split("'")

	if errors==False:
		try:
			destname = format(origin[0].split("\\")[-1])
			shutil.move(origin[0], archive_dir+"\\"+destname)
		except shutil.Error:
			print("No se pudo mover el archivo a {}".format(archive_dir))

	print("Matando UBA")
	print("Lanzando UBA")

def process_mgmt_file(initial_snap, conf):
	"""
	Comprueba periodicamente el directorio monitorizado y captura los
	archivos nuevos generados.
	"""

	snapshot1 = DirectorySnapshot(conf["mgmt_path1"], recursive = False)
	snapshot2 = DirectorySnapshot(conf["mgmt_path2"], recursive = False)
	diff1 = DirectorySnapshotDiff(initial_snap, snapshot1)
	diff2 = DirectorySnapshotDiff(initial_snap, snapshot2)
	diff_created1 = diff1.files_created
	diff_created2 = diff2.files_created
	# print(diff_created1)
	if diff_created1:
		print(diff_created1)
		print("Detectados nuevos archivos: {}".format(diff_created1))
	if diff_created2:
		print("Detectados nuevos archivos: {}".format(diff_created2))

	for file_to_process in diff_created1:
		process_file1(file_to_process,conf["archive_directory1"])
	for file_to_process in diff_created2:
		process_file2(file_to_process,conf["archive_directory2"])

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
	if not os.path.exists(conf["archive_directory1"]):
		os.makedirs(conf["archive_directory1"])
	if not os.path.exists(conf["archive_directory2"]):
		os.makedirs(conf["archive_directory2"])

	# Inicializacion del monitorización de directorio
	observer1 = initialize_observer(conf["mgmt_path1"])
	observer2 = initialize_observer(conf["mgmt_path2"])

	# Bucle principal del programa
	try:
		while True:

			# Se genera un snapshot inicial y se procesan y envian los cambios
			initial_snap = EmptyDirectorySnapshot()
			process_mgmt_file(initial_snap, conf)

	except KeyboardInterrupt:
		observer1.stop()
		observer2.stop()

	observer1.join()
	observer2.join()