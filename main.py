import json
import csv
import requests
from datetime import date, datetime
import time

print("Start:")
print (datetime.now())

urlBusca = 'https://jira.bradesco.com.br:8443/rest/api/2/search?jql=filter='
urlFilter = 'https://jira.bradesco.com.br:8443/rest/api/2/filter/'
urlHiperlink = 'https://jira.bradesco.com.br:8443/issues/?jql=filter='

paramFields = '&fields=key'
paramMax = '&maxResults=0'

headers = {
    'Accept': '*/*',
    'User-Agent': 'request',
}

usuario = 'm232682'
senha = ''

filtroName = ['Vila','Value Stream','Squad','Referência']
print("filtros:")
print (datetime.now())
with open('filtros.json') as json_fileFilter:
    dataFiltro = json.load(json_fileFilter)

    for filtro in dataFiltro['filtros']:
        requestFiltro = requests.get(urlFilter + filtro['id'], headers=headers, auth=(usuario, senha))
        jsonfiltro = json.loads(requestFiltro.text)
        filtroName.append(jsonfiltro['name'])
        filtroName.append("URL: " + jsonfiltro['name'])
    json_fileFilter.close()

print("Consultas:")
print (datetime.now())
with open('censo.json') as json_file:
    data = json.load(json_file)

    with open(r'consolidado.csv', 'w') as f:
        f.truncate()
        writerHeader = csv.writer(f)
        writerHeader.writerow(filtroName)
        for vila in data['vilas']:
            print("Vila: " + vila['name'])
            print (datetime.now())
            for vs in vila['vs']:
                for squad in vs['squads']:
                    rowlist = [vila['name'],vs['name'],squad['name'],squad['isReferencia']]
                    for busca in dataFiltro['filtros']:
                        try:    
                            inicio = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                            time.sleep(0.01)
                            getCount = requests.get(urlBusca+busca['id']+' and '+squad['filtro']+paramFields+paramMax, headers=headers, auth=(usuario, senha))
                            fim = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                        except :
                            print (busca['id'] + "==> ConnectionAbortedError")
                            pass
                        finally:
                            jsonCount = json.loads(getCount.text)
                            rowlist.append(jsonCount['total'])
                            rowlist.append(urlHiperlink+busca['id']+' and '+squad['filtro'])

                    writer = csv.writer(f)
                    writer.writerow(rowlist)
json_file.close()
print (datetime.now())