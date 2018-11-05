# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

@auth.requires_login()
def entradaValida(form):
    data = form.vars.Validade
    if data >= hoje:
        form.vars.DataDesativacao = date.fromordinal(data.toordinal()+1)
        #db(db.Produto.id == db.EntradaProdutoEstoque.ID_Produto).update(Quantidade = db.EntradaProdutoEstoque.Quantidade)
    else:
        form.errors.Validade = "Validade tem que ser superior a data de hoje"
@auth.requires_login()
def saidaValida(form):
    verificaP = db((db.EntradaProdutoEstoque.id == form.vars.ID_EntradaProdutoEstoque) & (db.EntradaProdutoEstoque.Quantidade >= form.vars.Quantidade))
    menor = db(db.EntradaProdutoEstoque.Quantidade < form.vars.Quantidade)

    if verificaP:
        verificaP.update(Quantidade = db.EntradaProdutoEstoque.Quantidade - form.vars.Quantidade)
    elif menor:
        form.errors.Quantidade = "Quantidade de saida maior que a quantidade em estoque"

@auth.requires_login()
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


def cadPVer(form):
    pass



@auth.requires_login()
def index():

    db.SaidaProdutoEstoque.ID_EntradaProdutoEstoque.requires = IS_IN_DB(db(db.EntradaProdutoEstoque.Ativo == True), db.EntradaProdutoEstoque,
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
    Tabela2 = db(db.EntradaProdutoEstoque.Ativo == True).select(db.Produto.ProdutoDescricao,db.TipoUnidade.TipoUnidadeDescricao, db.EntradaProdutoEstoque.Lote,
                                                                db.EntradaProdutoEstoque.Validade, db.EntradaProdutoEstoque.Quantidade,
                                                                join=(db.Produto.on(db.EntradaProdutoEstoque.ID_Produto == db.Produto.id),
                                                                db.TipoUnidade.on(db.Produto.ID_TipoUnidade == db.TipoUnidade.id)),
                                                                orderby=db.EntradaProdutoEstoque.Validade,
                                                                limitby=limite,
                                                                orderby_on_limitby = False)

    select = db(db.EntradaProdutoEstoque.Ativo == True).select(db.Produto.ProdutoDescricao,db.TipoUnidade.TipoUnidadeDescricao, db.EntradaProdutoEstoque.Lote,
                                                                db.EntradaProdutoEstoque.Validade, db.EntradaProdutoEstoque.Quantidade,
                                                                join=(db.Produto.on(db.EntradaProdutoEstoque.ID_Produto == db.Produto.id),
                                                                db.TipoUnidade.on(db.Produto.ID_TipoUnidade == db.TipoUnidade.id)),
                                                                orderby=db.EntradaProdutoEstoque.Validade)



    paginas = []
    pagina = 0
    qtdPaginas = int(len(select)/items_per_page)




    while pagina <= qtdPaginas:
        paginas.append(pagina+1)
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

    mail.send(to=['gui.germano.silva@gmail.com'],
          subject='hello',
          message='hi there')

    return dict(tabela=Tabela2, entradaProdutos=EntradaProdutos, saida=SaidaP, paginacao=page, quantidadePagina = items_per_page, paginas=paginas, select=select)


@auth.requires_login()
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

@auth.requires_login()
def relatorio():
    import codecs
    relatorio = SQLFORM.factory(
        Field("dataInicial", type="date", requires=IS_DATE(format=T('%d/%m/%Y'))),
        Field("dataFinal", type="date", requires=IS_DATE(format=T('%d/%m/%Y'))),
    )







    relatG = FORM()
    tabela = ""
    gerar = ""
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
                                     db.EntradaProdutoEstoque.id, db.SaidaProdutoEstoque.ID_EntradaProdutoEstoque,
                                     join=(db.Produto.on(db.EntradaProdutoEstoque.ID_Produto == db.Produto.id),
                                           db.TipoUnidade.on(db.Produto.ID_TipoUnidade == db.TipoUnidade.id),
                                           db.EntradaProdutoEstoque.on(db.SaidaProdutoEstoque.ID_EntradaProdutoEstoque == db.EntradaProdutoEstoque.id)),
                                    orderby=db.EntradaProdutoEstoque.Data | db.SaidaProdutoEstoque.Data)


        '''
        relatG = FORM(relatE+relatS,
                    INPUT(_type="submit"))
        '''



        gerar = FORM(INPUT(_type="submit"))

        if gerar.process().accepted:
            arquivo = open("accepted.csv", "w")
            arquivo.write("accepted")
            arquivo.close()
        elif gerar.errors:
            arquivo = open("errors.csv", "w")
            arquivo.write("errors")
            arquivo.close()
        else:
            arquivo = codecs.open("Relatorio.csv", "w", encoding="utf8")
            arquivo.write("Produto; Lote; Data; Quantidade; Tipo; Movimento\n")
            for produto in tabela:
                arquivo.write(str(produto.Produto.ProdutoDescricao) + ";" + str(produto.EntradaProdutoEstoque.Lote) + ";"+
                              str(produto.EntradaProdutoEstoque.Data.strftime("%d/%m/%Y")) + ";" + str(produto.EntradaProdutoEstoque.Quantidade) +";"+
                              "Entrada;"+str(produto.TipoUnidade.TipoUnidadeDescricao) +"\n")
                arquivo.write(str(produto.Produto.ProdutoDescricao) + ";" + str(produto.EntradaProdutoEstoque.Lote) + ";"+
                              str(produto.SaidaProdutoEstoque.Data.strftime("%d/%m/%Y")) + ";" + str(produto.SaidaProdutoEstoque.Quantidade) +";"+
                              "Saida;"+str(produto.TipoUnidade.TipoUnidadeDescricao)+"\n")
            arquivo.close()

        #produtos = db().select(db.Produto.id, db.Produto.ProdutoDescricao,db.Produto.CustoUnitario)

        '''
        if relatG.process().accepted:
            arquivo = open("teste.csv", "w")
            arquivo.write("erro")
            arquivo.close()
        elif relatG.errors:
            arquivo = open("Erro.csv", "w")
            arquivo.write("testeErro")
            arquivo.close()
        else:
            arquivo = open("Relatorio.xlsx", "w")
            arquivo.write("Produto; Data; Custo; Tipo; Lote; Quantidade\n")
            for produtoEntrada in relatEntrada:
                for produtoSaida in relatSaida:
                    for produto in produtos:
                        if str(produto.id) == str(produtoEntrada.ID_Produto):
                            arquivo.write(str(produto.ProdutoDescricao) + ";" + str(produtoEntrada.Data) + ";"+ str(produto.CustoUnitario) + ";" + "Entrada;" + str(produtoEntrada.Lote) +
                                          ";" + str(produtoEntrada.Quantidade)+"\n")
                            arquivo.write(str(produto.ProdutoDescricao) +";"+ str(produtoSaida.Data) + ";" + ";" +";" +"Saida;" + str(produtoEntrada.Lote) +
                                          ";" + str(produtoSaida.Quantidade)+"\n")
            arquivo.close()
        '''

    elif relatorio.errors:
        response.flash = 'Erro'
    else:
        response.flash = "Preencha todos os campos"

    return dict(relatorio=relatorio, relat=tabela, gerar=gerar)

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
