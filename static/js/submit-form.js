$(document).on('click', '#submit', function (e) {

    e.preventDefault();
    date = document.querySelector(".date-picker").value;
    hour = document.querySelector("#hour-picker").value
    barber = document.querySelector("#barber-picker").value


    $.ajax({
        type: "POST",
        url: `appointment-submit`,
        data: {
            'hour': hour,
            'date': date,
            'barber': barber,
            'service': serviceId,
            'saloon': saloon,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function (data) {
            console.log(data);
            window.location.href = "home";
        }
    });
    return false;
});