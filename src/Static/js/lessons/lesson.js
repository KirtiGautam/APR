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
            if (data.body == "") {
                $('#body').html('<h5 class="m-5 text-center"> No lessons available for this subject.</h5>');
            } else {
                $('#body').html(data.body);
            }
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

function resetForm() {
    $('#FName').val('');
    $('#dataType').val('')
}

function Validate() {
    let chapter = $('#FName').val();
    let dataType = $('#dataType').val()

    if (chapter == '' || dataType == '' || chapter == null || dataType == null) {
        show_alert("Please select Data Type and Name of File", "warning")
        return false;
    }

    if (!isVideo(input.files[0].name) && dataType == 'video') {
        show_alert("Please select valid video file", "warning")
        return false;
    }

    if (!isxls(input.files[0].name) && dataType == 'csv') {
        show_alert("Please select valid csv File", "warning")
        return false;
    }

    if (!ispdf(input.files[0].name) && dataType == 'pdf') {
        show_alert("Please select valid pdf File", "warning")
        return false;
    }
    return true;
}

function getFormData() {
    let data = new FormData();
    data.append("name", $('#FName').val());
    data.append("type", $('#dataType').val());
    data.append('lesson', $('#ChapName').val())
    return data;
}


$(document).ready(function () {

    $('#class').change(function () {
        getlessons();
    });
    $('#dataType').change(function () {
        if ($('#dataType').val() == 'csv') {
            $('.csv').removeClass('d-none');
        } else {
            $('.csv').addClass('d-none');
        }
    });

});
