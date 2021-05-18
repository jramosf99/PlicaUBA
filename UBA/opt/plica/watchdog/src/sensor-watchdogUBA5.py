#!/usr/bin/env python3

"""
Watchdog PLICA
Version: 0.4.1
Fecha: 2020/09/21
Autores: Xavier Larriva, Diego Rivera.
Co-autores: Pedro Cabrera, Raul Siles.
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

from confluent_kafka import Producer

from json.decoder import JSONDecodeError


def read_config(param):
	"""
	Lee la configuracion del archivo pasado por parámetro
	"""

	config = configparser.ConfigParser()
	config.read(param)
	print(">> Configuracion: {}".format(param))
	conf = {}

	# 4 modos de oepracion, a 10s, 30s, 5m o 10m
	op_times = [10,30,300,900]
	try:
		conf["operation_time"] = op_times[config["operation_mode"].getint("MODE")-1]
		conf["kafka_topic"] = config["kafka_topic"].get("KK_TOPIC")
		conf["kafka_server"] = config["kafka_server"].get("KK_SERVER")
		conf["json_path"] = config["json_path"].get("JSON_PATH")
		conf["archive_directory"] = config["archive_directory"].get("DIRECTORY")
		conf["debug_directory"] = config["debug_directory"].get("DIRECTORY")

	except KeyError as e:
		print("Error al leer la configuracion: {}".format(e))
		sys.exit(1)

	print(">> Path a monitorizar: {}".format(conf["json_path"] ))
	print(">> Topic Kafka: {}".format(conf["kafka_topic"]))
	print(">> Servidor Kafka: {}".format(conf["kafka_server"]))
	print(">> Tiempo de operacion: {}".format(conf["operation_time"]))
	print(">> Directorio de archivo: {}".format(conf["archive_directory"]))
	print(">> Directorio de depuracion: {}".format(conf["debug_directory"]))

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

def send_data(data, kafka_topic, producer):
	"""
	Envío de un elemento de datos a través de kafka.
	"""
	errors = False
	try:
		print(" Enviando mensaje ")

		producer.produce(kafka_topic,
						 key="msg",
						 value=json.dumps(data))
		producer.flush()

	except IOError as e:
		errors=True
		print('error - IO')

	except ValueError:
		errors=True
		print('error - conversion')

	except:
		errors=True
		print("Unexpected error:", sys.exc_info()[0])
		raise

	return errors

def kafka_send(kafka_topic, kafka_server, file, archive_dir, debug_dir):
	"""
	Lectura de contenido de un fichero y envio a través de kafka.
	"""

	errors=False
	origin=str(file).split("'")

	if type(kafka_topic) == bytes:
		kafka_topic = kafka_topic.decode('utf-8')

	producer = Producer({'bootstrap.servers': kafka_server})

	with open(file) as json_file:

		# Se lee el fichero:
		try:
			data_to_send = json.loads(json_file.read())

		except JSONDecodeError as e:
			errors=True
			print(" Error de parseo en JSON")
			data_to_send = ''
			shutil.move(origin[0],debug_dir)


		# Archivos de tipo lista de JSON, se envía cada elemento por separado.
		if isinstance(data_to_send, list):
			for item in data_to_send:
				if data_to_send != '':
					errors = send_data(item, kafka_topic, producer)

		# Archivos de tipo JSON, se separan sus estructuras "data" y se envian
		# por separado, cada una con sus metadatos.
		else:
			if data_to_send != '':
				if isinstance(data_to_send["data"], list):
					for data_item in data_to_send["data"]:
						print(data_item)
						errors = send_data(data_item, kafka_topic, producer)
	if errors==False:
		try:
			destname = "{}-{}".format(str(time.time()), origin[0].split("\\")[-1])
			shutil.move(origin[0], archive_dir+"\\"+destname)
		except shutil.Error:
			print("No se pudo mover el archivo a {}".format(archive_dir))

def process_and_send(initial_snap, conf):
	"""
	Comprueba periodicamente el directorio monitorizado y captura los
	archivos nuevos generados.
	"""
	time.sleep(conf["operation_time"])
	snapshot = DirectorySnapshot(conf["json_path"], recursive = False)
	diff = DirectorySnapshotDiff(initial_snap, snapshot)
	diff_created = diff.files_created
	if diff_created:
		print("Detectados nuevos archivos: {}".format(diff_created))

	for file_to_send in diff_created:
		kafka_send(conf["kafka_topic"], conf["kafka_server"], file_to_send, conf["archive_directory"], conf["debug_directory"])

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
	observer = initialize_observer(conf["json_path"])

	# Bucle principal del programa
	try:
		while True:

			# Se genera un snapshot inicial y se procesan y envian los cambios
			initial_snap = EmptyDirectorySnapshot()
			process_and_send(initial_snap, conf)

	except KeyboardInterrupt:
		observer.stop()

	observer.join()
