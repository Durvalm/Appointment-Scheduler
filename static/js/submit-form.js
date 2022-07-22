$(document).on('click', '#submit', function (e) {

    e.preventDefault();
    const date = document.querySelector(".date-picker").value;
    const hour = document.querySelector("#hour-picker").value;
    const barber = document.querySelector("#barber-picker").value;
    const cost = document.querySelector('.cost').textContent.replace('$', "").trim();
    console.log(cost);

    $.ajax({
        type: "POST",
        url: `appointment-submit`,
        data: {
            'cost': cost,
            'hour': hour,
            'date': date,
            'barber': barber,
            'service': serviceId,
            'saloon': saloon,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function (data) {
            window.location.href = "scheduler";
        }
    });
    return false;
});

$(document).on('input', '#barber-picker', function (e) {
    e.preventDefault();

    const date = document.querySelector(".date-picker").value;
    const hour = document.querySelector("#hour-picker").value;
    const barber = document.querySelector("#barber-picker").value;

    $.ajax({
        type: "POST",
        url: `modal/${saloon}/${serviceId}`,
        data: {
            'barber': barber,
            'date': date,
            'hour': hour,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function (data) {
            document.querySelector('.modal-content').innerHTML = data;
            document.querySelector('.date-picker').value = date;
            document.querySelector('#hour-picker').value = hour;
            document.querySelector('#barber-picker').value = barber;
        }
    });
    return false;
});