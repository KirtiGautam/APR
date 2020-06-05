function getlessons(id = '') {
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
                html += "<span onclick='getlessons(" + subjects[i].id + ")' class='subject col-1 p-2 m-1";
                html += (id == subjects[i].id || (id == '' && i == 0)) ? " active'>" : "'>";
                html += subjects[i].Name + "</span>  ";
            }
            $('#SB').html(html);
        }
    });
}

function setChapName(id) {
    $('#ChapName').val(id);
}

$(document).ready(function () {

    $('#class').change(function () {
        getlessons();
    });
});
