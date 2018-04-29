$(document).ready(function () {
    alert(233)
    $('.btn.delete').bind('click', function () {
        var father = $(this).parent().parent()
        if (father.css('text-decoration').match('none')) {
            father.css('text-decoration', 'line-through')
        } else {
            father.css('text-decoration', 'none')
        }
    })
    $('#btn_delete_all').bind('click', function () {
        alert(233)
        var ids = []
        $('.btn.delete').each(function () {
            var father = $(this).parent().parent()
            if (father.css('text-decoration').match('line-through')) {
                ids.push(this.id.substring(5))
            }
        })
        // $.get('delete_board', {ids: ids}, function (result) {
        // })
    })
    // $('#btn').bind('click', function () {
    //     var users = []
    //     $('.handle').each(function () {
    //         if(!$(this).parent().css('text-decoration').match('^none')){
    //             users.push($(this).html())
    //         }
    //     })
    //     $.post('{% url del_cf_users', {
    //         'users': users,
    //         "csrfmiddlewaretoken": $("[name='csrfmiddlewaretoken']").val()
    //     }, function (ret) {
    //         window.location.reload()
    //     })
    // })
})