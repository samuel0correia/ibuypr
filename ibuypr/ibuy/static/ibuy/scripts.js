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

/* Animação de hover num objeto (produtos e utilizadores) */
$(document).ready(function() {
    $(".object-wrap").hover(function () {
        var id = this.id;
        $(".object-wrap").css('border', '4px solid transparent');
        $("#" + id).css('border', '4px solid #3e4157');
    });
    $(".object-wrap").mouseleave(function () {
        $(".object-wrap").css('border', '4px solid transparent');
    });

    $(".object-wrap-profile").hover(function () {
        var id = this.id;
        $(".object-wrap-profile").css('border', '4px solid transparent');
        $("#" + id).css('border', '4px solid #3e4157');
    });
    $(".object-wrap-profile").mouseleave(function () {
        $(".object-wrap-profile").css('border', '4px solid transparent');
    });


});


$(document).ready(function () {
        $('#btncompra').click(function () {
            $('#popupcompra').addClass('open-popup');
        });
        $('#btncancel').click(function () {
            $('#popupcompra').removeClass('open-popup');
        });
        $('#btncancel2').click(function () {
            $('#popupcompra').removeClass('open-popup');
        });
    });

/* next... */

