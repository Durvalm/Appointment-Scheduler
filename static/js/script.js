// function modalData(id) {
//     $.ajax({
//         url: "{% url 'modal' 1 %}".replace("1", id),
//         type: "GET",
//         success(response) {
//             let service = JSON.parse(response)[0].fields;
//             $("#id_service").val(service.service);
//             $("#id_id").val(service.id);
//         },
//     });
// }

document.querySelector('#modal-open').addEventListener('click', function (e) {
    e.preventDefault();
    alert('done');
    console.log('HELLO');
})

