/* Animação da sidebar */
$(document).ready(function(){
    $("#menu-btn").click(function(){
        $(".sidebar").css({display: 'block'});
        $("#overlay").css({display: 'block'});
    });

    $("#close-sidebar-btn").click(function(){
        $(".sidebar").css({display: 'none'});
        $("#overlay").css({display: 'none'});
    });
    $("#overlay").click(function(){
        $(".sidebar").css({display: 'none'});
        $("#overlay").css({display: 'none'});
    });

});


/* next... */

