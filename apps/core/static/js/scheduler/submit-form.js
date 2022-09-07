// Deal with appointment submission in modal
// Send all the data to the backend
$(document).on('click', '#submit', function (e) {
    e.preventDefault();
    const date = document.querySelector(".date-picker").value;
    const hour = document.querySelector("#hour-picker").value;
    const barber = document.querySelector("#barber-picker").value;
    // Cut off '$' from cost and total
    const cost = document.querySelector('.cost').textContent.replace('$', "").trim();
    const total = document.querySelector('.total').textContent.replace('$', "").trim();

        $.ajax({
            type: "POST",
            url: `http://127.0.0.1:8000/handle-payment/`,
            crossDomain: true,
            data: {
                // send data to backend
                'cost': cost,
                'total': total,
                'hour': hour,
                'date': date,
                'barber': barber,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            // If appointment is successfully created, redirect user to the scheduler window
            success: function (data) {
                window.location.href = data.redirect;
            }
        });
        return false;
    }
);

// Posts user data of barber choice
$(document).on('change', '#barber-picker', function (e) {
    e.preventDefault();

    // gets data from input
    const date = document.querySelector(".date-picker").value;
    const hour = document.querySelector("#hour-picker").value;
    const barber = document.querySelector("#barber-picker").value;

    $.ajax({
        type: "POST",
        url: `http://127.0.0.1:8000/handle-barber-input/`,
        data: {
            // send data to the backend
            'barber': barber,
            'date': date,
            'hour': hour,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function (data) {
            // re-create modal
            document.querySelector('.modal-content').innerHTML = data;
            document.querySelector('.date-picker').value = date;
            document.querySelector('#hour-picker').value = hour;
            document.querySelector('#barber-picker').value = barber;
        }
    });
    return false;
});