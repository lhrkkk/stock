#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry
REDIS_SERVER="localhost"
REDIS_PORT=6379
MONGO_SERVER="localhost"
MONGO_PORT=27017

MAIL_SERVER = 'mail.ustc.edu.cn'
MAIL_PORT =  25
MAIL_USE_TLS = False
MAIL_USE_SSL = False
MAIL_USERNAME = 'lhrkkk@mail.ustc.edu.cn'
MAIL_PASSWORD = 'starnada'
DEFAULT_MAIL_SENDER = 'lhr'

# DEBUG False的时候会计算all.
DEBUG=True

# set_name_list=['focus','hold','test','hs300']
set_name_list=['hold']

import pymongo
import os

from stock.common.reflection import get_script_location
config_py_location=get_script_location(__file__)
# config_location=os.path.join(script_location,'config.yaml')



#
#
# CONNECTION_STRING = "mongodb://210.45.66.91"  # replace it with your settings
# CONNECTION = pymongo.MongoClient(CONNECTION_STRING)
#
# '''Leave this as is if you dont have other configuration'''
# DATABASE = CONNECTION.databank
# POSTS_COLLECTION = DATABASE.posts
# APPLICATIONS_COLLECTION = DATABASE.applications
# USERS_COLLECTION = DATABASE.users
# SETTINGS_COLLECTION = DATABASE.settings
# MOLECULES_PATH='databank'
#
# MAIL_SERVER = 'mail.ustc.edu.cn'
# MAIL_PORT =  25
# MAIL_USE_TLS = False
# MAIL_USE_SSL = False
# MAIL_USERNAME = 'lhrkkk@mail.ustc.edu.cn'
# MAIL_PASSWORD = 'starnada'
# DEFAULT_MAIL_SENDER = 'lhr'
#
