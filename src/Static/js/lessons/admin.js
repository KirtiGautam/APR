function getlessons(id = '') {
    console.log($('#class').val());
    $.ajax({
        type: "POST",
        headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr('content') },
        url: '/get-lessons',
        data: {
            'id': $('#class').val(),
            'subject': id,
        },
        dataType: 'json',
        success: function (data) {
            $('#body').html(data.body);
            let html = '';
            let subjects = data.subjects;
            for (let i = 0; i < subjects.length; i++) {
                html += "<button onclick='getlessons(" + subjects[i].id + ")' ";
                html += (id == subjects[i].id || (id == '' && i == 0)) ? 'style="background-color: #F05E23; color:#FFFFFF;">' : '>'
                html += subjects[i].Name + "</button>  ";
            }
            $('#SB').html(html);
        }
    });
}

$(document).ready(function () {

    $('#class').change(function () {
        getlessons();
    });
});