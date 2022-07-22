$(document).on('input', '.date-picker', function (e) {
    e.preventDefault();
    const date = document.querySelector(".date-picker").value;

    $.ajax({
        type: "POST",
        url: `modal/${saloon}/${serviceId}`,
        data: {
            'date': date,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function (data) {
            document.querySelector('.modal-content').innerHTML = data;
            document.querySelector('.date-picker').value = date
        }
    });
    return false;
});


$(document).on('input', '#hour-picker', function (e) {
    e.preventDefault();
    const date = document.querySelector(".date-picker").value;
    const hour = document.querySelector("#hour-picker").value

    $.ajax({
        type: "POST",
        url: `modal/${saloon}/${serviceId}`,
        data: {
            'hour': hour,
            'date': date,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function (data) {
            document.querySelector('.modal-content').innerHTML = data;
            document.querySelector('.date-picker').value = date
            document.querySelector('#hour-picker').value = hour
        }
    });
    return false;
});


$(document).on('keydown', '#hour-picker', function (e) {
    if (e.key === 'Backspace') {
        document.querySelector('#hour-picker').value = ''
    }
})

$(document).on('keydown', '#barber-picker', function (e) {
    if (e.key === 'Backspace') {
        document.querySelector('#barber-picker').value = ''
    }
})

