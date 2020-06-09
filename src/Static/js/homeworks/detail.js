function Validate() {
    let type = $('#dataType').val();
    let Name = $('#FName').val();
    let subject = $('#subjects').val();
    let lesson = $('#lessons').val();
    if (type == '' ||
        Name == '' ||
        subject == null ||
        subject == '' ||
        lesson == null ||
        lesson == '' ||
        type == null ||
        Name == null) {
        show_alert('Please fill all the details', "warning");
        return false;
    }
    if (!isVideo(input.files[0].name) && dataType == 'video') {
        show_alert("Please select valid video file", "warning");
        return false;
    }

    if (!isxls(input.files[0].name) && dataType == 'csv') {
        show_alert("Please select valid csv File", "warning");
        return false;
    }

    if (!ispdf(input.files[0].name) && dataType == 'pdf') {
        show_alert("Please select valid pdf File", "warning");
        return false;
    }
    return true;
}


function getFormData() {
    let data = new FormData();
    data.append('type', $('#dataType').val());
    data.append('Name', $('#FName').val());
    data.append('homework', $('#homeworkid').val());
    data.append('subject', $('#subjects').val());
    data.append('lesson', $('#lessons').val());
    return data;
}

function resetForm() {
    $('#dataType').val('');
    $('#FName').val('');
    $('#subjects').val('');
    $('#lessons').val('');
}


function getLessons() {
    $.ajax({
        type: "POST",
        headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr('content') },
        url: '/get-lesson',
        data: {
            'id': $('#subjects').val(),
        },
        dataType: 'json',
        success: function (data) {
            html = '<option value="" selected disabled>Lessons</option>';
            for (x in data.lessons) {
                html += `<option value="${data.lessons[x].id}" >${data.lessons[x].Name}</option>`
                $('#lessons').html(html);
            }
        }
    });
}


$(document).ready(function () {
    $('#subjects').change(function () {
        getLessons();
    });

    $('#dataType').change(function () {
        if (this.value == 'csv') {
            $('.csv').removeClass('d-none');
        } else {
            $('.csv').addClass('d-none');
        }
    });

});
