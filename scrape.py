import urllib
from optparse import OptionParser
import os
import requests 
import time
import datetime
import re
import json

parser = OptionParser()
parser.add_option("-o", "--output", dest="filename",
                  help="The folder to store the output", metavar="FILE")
parser.add_option("-f", "--freq",
                  dest="freq", default=True,
                  help="Frequency to scrape at")


(options, args) = parser.parse_args()
print(options)
baseDir   = options.filename
frequency = options.freq



targetList = requests.get('http://dotsignals.org/new-data.php').json()['markers']


for index,a in enumerate(targetList):
    print('grabbing info for',str(index),' of ',len(targetList))
    directory = baseDir+'/'+str(a['id'])
    if not os.path.exists(directory):
        os.makedirs(directory)
    t = requests.get('http://dotsignals.org/google_popup.php?cid='+str(a['id'])).text
    found = re.search('cctv(\d*)\.jpg',t)
    if found:
        targetList[index]['image_id']= found.groups()[0]

with open(baseDir+'/targets.json','w') as f:
    json.dump(targetList,f)

while True:
    dt = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    print('grabbing images at timestamp ', dt)
    for index,a in enumerate(targetList):
        print('Downloaded {no} of {total}'.format(no=index,total=len(targetList)))
        if 'image_id' in a:
            url = 'http://207.251.86.238/cctv{iid}.jpg'.format(iid=a['image_id'])
            savePath = baseDir+'/'+str(a['id'])+'/'+dt+'.jpg'
            urllib.request.urlretrieve(url,savePath)
    time.sleep(int(frequency))
