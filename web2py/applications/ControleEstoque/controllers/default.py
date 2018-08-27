# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------



def entradaValida(form):
    data = form.vars.Validade
    if data >= hoje:
        form.vars.DataDesativacao = date.fromordinal(data.toordinal()+1)
    else:
        form.errors.Validade = "Validade tem que ser superior a data de hoje"

def saidaValida(form):
    verificaP = db((db.EntradaProdutoEstoque.id == form.vars.ID_EntradaProdutoEstoque) & (db.EntradaProdutoEstoque.Quantidade >= form.vars.Quantidade))
    menor = db(db.EntradaProdutoEstoque.Quantidade < form.vars.Quantidade)

    if verificaP:
        verificaP.update(Quantidade = db.EntradaProdutoEstoque.Quantidade - form.vars.Quantidade)
    elif menor:
        form.errors.Quantidade = "Quantidade de saida maior que a quantidade em estoque"

def kitsVer(form):
    lista = form.vars.ID_EntradaProdutoEstoque
    produtos = form.vars.QuantidadeProdutos
    tamLista = len(lista) * form.vars.QuantidadeKits
    while tamLista > 0:
        for produto in range(len(lista)):
            verifica = db((db.EntradaProdutoEstoque.id == lista[produto]) & (db.EntradaProdutoEstoque.Quantidade >= produtos[produto]))
            if verifica and len(lista)  > 1:
                verifica.update(Quantidade = db.EntradaProdutoEstoque.Quantidade - produtos[produto])
                tamLista -= 1
            else:
                verifica.update(Quantidade = db.EntradaProdutoEstoque.Quantidade - produtos)
                tamLista -= 1



def index():

    '''
    export_classes = dict(csv=True, json=False, html=False,
                          tsv=False, xml=False, csv_with_hidden_cols=False,
                          tsv_with_hidden_cols=False)
    '''

    #Tabela mostrando os produtos
    Tabela = SQLFORM.grid(db.EntradaProdutoEstoque.Ativo==True,
                     sortable=False,details=False,searchable=False,
                     paginate=7, links_in_grid=False, _class="",create=False,csv=False,
                     fields = [db.Produto.ProdutoDescricao,db.EntradaProdutoEstoque.Lote,db.EntradaProdutoEstoque.Validade,
                               db.EntradaProdutoEstoque.Quantidade],
                     left=db.Produto.on(db.EntradaProdutoEstoque.ID_Produto == db.Produto.id),
                     orderby=db.EntradaProdutoEstoque.Validade)

    '''
    Tabela = db(db.EntradaProdutoEstoque.Ativo==True).select(db.Produto.ProdutoDescricao, db.EntradaProdutoEstoque.Lote,
                                                             db.EntradaProdutoEstoque.Validade, db.EntradaProdutoEstoque.Quantidade,
                                                             join=db.EntradaProdutoEstoque.on(db.Produto.id == db.EntradaProdutoEstoque.ID_Produto))

    '''


    #Formulário para dar entrada nos Produtos no estoque
    EntradaProdutos = SQLFORM(db.EntradaProdutoEstoque, buttons=[],
                              fields=["ID_Produto","Lote","Validade", "Quantidade"],
                              labels ={"ID_Produto":"", "Lote":"", "Validade":"", "Quantidade":""},
                              hideerror=True)

    #db.SaidaProdutoEstoque.ID_Kits.show_if = (db.SaidaProdutoEstoque.Eh_Kit == True)
    #db.SaidaProdutoEstoque.ID_EntradaProdutoEstoque.show_if = (db.SaidaProdutoEstoque.Eh_Kit == False)

    SaidaP = SQLFORM(db.SaidaProdutoEstoque)

    if SaidaP.process(onvalidation=saidaValida).accepted:
        redirect(URL("index"))
        response.flash = "Salvo"
    elif SaidaP.errors:
        response.flash = 'Erro'
    else:
        response.flash = "Preencha todos os campos"


    if EntradaProdutos.process(onvalidation=entradaValida).accepted:
        redirect(URL('index'))
        response.flash = 'Salvo'
    elif EntradaProdutos.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'

    return dict(tabela=Tabela, entradaProdutos=EntradaProdutos, saida=SaidaP)



def cadKits():

    cadKits = SQLFORM(db.Kits,
                   labels ={"ID_EntradaProdutoEstoque":"", "Nome":"", "QuantidadeKits":"", "QuantidadeProdutos":""},
                   buttons=['submit'])
    if cadKits.process(onvalidation=kitsVer).accepted:
        redirect(URL())
        response.flash = "Salvo"
    elif cadKits.errors:
        response.flash = 'Erro'
    else:
        response.flash = "Preencha todos os campos"

    return dict(cadKits=cadKits)

def kits():
    TabelaKits = SQLFORM.grid(db.Kits,
                     sortable=False,details=False,searchable=False,
                     paginate=7, links_in_grid=False, _class="",create=False,csv=False,
                     fields = [db.Kits.Nome, db.Kits.QuantidadeProdutos, db.Kits.QuantidadeKits])
    return dict(tabelaKits=TabelaKits)






# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})

# ---- Smart Grid (example) -----
@auth.requires_membership('admin') # can only be accessed by members of admin groupd
def grid():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    #grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)

# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu() # add the wiki to the menu
    return auth.wiki()

# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)
