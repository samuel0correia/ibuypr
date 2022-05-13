/* Animação da sidebar */

$(document).ready(function(){
    $("#menu-btn").click(function(){
        $(".sidebar").css({transform: 'translate(0px, 0px)'});

        $("#overlay").css({opacity: '1'});
        $("#overlay").css({width: '100%'});
        $("#overlay").css({height: '100%'});
    });

    $("#close-sidebar-btn").click(function(){
        $(".sidebar").css({transform: 'translate(-100%, 0px)'});

        $("#overlay").css({opacity: '0'});
        $("#overlay").css({width: '0'});
        $("#overlay").css({height: '0'});
    });
    $("#overlay").click(function(){
        $(".sidebar").css({transform: 'translate(-100%, 0px)'});

        $("#overlay").css({opacity: '0'});
        $("#overlay").css({width: '0'});
        $("#overlay").css({height: '0'});
    });
});

/* Animação do botão das categorias */
$(document).ready(function(){
    $("#category").click(function(){
        if($('#category-symbol').attr("class") === "fa-solid fa-angle-right") {
            $("#category-symbol").attr('class', 'fa-solid fa-angle-down');
        } else {
            $('#category-symbol').attr('class', 'fa-solid fa-angle-right');
        }
    });
});

/* filtro
$(document).ready(function(){

    $('select').on('change', function (e) {
        var optionSelected = $("option:selected", this).val();
        // var valueSelected = this.value;
        $('#title').text(optionSelected);

    });
});

*/

/* next... */

