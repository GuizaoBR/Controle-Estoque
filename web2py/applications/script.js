// Variavel do Modal/Pop-Up
var modal = document.getElementById('Modal');
// Varial do Botão que ABRE o Modal/Pop-Up
var modalBtn = document.getElementById('modalBtn');
// Varial do Botão que FECHA o Modal/Pop-Up
var fecharBtn = document.getElementsByClassName('fecharBtn')[0];
// Varial do Botão que CANCELAR o cadastro
var cancelarCad = document.getElementById('cancelaCad');

// Pega todos os fomulários existentes na página
var forms = document.getElementsByTagName("form");


// Evento de abertura por click
modalBtn.addEventListener('click', abrirModal);
// Evento de fechamento por click
fecharBtn.addEventListener('click', fecharModal);
// Evento de fechamento por click fora da base do Modal
window.addEventListener('click', foraClick);
// Evento de cancelamento por click
cancelarCad.addEventListener('click', cancelar);

// Função para abrir o Modal
function abrirModal(){
  modal.style.display = 'block';
}

// Função para fechar o Modal
function fecharModal(){
  modal.style.display = 'none';
}

// Função para fechar o Modal se clicar fora
function foraClick(e){
  if(e.target == modal){
    modal.style.display = 'none';
  }
}
// Função para cancelar
function cancelar(){
  modal.style.display = 'none';
}

// Função para da submit em vários formulários só com 1 botão(Não Funciona)
function formSubmit(){
  let pos = 0;
  while(pos < forms.length){
    forms[pos].submit();
    pos++;
  }
}
