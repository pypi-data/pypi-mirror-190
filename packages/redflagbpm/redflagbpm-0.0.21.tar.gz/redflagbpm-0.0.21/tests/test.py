import sys
sys.path.append("../src")

import redflagbpm

bpm=redflagbpm.BPMService()

# Leo los parámetros de configuración del mail en la BPM
env=bpm.service.env()
mail_host_name=env["BPM_MAIL_HOSTNAME"]
mail_port=env["BPM_MAIL_PORT"]
mail_username=env["BPM_MAIL_USERNAME"]
mail_password=env["BPM_MAIL_PASSWORD"]
mail_ssl=env["BPM_MAIL_SSL"]
mail_starttls=env["BPM_MAIL_STARTTLS"]
mail_login=env["BPM_MAIL_LOGIN"]

# El nombre del servidor smtp
print('mail_host_name =',mail_host_name)
# El puerto que se debe usar
print('mail_port =',mail_port)
# El nombre del usuario
print('mail_username =',mail_username)
# El password
print('mail_password =',mail_password)
# Indica si se debe usar o no SSL (True/False)
print('mail_ssl =',mail_ssl)
# Indica si se debe usar STARTTLS (REQUIRED/OPTIONAL/DISABLED)
print('mail_starttls =',mail_starttls)
# Indica el método de Login (DISABLED, NONE, REQUIRED,XOAUTH2)
print('mail_login =',mail_login)


## Ejemplos de service

#Ejemplo: Notifico a un usuario
#bpm.service.notifyUser("redflag","Hola","Estoy en pyhton3 remoto Liorén!")

#Ejemplo: me traigo código de la BPM
#json_especies=bpm.service.code("GARCPD/ESPECIES_MAV")
#print(json_especies)

#Ejemplo: me traigo parámetros
#token=bpm.service.text("TOKEN_WS")
#print(token)

#Ejemplo: ejecuto un VTL
#vtl=bpm.service.execute("GARCPD/TEMPLATE",{})
#print(vtl)

## Ejemplos de context
#bpm.context.nombre="Liorén"
#
# variables = {'persona.tipoId': 'CUIT',
#              'persona.id': '30-51841045-4',
#              'persona.perfilInversor': 'INDEF/VENCIDO',
#              'max_riesgo': 1000.0,
#              'perfil_inv_actualizado': 'Agresivo',
#              'modificar_perfil': True}
#
# bpm.call_timeout=2
#
# # bpm.service.now()
#
# bpm.runtimeService.startProcessInstanceByKey("CUPERFI", None,
#                                          {'persona.tipoId': 'CUIT',
#                                           'persona.id': '30-51841045-4',
#                                           'persona.perfilInversor': 'INDEF/VENCIDO',
#                                           'max_riesgo': 1000.0,
#                                           'perfil_inv_actualizado': 'Agresivo',
#                                           'modificar_perfil': True})
# #bpm.reply("Hola Liorén")
