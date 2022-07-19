$(document).on('input', '.date-picker', function (e) {
    e.preventDefault();

    date = document.querySelector(".date-picker").value

    $.ajax({
        type: "POST",
        url: `modal/${saloon}/${serviceId}`,
        data: {
            'date': date,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function (data) {
            console.log(data);
            document.querySelector('.modal-content').innerHTML = data;
        }
    });
    return false; //<---- move it here
});
