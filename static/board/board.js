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
    var red = 'red'
    var violet = '#a0a'
    var blue = 'blue'
    var orange = '#FF8C00'
    var cyan = '#03A89E'
    var gray = 'gray'
    var green = 'green'
    var black = 'black'
    var colors = [gray, green, cyan, blue, violet, orange, red]
    var ratings = [1, 1200, 1400, 1600, 1900, 2200, 2400]
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