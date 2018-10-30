# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# AppConfig configuration made easy. Look inside private/appconfig.ini
# Auth is for authenticaiton and access control
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig
from gluon.tools import Auth

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.15.5":
    raise HTTP(500, "Requires web2py 2.15.5 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
configuration = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL(configuration.get('db.uri'),
             pool_size=configuration.get('db.pool_size'),
             migrate_enabled=configuration.get('db.migrate'),
             check_reserved=['all'])
else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = []
if request.is_local and not configuration.get('app.production'):
    response.generic_patterns.append('*')

# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = 'bootstrap4_inline'
response.form_label_separator = ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=configuration.get('host.names'))

# -------------------------------------------------------------------------
# create all tables needed by auth, maybe add a list of extra fields
# -------------------------------------------------------------------------
auth.settings.extra_fields['auth_user'] = []
auth.define_tables(username=False, signature=False)

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else configuration.get('smtp.server')
mail.settings.sender = configuration.get('smtp.sender')
mail.settings.login = configuration.get('smtp.login')
mail.settings.tls = configuration.get('smtp.tls') or False
mail.settings.ssl = configuration.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

# -------------------------------------------------------------------------
# read more at http://dev.w3.org/html5/markup/meta.name.html
# -------------------------------------------------------------------------
response.meta.author = configuration.get('app.author')
response.meta.description = configuration.get('app.description')
response.meta.keywords = configuration.get('app.keywords')
response.meta.generator = configuration.get('app.generator')

# -------------------------------------------------------------------------
# your http://google.com/analytics id
# -------------------------------------------------------------------------
response.google_analytics_id = configuration.get('google.analytics_id')

# -------------------------------------------------------------------------
# maybe use the scheduler
# -------------------------------------------------------------------------
if configuration.get('scheduler.enabled'):
    from gluon.scheduler import Scheduler
    scheduler = Scheduler(db, heartbeat=configure.get('heartbeat'))

# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield='value')
# >>> rows = db(db.mytable.myfield == 'value').select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# after defining tables, uncomment below to enable auditing
# -------------------------------------------------------------------------
# auth.enable_record_versioning(db)

db = DAL("sqlite://storage.sqlite", lazy_tables=False)
auth = Auth(db)
auth.define_tables(username=False, signature=False)

db.define_table('TipoUnidade',
                Field('TipoUnidadeDescricao'),
                format='%(TipoUnidadeDescricao)s'
                )

db.define_table('Produto',
                Field('ID_TipoUnidade', 'reference TipoUnidade', requires=IS_IN_SET(['Unidade', 'Gramas'])),
                Field('CodigoBarras', type='integer'),
                Field('CodigoCacauShow', type='integer'),
                Field('CustoUnitario', type='double'),
                Field('QuantidadeMinima', type='double'),
                Field('ProdutoDescricao', type='string', label='Produto'),
                format='%(ProdutoDescricao)s'
                )

db.define_table('EntradaProdutoEstoque',
                Field('ID_Produto', 'reference Produto'),
                Field('Ativo', type='boolean', default=True),
                Field('Validade', type='date'),
                Field('Data', type='date' ),
                Field('Quantidade', type='double'),
                Field('DataDesativacao',type='date'),
                Field('Lote'),
                format='%(Lote)s' + ' - ' + '%(ID_Produto)s'
                )



db.define_table('Kits',
                Field('Nome'),
                Field('ID_EntradaProdutoEstoque', 'list:reference EntradaProdutoEstoque'),
                Field('QuantidadeProdutos', type='list:integer',label="Quantidade de Produtos"),
                Field('QuantidadeKits', type='integer', label="Quantidade de Kits")
                )

db.define_table('SaidaProdutoEstoque',
                Field('ID_EntradaProdutoEstoque', 'reference EntradaProdutoEstoque'),
                #Field('CustoTotal', type='double'),
                Field('Data', type='date'),
                Field('Quantidade', type='double'),
                )







#Obrigatorios
db.EntradaProdutoEstoque.ID_Produto.requires = IS_NOT_EMPTY(error_message="Selecione um Produto")
db.EntradaProdutoEstoque.Lote.requires = IS_NOT_EMPTY(error_message="Preencha este campo")
db.EntradaProdutoEstoque.Validade.requires = IS_NOT_EMPTY(error_message="Preencha este campo")
db.EntradaProdutoEstoque.Quantidade.requires = IS_NOT_EMPTY(error_message="Preencha este campo")
db.Produto.ID_TipoUnidade.requires = IS_NOT_EMPTY(error_message="Preencha este campo")
db.Produto.CodigoBarras.requires = IS_NOT_EMPTY(error_message="Preencha este campo")
db.Produto.CodigoCacauShow.requires = IS_NOT_EMPTY(error_message="Preencha este campo")
db.Produto.QuantidadeMinima.requires = IS_NOT_EMPTY(error_message="Preencha este campo")
db.Produto.ProdutoDescricao.requires = IS_NOT_EMPTY(error_message="Preencha este campo")
db.SaidaProdutoEstoque.ID_EntradaProdutoEstoque.requires = IS_NOT_EMPTY(error_message="Preencha  este campo")
#db.SaidaProdutoEstoque.CustoUnitario.requires = IS_NOT_EMPTY(error_message="Preencha este campo")
db.SaidaProdutoEstoque.Data.requires = IS_NOT_EMPTY(error_message="Coloque a data no formata dd/mm/aaaa")
db.SaidaProdutoEstoque.Quantidade.requires = IS_NOT_EMPTY(error_message="Preencha este campo")




#db.EntradaProdutoEstoque.DataDesativacao.requires = IS_NOT_EMPTY()

#Não permite entrada de lotes repetidos
db.EntradaProdutoEstoque.Lote.requires = IS_NOT_IN_DB(db, 'EntradaProdutoEstoque.Lote')
db.Produto.ProdutoDescricao.requires = IS_NOT_IN_DB(db, "Produto.ProdutoDescricao")
db.Produto.CodigoBarras.requires = IS_NOT_IN_DB(db, "Produto.CodigoBarras")
db.Produto.CodigoCacauShow.requires = IS_NOT_IN_DB(db, "Produto.CodigoCacauShow")

#Cadastra pelo nome e não pelo id
db.Produto.ID_TipoUnidade.requires = IS_IN_DB(db, db.TipoUnidade, db.TipoUnidade._format)
db.EntradaProdutoEstoque.ID_Produto.requires = IS_IN_DB(db, db.Produto, db.Produto._format)

#db.SaidaProdutoEstoque.ID_Kits.requires = IS_IN_DB(db, db.Kits, db.Kits.Nome)

db.Kits.ID_EntradaProdutoEstoque.requires = IS_IN_DB(db(db.EntradaProdutoEstoque.Ativo == True), db.EntradaProdutoEstoque,
                                                     lambda r: '%s - %s' % (r.Lote, r.ID_Produto.ProdutoDescricao), multiple=True)



#db(db.Produto.id == db.EntradaProdutoEstoque.ID_Produto).update(Quantidade = db.EntradaProdutoEstoque.Quantidade)

#Deixa a data no formato dd/mm/aaaa
db.EntradaProdutoEstoque.Validade.requires = IS_DATE(format=T('%d/%m/%Y'))
db.SaidaProdutoEstoque.Data.requires = IS_DATE(format=T('%d/%m/%Y'))
db.EntradaProdutoEstoque.DataDesativacao.requires = IS_DATE(format=T('%d/%m/%Y'))




#Estilisa os widgets do SQLFORM
db.EntradaProdutoEstoque.ID_Produto.widget = SQLFORM.widgets.autocomplete(request, db.Produto.ProdutoDescricao,id_field=db.Produto.id)

#db.EntradaProdutoEstoque.ID_Produto.widget = SQLFORM.widgets.autocomplete(request, db.Produto.ProdutoDescricao)
db.EntradaProdutoEstoque.Lote.widget = lambda field,value:     SQLFORM.widgets.integer.widget(field,value,_placeholder="Lote",_class="form-control")
db.EntradaProdutoEstoque.Validade.widget = lambda field,value:     SQLFORM.widgets.date.widget(field,value,_placeholder='Validade',_class="form-control date",)
db.EntradaProdutoEstoque.Quantidade.widget = lambda field,value:     SQLFORM.widgets.integer.widget(field,value,_placeholder='Quantidade',_class="form-control")
db.Kits.Nome.widget = lambda field,value:     SQLFORM.widgets.string.widget(field,value,_placeholder='Nome',_class="login nome")
db.Kits.QuantidadeKits.widget = lambda field,value:     SQLFORM.widgets.integer.widget(field,value,_placeholder='Quantidade Kits',_class="login")
db.Kits.ID_EntradaProdutoEstoque.widget = lambda field,value:     SQLFORM.widgets.options.widget(field,value,_class="produto")
db.Kits.QuantidadeProdutos.widget = lambda field,value:     SQLFORM.widgets.integer.widget(field,value,_placeholder='Quantidade Produtos',_class="integer login")
db.SaidaProdutoEstoque.ID_EntradaProdutoEstoque.widget = lambda field,value:     SQLFORM.widgets.options.widget(field,value,_class="form-control")
db.Produto.CustoUnitario.widget = lambda field,value:     SQLFORM.widgets.double.widget(field,value,_class="form-control", _id="precoUni")
db.SaidaProdutoEstoque.Data.widget = lambda field,value:     SQLFORM.widgets.date.widget(field,value, _class="form-control", _type="date")


from datetime import date
hoje = date.today()
db.EntradaProdutoEstoque.Data.default = hoje

#Desativar produstos Vencidos

db((db.EntradaProdutoEstoque.Quantidade == 0) & (db.EntradaProdutoEstoque.Ativo == True)).update(DataDesativacao = hoje)
db((db.EntradaProdutoEstoque.DataDesativacao <= hoje) & (db.EntradaProdutoEstoque.Ativo == True)).update(Ativo = False)
