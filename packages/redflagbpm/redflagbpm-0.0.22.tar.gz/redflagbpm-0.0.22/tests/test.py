import sys
sys.path.append("../src")

# import the necessary components first
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import redflagbpm

bpm=redflagbpm.BPMService()

# Leo los parámetros de configuración del mail en la BPM
env=bpm.service.env()

#Parámetros de conexión
smtp_server=env["BPM_MAIL_HOSTNAME"]
port=env["BPM_MAIL_PORT"]
login=env["BPM_MAIL_USERNAME"]
password=env["BPM_MAIL_PASSWORD"]

#Armo el mensaje.
sender_email = "informes@sycinversiones.com"
receiver_email = "gdressino@redflag.dev"

message = MIMEMultipart("alternative")
message["Subject"] = "multipart test"
message["From"] = sender_email
message["To"] = receiver_email

# write the text/plain part
text = """\
Hi,
Check out the new post on the Mailtrap blog:
SMTP Server for Testing: Cloud-based or Local?
https://blog.mailtrap.io/2018/09/27/cloud-or-local-smtp-server/
Feel free to let us know what content would be useful for you!"""

# write the HTML part
html = """\
<html>
  <body>
    <p>Hi,<br>
       Check out the new post on the Mailtrap blog:</p>
    <p><a href="https://blog.mailtrap.io/2018/09/27/cloud-or-local-smtp-server">SMTP Server for Testing: Cloud-based or Local?</a></p>
    <p> Feel free to <strong>let us</strong> know what content would be useful for you!</p>
  </body>
</html>
"""
# convert both parts to MIMEText objects and add them to the MIMEMultipart message
# Los mensajes de email suelen enviarse tanto en texto plano como en HTML
# Así el visor de mail puede elegir uno u otro según las capacidades de rendering que tenga
# Pero podría enviarse en html solamente... eso evita tener que redactar el mail en dos formatos
# Todos los visores de email modernos soportan html, así que no es tan necesario escribirlo dos veces.
part1 = MIMEText(text, "plain")
part2 = MIMEText(html, "html")
message.attach(part1)
message.attach(part2)


# send your email
with smtplib.SMTP(smtp_server, port) as server:
    server.login(login, password)
    server.sendmail(
        sender_email, receiver_email, message.as_string()
    )
print('Sent')

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
