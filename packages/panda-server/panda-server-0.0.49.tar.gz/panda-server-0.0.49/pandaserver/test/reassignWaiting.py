import time
import datetime
from pandaserver.taskbuffer.OraDBProxy import DBProxy
import pandaserver.userinterface.Client as Client

# password
from pandaserver.config import panda_config

# time limit
timeLimit = datetime.datetime.utcnow() - datetime.timedelta(hours=1)

# instantiate DB proxies
proxyS = DBProxy()
proxyS.connect(panda_config.dbhost,panda_config.dbpasswd,panda_config.dbuser,panda_config.dbname)

while True:
    # get PandaIDs
    varMap = {}
    varMap[':modificationTime'] = timeLimit
    sql = "SELECT PandaID FROM ATLAS_PANDA.jobsWaiting4 WHERE modificationTime<:modificationTime ORDER BY PandaID"
    status,res = proxyS.querySQLS(sql,varMap)
    
    # escape
    if len(res) == 0:
        break
    # convert to list
    jobs = []
    for id, in res:
        jobs.append(id)
    # reassign
    nJob = 300
    iJob = 0
    while iJob < len(jobs):
        print('reassignJobs(%s)' % jobs[iJob:iJob+nJob])
        Client.reassignJobs(jobs[iJob:iJob+nJob])
        iJob += nJob
        time.sleep(60)
