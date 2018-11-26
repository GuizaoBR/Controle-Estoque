from gluon.tools import Mail
mail = Mail()

mail.settings.server = "smtp.gmail.com:587"
mail.settings.sender = 'djangonoreplay@gmail.com'
mail.settings.login = 'djangonoreplay@gmail.com:GuizaoTech'
mail.settings.tls = True


'''
validade = db(db.Estoque.Ativo == True).select(db.Produto.ProdutoDescricao, db.Estoque.Lote,
                                                   db.Estoque.Validade,
                                                   join=db.Produto.on(db.Estoque.ID_Produto == db.Produto.id))
proximoAValidade = []
data = date.fromordinal(hoje.toordinal() + 60)
for produto in validade:
    if produto.Estoque.Validade <= data:
        proximoAValidade.append({"Produto": produto.Produto.ProdutoDescricao, "Lote": produto.Estoque.Lote})
        texto = ""
        for x in proximoAValidade:
            texto += "{} - {}\n".format(x["Produto"], x["Lote"])

        mail.send(to=['gui.germano.silva@gmail.com'],
                  subject='Validade',
                  message="Os seguintes produtos estão próximos da sua data de validade:\n" + texto)
    '''



import time
while True:
    rows = db(db.email.status=='pendente').select()
    for row in rows:
        if mail.send(to=row.email,
            subject=row.assunto,
            message=row.mensagem):
            row.update_record(status='enviado')
        else:
            row.update_record(status='falhado')
        db.commit()
    time.sleep(60) # check every minute
