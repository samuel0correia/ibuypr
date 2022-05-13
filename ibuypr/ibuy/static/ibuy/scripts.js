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
        $("#overlay").css( {height: '0'});
    });

    $("#overlay").click(function(){
        $(".sidebar").css({transform: 'translate(-100%, 0px)'});
        $("#overlay").css({opacity: '0'});
        $("#overlay").css({width: '0'});
        $("#overlay").css( {height: '0'});
    });
});

/* Animação e funcionamento do botão das categorias */
$(document).ready(function(){
    $("#category").click(function(){
        if($('#category-symbol').attr("class") === "fa-solid fa-angle-right") {
            $("#category-symbol").attr('class', 'fa-solid fa-angle-down');
            $('.sidebar-dropdown-container').css('display', 'block');
        } else {
            $('#category-symbol').attr('class', 'fa-solid fa-angle-right');
            $('.sidebar-dropdown-container').css('display', 'none');
        }
    });

    $('a.sidebar-dropdown-option').click(function() {
        var option = $(this).text();
        if(option === "Tudo")
            $('#categoria option[value="Tudo"]').attr("selected", "selected");
        else if(option === "Roupa")
            $('#categoria option[value="Roupa"]').attr("selected", "selected");
        else if(option === "Livros")
            $('#categoria option[value="Livros"]').attr("selected", "selected");
        else if(option === "Escrita")
            $('#categoria option[value="Escrita"]').attr("selected", "selected");
        else if(option === "Casa")
            $('#categoria option[value="Casa"]').attr("selected", "selected");
        else if(option === "Outros")
            $('#categoria option[value="Outros"]').attr("selected", "selected");
        $('#filter-form').submit();
    });
});

/* Animação do produto no index */
$(document).ready(function() {
    $(".index-product-wrap").hover(function () {
        var id = this.id;
        $(".index-product-wrap").css('border', '4px solid transparent');
        $("#" + id).css('border', '4px solid #3e4157');
    });
    $(".index-product-wrap").mouseleave(function () {
        $(".index-product-wrap").css('border', '4px solid transparent');
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

