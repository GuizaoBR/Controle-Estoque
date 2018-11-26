validade = db(db.Estoque.Ativo == True).select(db.Produto.ProdutoDescricao, db.Estoque.Lote,
                                               db.Estoque.Validade,
                                               join=db.Produto.on(db.Estoque.ID_Produto == db.Produto.id))
proximoAValidade = []
data = date.fromordinal(hoje.toordinal() + 60)
for produto in validade:
    if produto.Estoque.Validade <= data:
                #proximoAValidade.append([produto.Produto.ProdutoDescricao, produto.Estoque.Lote])
        proximoAValidade.append({"Produto": produto.Produto.ProdutoDescricao, "Lote": produto.Estoque.Lote})
texto = ""
for x in proximoAValidade:
    texto += "{} - {}\n".format(x["Produto"], x["Lote"])

db.email.insert(status='pending',
    email='gui.germano.silva@gmail.com',
    assunto='Validade',
    mensagem="Os seguintes produtos estão próximos da sua data de validade:\n" + texto)
