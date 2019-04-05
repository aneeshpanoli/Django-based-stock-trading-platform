var append_increment = 0;
setInterval(function() {
    $.ajax({
        type: "GET",
        url: "{% url 'indexView' %}",  // URL to your view that serves new info
        data: {'append_increment': append_increment}
    })
    .done(function(response) {
        $('#stockData').html(response);
        append_increment += 10;
    });
}, 10000)
