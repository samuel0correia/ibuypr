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

/* Animação do botão das categorias */
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


/* next... */

