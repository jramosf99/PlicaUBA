# PlicaUBA

Sensor UBA del proyecto PLICA

## Instrucciones de instalación y configuración

_Estas instrucciones te permitirán obtener una copia del proyecto en funcionamiento en tu máquina local para propósitos de desarrollo y pruebas._


### Pre-requisitos 📋

_Se debe contar con python3 instalado en el equipo y con la libreria pip_


### Instalación 🔧

_Con la ejecución del paquete deb debería valer para tener el proyecto listo para usarse_

_El paquete se instalará mediante le siguiente comando_

```
sudo dpkg --install UBA-PLICA.deb 
```

## Configuración ⚙️

_Para configurar el sistema se usan los siguientes archivos_

### UBA.cfg

_Este se encuentra en la dirección /opt/plica/uba/src_

### watchdogX.cfg

_Estos se encuentran en la dirección /opt/plica/watcdog/src/_

Cada uno configura un sistema watchdog distinto. En ellos se configura la información relativa al servidor Kafka y se indica las carpetas a vigilar (estas deben ir acorde a las configuradas en UBA.cfg).

### mgmt_daemon_4_watchdog.cfg

_Este se encuentra en la dirección /home/plica/mgmt_

Se configurará los path de los archivos de configuración, donde se reciben y donde se usan.

## Puesta en marcha

_Se pondrá en marcha con el siguiente comando_

```
python3 /home/plica/mgmt/start_all.py
```


