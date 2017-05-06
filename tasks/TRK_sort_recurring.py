from script import writePidFile, deletePidFile, error, taskme
import csv, os, sys, urllib.request, json

scriptdir = os.path.dirname(os.path.realpath(__file__))
taskid = 1
port = sys.argv[1]
name = 'TRK_sort_recurring'
csvndatas = scriptdir + '/' + name + '.csv'
csvvisitor =  scriptdir + '/' + name + '_visitors.csv'
csvdatas =  scriptdir + '/' + name + '_datas.csv'

writePidFile(scriptdir, name)
taskme(port, 'start', taskid)

taskme(port, 'running', taskid, 'getcsv')
with urllib.request.urlopen("http://localhost:%s/tracker/ndatas.csv" % port) as response, open(csvndatas, 'wb') as out_file:
    data = response.read()
    out_file.write(data)

taskme(port, 'running', taskid, 'readcsv')
visitors = datas = {}
with open(csvndatas, newline='') as csvfile:
    for row in csv.reader(csvfile, delimiter=','):
        try:
            visitors[row[4]][row[1]] = 1
        except KeyError:
            visitors[row[4]] = {}
            visitors[row[4]][row[1]] = 1
            datas[row[4]] = {}

        try:
            datas[row[4]][row[1]][row[2]] = row[3]
        except KeyError:
            datas[row[4]][row[1]] = { row[2]: row[3], 'url': {}, 'title': {}, }
        datas[row[4]][row[1]]['url'][row[7]] = row[5]
        datas[row[4]][row[1]]['title'][row[7]] = row[6]

taskme(port, 'running', taskid, 'writecsv')
with open(csvvisitor, 'w') as outfile:
    json.dump(visitors, outfile)
with open(csvdatas, 'w') as outfile:
    json.dump(datas, outfile)

taskme(port, 'complete', taskid)
deletePidFile(scriptdir, name)