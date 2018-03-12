$(document).ready(function () {
    $.get("get_config", {}, function (ret) {
        $('#hour').attr('value', ret.hour);
        $('#minute').attr('value', ret.minute);
        $('#box_yes').attr('checked', ret.is_open)
        $('#box_no').attr('checked', !ret.is_open)
    });
    $('#box_yes').click(function () {
        var sta = $('#box_no').is(':checked');
        $('#box_no').prop('checked', !sta);
    });
    $('#box_no').click(function () {
        var sta = $('#box_yes').is(':checked');
        $('#box_yes').prop('checked', !sta)
    });
    $(function () {
        $('[data-toggle="tooltip"]').tooltip();
    });
    $('#hour').change(function () {
        if (this.value < 0 || this.value >= 24) {
            $('#hour').tooltip('show');
        } else {
            $('#hour').tooltip('hide');
        }
    });
    $('#minute').change(function () {
        if (this.value < 0 || this.value >= 60) {
            $('#minute').tooltip('show');
        } else {
            $('#minute').tooltip('hide');
        }
    });
    $('#btn').bind('click', (function () {
        var hour = $('#hour').val()
        var minute = $('#minute').val()
        var is_open = $('#box_yes').is(':checked')
        if (0 <= hour && hour < 24 && 0 <= minute && minute < 60) {
            $.get("set_auto_update", {
                'hour': hour,
                'minute': minute,
                'is_open': is_open
            }, function (ret) {
                window.location.href = 'finished'
            });
        }
    }));
});