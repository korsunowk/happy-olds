$(document).ready(function(){
    $('.day').click(function(){
        var count = $(this).find('.olds-count').text().split(' ')[0];

        if (count > 0) {
            $(this).find('.olds-block').toggleClass('open');
        }
    });
});
