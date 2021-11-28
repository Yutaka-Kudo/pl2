$('#categorytable td').filter(function () {
    return parseInt($(this).text()) < 0;
}).addClass('minus');