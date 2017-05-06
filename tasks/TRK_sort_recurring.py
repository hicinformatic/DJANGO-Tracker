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
with urllib.request.urlopen("http://localhost:%s/tracker/ndatas.csv" % port) as response:
    for row in csv.reader(response.read(), delimiter=','):
        try:
            visitors[row[4]][row[1]] = 1
        except NameError:
            visitors[row[4]] = {}
            visitors[row[4]][row[1]] = 1
            datas[row[4]] = {}
        except KeyError:
            pass

        try:
            datas[row[4]][row[1]][row[2]] = row[3]
        except NameError:
            datas[row[4]][row[1]] = { 'url': {}, 'title': {}, }
            datas[row[4]][row[1]][row[2]] = row[3]
        except KeyError:
            pass
        datas[row[4]][row[1]]['url'][row[7]] = row[5]
        datas[row[4]][row[1]]['title'][row[7]] = row[6]

taskme(port, 'running', taskid, 'writecsv')
with open(csvvisitor, 'w') as outfile:
    json.dump(visitors, outfile)
with open(csvdatas, 'w') as outfile:
    json.dump(datas, outfile)

taskme(port, 'complete', taskid)
deletePidFile(scriptdir, name)