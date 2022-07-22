// Posts user data of date
$(document).on('change', '.date-picker', function (e) {
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
            // Re-create modal with dynamic data
            document.querySelector('.modal-content').innerHTML = data;
            document.querySelector('.date-picker').value = date
        }
    });
    return false;
});

// Posts user data of time
$(document).on('change', '#hour-picker', function (e) {
    e.preventDefault();
    // Get values from inputs
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
            // Re-create modal with dynamic data
            document.querySelector('.modal-content').innerHTML = data;
            document.querySelector('.date-picker').value = date
            document.querySelector('#hour-picker').value = hour
        }
    });
    return false;
});

// Fixes bug in datalist whenuser tries to delete a character
// It deletes the entire input when user clicks on backspace
const deleteInput = function (id) {
    if (e.key === 'Backspace') {
        document.querySelector(id).value = ''
    }
}
$(document).on('keydown', '#hour-picker', function (e) {
    deleteInput('#hour-picker')
})
$(document).on('keydown', '#barber-picker', function (e) {
    deleteInput('#barber-picker')
})

