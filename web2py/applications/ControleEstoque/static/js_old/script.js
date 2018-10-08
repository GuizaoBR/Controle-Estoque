///////////////////////////////////MODAL DE CADASTRO/////////////////////////////////////////////
// Variavel do Modal/Pop-Up
var modal = document.getElementById('Modal');
// Varial do Botão que ABRE o Modal/Pop-Up
var modalBtn = document.getElementById('modalBtn');
// Varial do Botão que FECHA o Modal/Pop-Up
var fecharBtn = document.getElementsByClassName('fecharBtn')[0];
// Varial do Botão que CANCELAR o cadastro
var cancelarCad = document.getElementById('cancelaCad');

//////////////////////////////EVENTOS///////////////////////////////////////

// Evento de abertura por click
modalBtn.addEventListener('click', abrirModal);
// Evento de fechamento por click
fecharBtn.addEventListener('click', fecharModal);
// Evento de fechamento por click fora da base do Modal
window.addEventListener('click', foraClick);
// Evento de cancelamento por click 
cancelarCad.addEventListener('click', cancelar);

///////////////////////////////FUNÇÕES//////////////////////////////////////

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

///////////////////////////////////MODAL DE EXCLUSÃO/////////////////////////////////////////////
//Variavel do Modal de Exclusão
var modal_Ex = document.getElementById('ModalEX');
//Variavel do botão de abertura do Modal de Exclusão
var botao_Ex = document.getElementById('modalBtnEX');
//Variavel do botão de fechamento do Modal de Exclusão
var botaof_Ex = document.getElementsByClassName('fecharBtnEX')[0];
//Variavel do botão de cancelamento do Modal de Exclusão
var cancelar_Ex = document.getElementById('cancelaEX');

// Evento de abertura por click
botao_Ex.addEventListener('click', abrirModalEX);
// Evento de fechamento por click
botaof_Ex.addEventListener('click', fecharModalEX)
// Evento de cancelamento por click
cancelar_Ex.addEventListener('click', cancelarex)
// Evento de fechamento por click fora do campo do modal
window.addEventListener('click', foraClickEx)

// Função para abrir o Modal e esconder os botões 
function abrirModalEX(){
  modal_Ex.style.display = 'block'; 
}

// Função para fechar o Modal e mostrar os botões novamente
function fecharModalEX(){
  modal_Ex.style.display = 'none';  
}

// Função para fechar o Modal se clicar fora e mostrar os botões novamente
function cancelarex(){
  modal_Ex.style.display = 'none'; 
}

// Função para cancelar e mostrar os botões novamente
function foraClickEx(i){
  if(i.target == modal_Ex){
    modal_Ex.style.display = 'none';
  }
}