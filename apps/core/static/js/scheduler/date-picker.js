// Posts user data of date
$(document).on('change', '.date-picker', function (e) {
    e.preventDefault();
    const date = document.querySelector(".date-picker").value;

    $.ajax({
        type: "POST",
        url: `http://127.0.0.1:8000/handle-date-input/`,
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
    const hour = convertTime12to24(document.querySelector("#hour-picker").value)

    $.ajax({
        type: "POST",
        url: `http://127.0.0.1:8000/handle-hour-input/`,
        data: {
            'hour': hour,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function (data) {
            // Re-create modal with dynamic data
            document.querySelector('.modal-content').innerHTML = data;
            document.querySelector('.date-picker').value = date
            document.querySelector('.hour-picker').value = hour
        }
    });
    return false;
});

// Fixes bug in datalist whenuser tries to delete a character
// It deletes the entire input when user clicks on backspace
const deleteInput = function (e, id) {
    if (e.key === 'Backspace') {
        document.querySelector(id).value = ''
    }
}
$(document).on('keydown', '#hour-picker', function (e) {
    deleteInput(e, '#hour-picker')
})
$(document).on('keydown', '#barber-picker', function (e) {
    deleteInput(e, '#barber-picker')
})

// Transforms 12h time into 24h format
const convertTime12to24 = (time12h) => {
    const [time, modifier] = time12h.split(' ');
  
    let [hours, minutes] = time.split(':');
  
    if (hours === '12') {
      hours = '00';
    }
  
    if (modifier === 'PM') {
      hours = parseInt(hours, 10) + 12;
    }
  
    return `${hours}:${minutes}`;
  }