//Botão adicionar para botar mais produtos nos kits
var add = document.getElementById("Adicionar");

// Linha criada pelo web2py
var addProduto = document.getElementById("form");
//input criado pelo web2py
var produtos = document.getElementById("Kits_ID_EntradaProdutoEstoque");

//primeiro botão de adicionar
var btAdd = document.getElementById("Adicionar");

btAdd.addEventListener('click', adicionar);

//lista de botões remover
var btsRm = document.getElementsByName("Rm");
//lista de botões de "+"
var btAdd2 = document.getElementsByName("Add");

//função para adicionar inputs
function adicionar(){
  //inputs que serão criados ao apertar o botão de "+"
  var produtoNome = document.createElement('select');
  var produtoQuantidade = document.createElement('input');
  var btAddC = document.createElement('button');
  var btRmC = document.createElement('button');


  addProduto.appendChild(produtoNome);
  produtoNome.className = "form-control produto";
  produtoNome.id="Kits_ID_EntradaProdutoEstoque";
  produtoNome.name = "ID_EntradaProdutoEstoque";
  addProduto.appendChild(produtoQuantidade);
  produtoQuantidade.className = "login form-control integer";
  produtoQuantidade.id = "Kits_QuantidadeProdutos";
  produtoQuantidade.name = "QuantidadeProdutos";
  produtoQuantidade.type = "text";
  produtoQuantidade.placeholder = "Quantidade Produtos";
  addProduto.appendChild(btAddC);
  btAddC.id = "Adicionar";
  btAddC.name = "Add";
  btAddC.type = "button";
  btAddC.className = "add_rm";
  btAddC.innerHTML = "+";
  addProduto.appendChild(btRmC);
  btRmC.id = "Remover";
  btRmC.name = "Rm";
  btRmC.type = "button";
  btRmC.className = "add_rm";
  btRmC.innerHTML = "-";

  for(var x = 0; x <= btAdd2.length; x++){
    for(var y = 0; y <= produtos.options.length; y++){
      var newoption = document.createElement("option");
      newoption.value = produtos.options[y].value;
      newoption.text = produtos.options[y].text;
      produtoNome.add(newoption);
      if(btAdd2[x] == btAdd2[btAdd2.length - 1]){
        btAdd2[x].addEventListener('click', adicionar);
      } else if(btAdd2.length == produtos.options.length){
        btAdd2[x].removeEventListener('click', adicionar);
      } else {
        btAdd2[x].removeEventListener('click', adicionar);
        x++
      }
    }
  }
}
