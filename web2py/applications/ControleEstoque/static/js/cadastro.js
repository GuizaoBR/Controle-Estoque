//var btLimpar = document.getElementById("EnviaCad");



//btLlimpar.addEventListener('click', limpar);


/*
function limpar(){
  unmasked = $("#precoUni").maskMoney('unmasked')[0]
  $("#precoUni").val(unmasked);
}*/
$(document).on("click", "#EnviaCad", function() {
  unmasked = $("#precoUni").maskMoney('unmasked')[0]
  $("#precoUni").val(unmasked);

});

$(document).ready(function(){
    /*$('#precoUni').mask("R$ #00,00", {reverse: true});*/
    $("#precoUni").maskMoney({
         prefix: "R$",
         decimal: ",",
         thousands: ".",
         affixesStay: true
       })

});
