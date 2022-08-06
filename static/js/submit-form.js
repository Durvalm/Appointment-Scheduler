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
    console.log(total);
    console.log('oi');

    // Ask if user confirms the order
    const confirmation = confirm(`Do you confirm the appointment in ${saloon} for $${total}?`)
    if (confirmation) {
        $.ajax({
            type: "POST",
            url: `appointment-submit`,
            data: {
                // send data to backend
                'cost': cost,
                'total': total,
                'hour': hour,
                'date': date,
                'barber': barber,
                'service': serviceId,
                'saloon': saloon,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            // If appointment is successfully created, redirect user to the scheduler window
            success: function (data) {
                window.location.href = `scheduler?location=${saloon}`;
            }
        });
        return false;
    }
});

// Posts user data of barber choice
$(document).on('change', '#barber-picker', function (e) {
    e.preventDefault();

    // gets data from input
    const date = document.querySelector(".date-picker").value;
    const hour = document.querySelector("#hour-picker").value;
    const barber = document.querySelector("#barber-picker").value;

    $.ajax({
        type: "POST",
        url: `modal/${saloon}/${serviceId}`,
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