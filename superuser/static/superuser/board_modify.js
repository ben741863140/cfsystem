$(document).ready(function () {
    $('.btn.delete').bind('click', function () {
        var father = $(this).parent().parent()
        if (father.css('text-decoration').match('none')) {
            father.css('text-decoration', 'line-through')
        } else {
            father.css('text-decoration', 'none')
        }
    })
    $('#btn_delete_all').bind('click', function () {

        var ids = []
        $('.btn.delete').each(function () {
            var father = $(this).parent().parent()
            if (father.css('text-decoration').match('line-through')) {
                ids.push(this.id.substring(5))
            }
        })
        if(ids.length == 0) return
        var choice = confirm("确定删除所有标记项？")
        if(!choice) return
        $.post('delete_board', {
            csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val(),
            ids: ids
        }, function (result) {
            window.location.reload()
        })
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