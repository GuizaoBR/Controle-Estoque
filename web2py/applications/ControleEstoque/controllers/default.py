# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------
import codecs

from gluon.tools import Mail

mail = Mail()

mail.settings.server = "smtp.gmail.com:587"
mail.settings.sender = 'djangonoreplay@gmail.com'
mail.settings.login = 'djangonoreplay@gmail.com:GuizaoTech'
mail.settings.tls = True

from gluon.contrib.login_methods.email_auth import email_auth
auth.settings.login_methods.append(
    email_auth("smtp.gmail.com:587", "@gmail.com"))


'''
def verificaValidade():
    validade = db(db.Estoque.Ativo == True).select(db.Produto.ProdutoDescricao, db.Estoque.Lote,
                                                   db.Estoque.Validade,
                                                   join=db.Produto.on(db.Estoque.ID_Produto == db.Produto.id))
    proximoAValidade = []
    data = date.fromordinal(hoje.toordinal + 60)
    for produto in validade:
        if produto.Validade <= data:
'''        



@auth.requires_login()
def entradaValida(form):
    validade = form.vars.Validade
    produto = form.vars.ID_Produto
    quantidade = form.vars.Quantidade
    lote = form.vars.Lote

    if validade >= hoje:
        desativar = date.fromordinal(validade.toordinal()+1)
        db.Estoque.insert(ID_Produto=produto, Validade=validade, Quantidade=quantidade, Lote=lote, DataDesativacao=desativar)
        #db(db.Produto.id == db.EntradaProdutoEstoque.ID_Produto).update(Quantidade = db.EntradaProdutoEstoque.Quantidade)
    else:
        form.errors.Validade = "Validade tem que ser superior a data de hoje"
@auth.requires_login()
def saidaValida(form):
    verificaP = db((db.Estoque.id == form.vars.ID_Estoque) & (db.Estoque.Quantidade >= form.vars.Quantidade))
    menor = db(db.Estoque.Quantidade < form.vars.Quantidade)

    if verificaP:
        verificaP.update(Quantidade = db.Estoque.Quantidade - form.vars.Quantidade)
    elif menor:
        form.errors.Quantidade = "Quantidade de saida maior que a quantidade em estoque"

@auth.requires_login()
def kitsVer(form):
    lista = form.vars.ID_Estoque
    produtos = form.vars.QuantidadeProdutos
    tamLista = len(lista) * form.vars.QuantidadeKits
    while tamLista > 0:
        for produto in range(len(lista)):
            verifica = db((db.Estoque.id == lista[produto]) & (db.Estoque.Quantidade >= produtos[produto]))
            if verifica and len(lista)  > 1:
                verifica.update(Quantidade = db.Estoque.Quantidade - produtos[produto])
                tamLista -= 1
            else:
                verifica.update(Quantidade = db.Estoque.Quantidade - produtos)
                tamLista -= 1


def cadPVer(form):
    pass



@auth.requires_login()
def index():

    db.SaidaProdutoEstoque.ID_Estoque.requires = IS_IN_DB(db(db.Estoque.Ativo == True), db.Estoque,
                                                                        lambda r: '%s - %s' % (r.Lote, r.ID_Produto.ProdutoDescricao))


    '''
    export_classes = dict(csv=True, json=False, html=False,
                          tsv=False, xml=False, csv_with_hidden_cols=False,
                          tsv_with_hidden_cols=False)
    '''
    '''
    if not request.vars.page:
        redirect(URL(vars={'page':1}))
    else:
        page = int(request.vars.page)
        start = (page-1)*5
        end = page*5
    '''
    if len(request.args):
        page = int(request.args[0])
    else:
        page = 0

    items_per_page = 5
    limite = (page * items_per_page, (page + 1) * items_per_page + 1)


    #Tabela mostrando os produtos
    Tabela2 = db(db.Estoque.Ativo == True).select(db.Produto.ProdutoDescricao,db.TipoUnidade.TipoUnidadeDescricao, db.Estoque.Lote,
                                                                db.Estoque.Validade, db.Estoque.Quantidade,
                                                                join=(db.Produto.on(db.Estoque.ID_Produto == db.Produto.id),
                                                                db.TipoUnidade.on(db.Produto.ID_TipoUnidade == db.TipoUnidade.id)),
                                                                orderby=db.Estoque.Validade,
                                                                limitby=limite,
                                                                orderby_on_limitby = False)

    select = db(db.Estoque.Ativo == True).select(db.Produto.ProdutoDescricao,db.TipoUnidade.TipoUnidadeDescricao, db.Estoque.Lote,
                                                                db.Estoque.Validade, db.Estoque.Quantidade,
                                                                join=(db.Produto.on(db.Estoque.ID_Produto == db.Produto.id),
                                                                db.TipoUnidade.on(db.Produto.ID_TipoUnidade == db.TipoUnidade.id)),
                                                                orderby=db.Estoque.Validade)



    paginas = []
    pagina = 1
    qtdPaginas = int(len(select)/items_per_page)




    while pagina <= qtdPaginas:
        paginas.append(pagina)
        pagina+=1


    '''
    Tabela = SQLFORM.grid(db.EntradaProdutoEstoque.Ativo==True,
                     sortable=False,details=False,searchable=False,
                     paginate=7, links_in_grid=False, _class="",create=False,csv=False,
                     fields = [db.Produto.ProdutoDescricao,db.EntradaProdutoEstoque.Lote,db.EntradaProdutoEstoque.Validade,
                               db.EntradaProdutoEstoque.Quantidade],
                     left=db.Produto.on(db.EntradaProdutoEstoque.ID_Produto == db.Produto.id),
                     orderby=db.EntradaProdutoEstoque.Validade)
    Tabela.element("table")["_id"] = "TblProduto"
    Tabela.element("th")["_id"] = "DescCamp"
    Tabela.element("td")["_id"] = "DescProd"
    Tabela.element('.web2py_counter', replace=None)
    '''

    #Formulário para dar entrada nos Produtos no estoque
    EntradaProdutos = SQLFORM(db.EntradaProdutoEstoque, buttons=[],
                              fields=["ID_Produto","Lote","Validade", "Quantidade"],
                              labels ={"ID_Produto":"", "Lote":"", "Validade":"", "Quantidade":""},
                              hideerror=True)

    #db.SaidaProdutoEstoque.ID_Kits.show_if = (db.SaidaProdutoEstoque.Eh_Kit == True)
    #db.SaidaProdutoEstoque.ID_EntradaProdutoEstoque.show_if = (db.SaidaProdutoEstoque.Eh_Kit == False)

    SaidaP = SQLFORM(db.SaidaProdutoEstoque,hideerror=True)

    if SaidaP.process(onvalidation=saidaValida,formname='saida').accepted:
        rowQuantidadeMinima = db((SaidaP.vars.ID_Estoque == db.Estoque.id) & (db.Estoque.ID_Produto == db.Produto.id)).select(db.Produto.QuantidadeMinima,
                                                                                                                              db.Produto.ProdutoDescricao)
        rowAviso = db(db.Estoque.id == SaidaP.vars.ID_Estoque).select(db.Estoque.Quantidade)
        for qtd in rowQuantidadeMinima:
            for aviso in rowAviso:
                if qtd.QuantidadeMinima >= aviso.Quantidade:
                    mail.send(to=['gui.germano.silva@gmail.com'],
                          subject='Produto {} está em falta no estoque'.format(qtd.ProdutoDescricao),
                          message='Produto {} precisa ser reposto'.format(qtd.ProdutoDescricao))
        redirect(URL("index"))
        response.flash = "Salvo"
    elif SaidaP.errors:
        response.flash = 'Erro'
    else:
        response.flash = "Preencha todos os campos"


    if EntradaProdutos.process(onvalidation=entradaValida,formname='entrada').accepted:
        redirect(URL('index'))

        response.flash = 'Salvo'
    elif EntradaProdutos.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'




    return dict(tabela=Tabela2, entradaProdutos=EntradaProdutos, saida=SaidaP, paginacao=page, quantidadePagina = items_per_page, paginas=paginas, select=select)


@auth.requires_login()
def cadKits():

    cadKits = SQLFORM(db.Kits,
                   labels ={"ID_Estoque":"", "Nome":"", "QuantidadeKits":"", "QuantidadeProdutos":""},
                   buttons=['submit'])
    if cadKits.process(onvalidation=kitsVer).accepted:
        redirect(URL())
        response.flash = "Salvo"
    elif cadKits.errors:
        response.flash = 'Erro'
    else:
        response.flash = "Preencha todos os campos"

    return dict(cadKits=cadKits)

@auth.requires_login()
def kits():

    Kits = db().select(db.Produto.ProdutoDescricao,db.Estoque.Lote, db.Kits.QuantidadeKits, db.Kits.Nome,
                       join=(db.Produto.on(db.Estoque.ID_Produto == db.Produto.id),
                             db.Estoque.on(db.Kits.ID_Estoque == db.Estoque.id)))

    return dict(tabelaKits=Kits)

@auth.requires_login()
def relatorio():
    relatorio = SQLFORM.factory(
        Field("dataInicial", type="date", requires=IS_DATE(format=T('%d/%m/%Y'))),
        Field("dataFinal", type="date", requires=IS_DATE(format=T('%d/%m/%Y'))),
    )








    relatG = FORM()
    tabela = ""
    gerar = ""
    tabelaEntrada = ""
    tabelaSaida = ""
    '''
    db.SaidaProdutoEstoque.ID_EntradaProdutoEstoque.requires = IS_IN_DB(db, db.EntradaProdutoEstoque,
                                                                        lambda r: '%s - %s' % (r.Lote, r.ID_Produto.ProdutoDescricao))
    '''

    if relatorio.process(formname='form_one').accepted:
        inicio = relatorio.vars.dataInicial
        fim = relatorio.vars.dataFinal



        tabelaSelect = ((db.EntradaProdutoEstoque.Data >= inicio) & (db.EntradaProdutoEstoque.Data <= fim) &
                        (db.SaidaProdutoEstoque.Data >= inicio) & (db.SaidaProdutoEstoque.Data <= fim))

        tabela = db(tabelaSelect).select(db.Produto.ProdutoDescricao, db.EntradaProdutoEstoque.Data, db.EntradaProdutoEstoque.Quantidade,
                                     db.SaidaProdutoEstoque.Quantidade, db.SaidaProdutoEstoque.Data,
                                     db.TipoUnidade.TipoUnidadeDescricao, db.EntradaProdutoEstoque.Lote, db.Produto.id,
                                     db.EntradaProdutoEstoque.id, db.SaidaProdutoEstoque.ID_Estoque,
                                     join=(db.Produto.on(db.EntradaProdutoEstoque.ID_Produto == db.Produto.id),
                                           db.TipoUnidade.on(db.Produto.ID_TipoUnidade == db.TipoUnidade.id),
                                           db.Estoque.on(db.SaidaProdutoEstoque.ID_Estoque == db.EntradaProdutoEstoque.id)),
                                    orderby=db.EntradaProdutoEstoque.Data | db.SaidaProdutoEstoque.Data)

        tabelaSelectEntrada = ((db.EntradaProdutoEstoque.Data >= inicio) & (db.EntradaProdutoEstoque.Data <= fim))
        tabelaSelectSaida = ((db.SaidaProdutoEstoque.Data >= inicio) & (db.SaidaProdutoEstoque.Data <= fim))
        tabelaEntrada = db(tabelaSelectEntrada).select(db.Produto.ProdutoDescricao, db.EntradaProdutoEstoque.Data, db.EntradaProdutoEstoque.Quantidade,
                                     db.TipoUnidade.TipoUnidadeDescricao, db.EntradaProdutoEstoque.Lote, db.Produto.id,
                                     db.EntradaProdutoEstoque.id,
                                     join=(db.Produto.on(db.EntradaProdutoEstoque.ID_Produto == db.Produto.id),
                                           db.TipoUnidade.on(db.Produto.ID_TipoUnidade == db.TipoUnidade.id)),
                                    orderby=db.EntradaProdutoEstoque.Data)
        tabelaSaida = db(tabelaSelectSaida).select(db.Produto.ProdutoDescricao, db.SaidaProdutoEstoque.Quantidade,
                                     db.SaidaProdutoEstoque.Data, db.TipoUnidade.TipoUnidadeDescricao,
                                     db.Estoque.Lote, db.Produto.id, db.Estoque.id, db.SaidaProdutoEstoque.ID_Estoque,
                                     join=(db.Produto.on(db.Estoque.ID_Produto == db.Produto.id),
                                           db.TipoUnidade.on(db.Produto.ID_TipoUnidade == db.TipoUnidade.id),
                                           db.Estoque.on(db.SaidaProdutoEstoque.ID_Estoque == db.Estoque.id)),
                                    orderby=db.SaidaProdutoEstoque.Data)


        '''
        relatG = FORM(relatE+relatS,
                    INPUT(_type="submit"))
        '''



        gerar = FORM(INPUT(_type="submit", _value="Gerar relatorio"))

        if gerar.process().accepted:
            arquivo = open("accepted.csv", "w")
            arquivo.write("accepted")
            arquivo.close()
        elif gerar.errors:
            arquivo = open("errors.csv", "w")
            arquivo.write("errors")
            arquivo.close()
        else:
            arquivo = codecs.open("Relatorio.csv", encoding='utf-8' , mode="w")
            arquivo.write("Produto; Lote; Data; Quantidade; Tipo; Movimento\n")
            for produto in tabelaEntrada:
                arquivo.write(str(produto.Produto.ProdutoDescricao) + ";" + str(produto.EntradaProdutoEstoque.Lote) + ";"+
                              str(produto.EntradaProdutoEstoque.Data.strftime("%d/%m/%Y")) + ";" + str(produto.EntradaProdutoEstoque.Quantidade) +";"+
                              "Entrada;"+str(produto.TipoUnidade.TipoUnidadeDescricao) +"\n")
            for produto in tabelaSaida:
                arquivo.write(str(produto.Produto.ProdutoDescricao) + ";" + str(produto.Estoque.Lote) + ";" +
                              str(produto.SaidaProdutoEstoque.Data.strftime("%d/%m/%Y")) + ";" + str(produto.SaidaProdutoEstoque.Quantidade) +";"+
                              "Saida;"+str(produto.TipoUnidade.TipoUnidadeDescricao)+"\n")


    elif relatorio.errors:
        response.flash = 'Erro'
    else:
        response.flash = "Preencha todos os campos"

    return dict(relatorio=relatorio, tabelaEntrada=tabelaEntrada, tabelaSaida=tabelaSaida, gerar=gerar)

@auth.requires_login()
def cadProdutos():
    cadP=  SQLFORM(db.Produto)


    if cadP.process(onvalidation=cadPVer,formname='cadastro').accepted:
        session.flash = 'record inserted'
        redirect(URL())
    elif cadP.errors:
        response.flash = 'Erro'
    else:
        response.flash = "Preencha todos os campos"

    return(dict(cadP=cadP))


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
