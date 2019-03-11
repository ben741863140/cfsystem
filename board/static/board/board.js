$(document).ready(function () {
    $('.rating').each(function () {
        var rating = $(this).html()
        $(this).parent().parent().css('color', getColor(rating))
    })
    $('.oldRating').each(function () {
        var rating = $(this).html()
        $(this).css('color', getColor(rating))
    })
})

function getColor(rating) {
    var red = '#ff0000'
    var orange = '#ff8c00'
    var violet = '#a0a'
    var blue = '#0000ff'
    var cyan = '#03a89e'
    var green = '#008000'
    var gray = '#808080'
    var black = '#000000'
    var colors = [gray, green, cyan, blue, violet, orange, red]
    var ratings = [1, 1200, 1400, 1600, 1900, 2100, 2400]
    var res = black
    for (var i = 0; i < colors.length; i++) {
        if (rating >= ratings[i]) {
            res = colors[i]
        } else {
            break
        }
    }
    return res
}