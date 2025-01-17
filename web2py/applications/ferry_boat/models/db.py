# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []

## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
## (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Service, PluginManager

auth = Auth(db)
service = Service()
plugins = PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.janrain_account import use_janrain
use_janrain(auth, filename='private/janrain.key')

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)

db.define_table('my_image',
    Field('name', requires=[IS_NOT_EMPTY(),IS_NOT_IN_DB(db, 'my_image.name')]),
    Field('docker_name', requires=IS_NOT_EMPTY()),
    Field('default_tag', requires=IS_NOT_EMPTY()),
    Field('icon','upload', autodelete=True),
    Field('glyphicon'),
    Field('random_port', 'boolean', default=True),
    Field('command', default=''),
    )

db.define_table('volumes',
    Field('image', 'reference my_image', requires=IS_IN_DB(db(db.my_image.id>0), 'my_image.id', '%(docker_name)s')),
    Field('host_path', requires=IS_PATH()),
    Field('container_path', requires=IS_PATH()),
    Field('rw', 'boolean', default=True),
    )

db.define_table('ports',
    Field('image', 'reference my_image', requires=IS_IN_DB(db(db.my_image.id>0), 'my_image.id', '%(docker_name)s')),
    Field('host_port', requires=IS_INT_IN_RANGE(1, 65535, error_message='invalid port')),
    Field('container_port', requires=IS_INT_IN_RANGE(1, 65535, error_message='invalid port')),
    )
