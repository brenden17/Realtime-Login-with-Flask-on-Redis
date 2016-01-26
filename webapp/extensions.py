from time import time

from redis import Redis

from flask.ext.login import current_user

from flask import g

redis = Redis()
KEEPING_TIME = 30

class LoginStatusSession(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.context_processor(self.context_processor)

    def context_processor(self):
        user = current_user
        user_friends = []
        logined_friends = []
        
        if not user.is_anonymous:
            # remove all users who logined ago KEEPING_TIME sec.
            timestamp = time()
            pipe = redis.pipeline()
            redis.zremrangebyscore('loginstatus', 0, timestamp-KEEPING_TIME)
            # added user
            redis.zadd('loginstatus', user.username, timestamp)
            pipe.execute()
            user_friends = user.get_friends() or []
            if user_friends:
                friends_key = 'friend:{}'.format(user.username)
                pipe.sadd(friends_key, *user_friends)
                # save friends for KEEPING_TIME sec
                pipe.expire(friends_key, KEEPING_TIME)
            
                # get frineds who logined             
                logined_friend_key = 'lfriend:{}'.format(user.username)
                pipe.zinterstore(logined_friend_key, [friends_key, 'loginstatus'])
                pipe.zrange(logined_friend_key, 0,-1, withscores=False)
                logined_friends = pipe.execute()[-1]
        return dict(user=user,
                    user_friends=user_friends,
                    logined_friends=logined_friends)

lss = LoginStatusSession()