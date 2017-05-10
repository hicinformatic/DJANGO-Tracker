from script import writePidFile, deletePidFile, error, taskme
import csv, os, sys, urllib.request, json

scriptdir = os.path.dirname(os.path.realpath(__file__))
taskid = 1
port = sys.argv[1]
name = 'TRK_sort_recurring'
csvndatas = scriptdir + '/' + name + '.csv'
listidJSON =  scriptdir + '/' + name + '_listid.json'
datasJSON =  scriptdir + '/' + name + '_datas.json'

writePidFile(scriptdir, name)
taskme(port, 'start', taskid)

taskme(port, 'running', taskid, 'getcsv')
with urllib.request.urlopen("http://localhost:%s/tracker/ndatas.csv" % port) as response, open(csvndatas, 'wb') as out_file:
    data = response.read()
    out_file.write(data)

taskme(port, 'running', taskid, 'readcsv')
listid = []
datas = {}
with open(csvndatas, newline='') as csvfile:
    for row in csv.reader(csvfile, delimiter=','):
        listid.append(row[0])
        try:
            if row[2] == 'User-Agent':
                datas[row[1]]['User-Agent'] = { row[7]: row[3] }
            elif row[2] == 'AcceptLanguage':
                datas[row[1]]['AcceptLanguage'] = { row[7]: row[3] }
            else:
                datas[row[1]]['datas'][row[7]] = { row[2]: row[3] }
            datas[row[1]]['route'][row[7]] = { 'title': row[6], 'url': row[5], }
        except Exception:
            if row[2] == 'User-Agent':
                datas[row[1]] = { 'domain': row[4], 'User-Agent': { row[7]: row[3] }, 'AcceptLanguage': {}, 'datas': {}, 'route': { row[7]: { 'title': row[6], 'url': row[5] } } , }
            elif row[2] == 'AcceptLanguage':
                datas[row[1]] = { 'domain': row[4], 'User-Agent': {}, 'AcceptLanguage': { row[7]: row[3] }, 'datas': {}, 'route': { row[7]: { 'title': row[6], 'url': row[5] } } , }
            else:
                datas[row[1]] = { 'domain': row[4], 'User-Agent': {}, 'AcceptLanguage': {}, 'datas': { row[7]: { row[2]: row[3] } }, 'routes': { row[7]: { 'title': row[6], 'url': row[5] } }     , }

taskme(port, 'running', taskid, 'writejson')
with open(listidJSON, 'w') as outfile:
    json.dump(listid, outfile, indent=4)
with open(datasJSON, 'w') as outfile:
    json.dump(datas, outfile, indent=4)

taskme(port, 'running', taskid, 'addjson')

taskme(port, 'complete', taskid)
deletePidFile(scriptdir, name)