$(document).ready(function () {
    $('.element').bind('click', function () {
        if ($(this).css('text-decoration').match('^none')) {
            $(this).css('text-decoration', 'line-through')
        } else {
            $(this).css('text-decoration', 'none')
        }
    })
    $('#btn').bind('click', function () {
        var users = []
        $('.handle').each(function () {
            if(!$(this).parent().css('text-decoration').match('^none')){
                users.push($(this).html())
            }
        })
        $.post('{% url del_cf_users', {
            'users': users,
            "csrfmiddlewaretoken": $("[name='csrfmiddlewaretoken']").val()
        }, function (ret) {
            window.location.reload()
        })
    })
})