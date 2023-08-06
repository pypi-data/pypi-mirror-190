#Falso dict
class MyFakeDict:
    def __getitem__(self, key):
        return 'culo'

#Real dict
class MyDict(dict):
    def test(self):
        return 'culo';


print("------------- dict REAL --------------")
midict={"hola":"que tal"}
print(midict)
print("tipo: ",type(midict))
print("es dict?: ",isinstance(midict, dict))

print("------------- dict heredado ----------")
miotrodict=MyDict()
miotrodict['hola']='que tal'
print(miotrodict)
print("tipo: ",type(miotrodict))
print("es dict?: ",isinstance(miotrodict, dict))
print(miotrodict.test())

print("------------- dict FALSO ----------")
mifalsodict=MyFakeDict()
print(mifalsodict)
print("tipo: ",type(mifalsodict))
print("es dict?: ",isinstance(mifalsodict, dict))
mifalsodict['hola']='que tal'

# !python3

import redflagbpm
import pandas as pd
import numpy as np
import json
import pycurl
from io import BytesIO
import urllib.parse
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from pandas.io.formats.excel import ExcelFormatter

bpm = redflagbpm.BPMService()


def _call_endpoint_subastas():
    TOKEN = bpm.context["values.text('TOKEN_WS')"]

    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, 'https://ws.sycinversiones.com/mavCPDSubastas?estado=Concertadas')
    c.setopt(pycurl.HTTPHEADER, ["accept: application/json", "Authorization: Bearer " + TOKEN])
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    response = c.getinfo(pycurl.RESPONSE_CODE)
    c.close()

    if response != 200:
        raise Exception('WS no disponible o WS vacío')

    body = buffer.getvalue()
    parsed_b = json.loads(body.decode('iso-8859-1'))

    for d in parsed_b:
        d.update({'subasta': int(d['subasta'])})
    return parsed_b


subastas = _call_endpoint_subastas()
subastas = [s for s in subastas if s['moneda'] == '$' and s['tipo'] != 'PAGARE']

for i, row in enumerate(subastas):
    if row['segmento'] != 'Avalado':
        if "No Garantizado" in row['segmento']:
            row['segmento'] = 'Directo NO Grantizado'
            row['sgr'] = "Directo NO Garantizado " + (" PYME" if row['pyme'] == 'SI' else " NO PYME")
        else:
            row['segmento'] = 'Directo Grantizado'
            row['sgr'] = "Directo Garantizado " + (" PYME" if row['pyme'] == 'SI' else " NO PYME")
    else:
        row['sgr'] = row['sgrLibradorDesc']

if len(subastas) != 0:
    df = pd.DataFrame.from_records(subastas)
    df['ppv'] = df['ppv'].astype(int)
    # print('DATAFRAME\n')
    df['plazo'] = (np.trunc(df['ppv'] / 30) + 1) * 30
    df['plazo'] = df['plazo'].astype(int)

    dftasas = df.pivot_table(index=['segmento', 'sgr'], columns=['plazo'], values=['ofertaVenta'],
                             aggfunc=lambda rows: np.average(rows, weights=df.loc[rows.index, 'monto']))
    dfmonto = df.pivot_table(index=['segmento', 'sgr'], columns=[], values=['monto'], aggfunc=sum)
    dfpivot = dftasas.merge(dfmonto, on=['sgr'])

    dfpivot = dfpivot.rename(columns=lambda x: x[1] if isinstance(x[1], int) else "Monto")
    dfpivot = dfpivot.rename_axis("SGR/Segmento", axis=0)

    # dfpivot=dfpivot.rename_axis(None, axis=0).rename(columns={"ofV":"Valores promedio cada 30 días"})
    # print(dfpivot.to_html(float_format = '{:,.2f}'.format,justify="right",na_rep="-",border=1,))

    book = load_workbook('INFORME_TASAS_MAV_TEMPLATE.xlsx')
    writer = pd.ExcelWriter('/tmp/tasas.xlsx', engine='openpyxl')
    writer.book = book

    row_start = 7
    col_start = 0

    formatter = ExcelFormatter(dfpivot)
    writer.sheets["Hoja1"] = book["Hoja1"]
    writer.write_cells(
        formatter.get_formatted_cells(),
        float_format="%.1f",
        sheet_name="Hoja1",
        startrow=row_start,
        startcol=col_start)

    writer.save()

    # dfpivot.to_excel("/tmp/tasas.xlsx")

    ##Preparo la salida del endpoint
    _responseHeaders = bpm.context.json._responseHeaders
    _responseHeaders["status"] = "200"  # Indico status 200 (OK)
    _responseHeaders[
        "Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"  # Indico el tipo de archivo
    _responseHeaders["Content-Encoding"] = "UTF-8"  # Indico el encoding
    _responseHeaders["Content-Disposition"] = "attachment; filename=tasas.xlsx"  # Indico el encoding
    # Indico que la respuesta será un recurso que guardé. Si omito esto la salida es
    # lo que imprima por consola
    _responseHeaders["resource"] = "/tmp/tasas.xlsx"
else:
    print(u"<html><body>No hay subastas en MAV.</body></html>")
    _responseHeaders = bpm.context.json._responseHeaders
    _responseHeaders["status"] = "200"  # Indico status 200 (OK)
    _responseHeaders["Content-Type"] = "text/html"  # Indico el tipo de archivo
    _responseHeaders["Content-Encoding"] = "UTF-8"  # Indico el encoding
    # Indico que la respuesta será un recurso que guardé. Si omito esto la salida es
    # lo que imprima por consola
