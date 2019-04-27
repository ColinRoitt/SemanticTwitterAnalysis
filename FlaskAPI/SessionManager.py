from apscheduler.schedulers.background import BackgroundScheduler


class SessionManager:
    def __init__(self, db, social):
        self.sessions = {}
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        self.dbObj = db
        self.social = social

        res = self.dbObj.getTasks(1)
        # print(res)
        if(len(res) > 0):
            for job in res:
                # self.addAJob(job.name, job.func)
                n = 1
        else:
            print('No tasks in data')

    # POST
    def addAJob(self, name, func, sec):
        self.sessions[name] = self.scheduler.add_job(
            func=func, trigger="interval", seconds=sec)
        print(self.sessions)
        return 'running'

    def getTweets(self, PID, perDay):
        self.social.getTweets(PID)
        return self.addAJob(PID,
                            lambda: self.social.getTweets(PID),
                            round(86400/perDay, 0)
                            )

    def stopProfile(self, PID):
        self.scheduler.remove_job(self.sessions[PID].id)
        self.sessions.pop(PID)
        return 'job removed'

    def isProfileRunning(self, PID):
        profs = self.sessions.keys()
        if PID in profs:
            return True
        else:
            return False
