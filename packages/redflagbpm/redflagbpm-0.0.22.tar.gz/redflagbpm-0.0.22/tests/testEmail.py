import sys

sys.path.append("../src")

import redflagbpm

bpm = redflagbpm.BPMService()

msg = {
    "from": "SyC Inversiones<informes@sycinversiones.com>",
    "to": ["gdressino@redflag.dev"],
    "cc": ["gdressino@redflag.dev"],
    "bcc": ["gdressino@redflag.dev"],
    "subject": "Prueba",
    "message": "<p>Cuerpo del email</p>"}

bpm.service.sendMail(msg)

bpm.reply()