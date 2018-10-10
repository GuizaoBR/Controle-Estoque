// Get modal element
var modal = document.getElementById('simpleModal');
// Get open modal button
var modalBtn = document.getElementById('Btn-Estoque');
// Get close button
var closeBtn = document.getElementsByClassName('closeBtn')[0];



// Listen for open click
modalBtn.addEventListener('click', openModal);
// Listen for close click
closeBtn.addEventListener('click', closeModal);
// Listen for outside click
window.addEventListener('click', outsideClick);

// Function to open modal
function openModal(){
  modal.style.display = 'block';
}

// Function to close modal
function closeModal(){
  modal.style.display = 'none';
}

// Function to close modal if outside click
function outsideClick(e){
  if(e.target == modal){
    modal.style.display = 'none';
  }
}


/*
                      Modal Ex
*/

// Get modal element
var modalEx = document.getElementById('simpleModal-eX');
// Get open modal button
var modalBtnEx = document.getElementById('Btn_EstoqueEX');
// Get close button
var closeBtnEx = document.getElementsByClassName('closeBtnEx')[0];


// Listen for open click
modalBtnEx.addEventListener('click', openModalII);
// Listen for open click
closeBtnEx.addEventListener('click', closeModalII);
// Listen for outside click
window.addEventListener('click', outsideClickII);

// Function to open modal
function openModalII(){
  modalEx.style.display = 'block';
}
// Function to open modal
function closeModalII(){
  modalEx.style.display = 'none';
  modalEx.style.cursor = 'pointer';
}

// Function to close modal if outside click
function outsideClickII(i){
  if(i.target == modalEx){
    modalEx.style.display = 'none';
  }
}
