$(document).ready(function(){
    /*$('#precoUni').mask("R$ #00,00", {reverse: true});*/

       $("form").submit(function(){

            var isValid = true;
            $("input").each(function() {

                var element = $(this);
                if (element.val() == "") { isValid = false; }

            }); // each Function

            // Função permite verificar se todos os campos estão preenchidos dentro do each
            if(isValid == false){ alert("Todos os campos devem ser preenchidos."); return false;}

        }); // termina #form_cadastra


});
