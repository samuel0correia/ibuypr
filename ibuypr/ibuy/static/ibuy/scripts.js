/* Animação da sidebar */
$(document).ready(function(){
    $("#menu-btn").click(function(){
        $("#menu").css({
            width: '250px'
        });
        $(".sidebar").css({
            marginLeft: '250px'
        });
    });
});

$(document).ready(function(){
    $("#close-menu-btn").click(function(){
        $("#menu").css({
            width: '0px'
        });
        $(".sidebar").css({
            marginLeft: '0px'
        });
    });
});

/* next... */

