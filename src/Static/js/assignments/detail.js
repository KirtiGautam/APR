function Validate() {
    let type = $('#dataType').val();
    let Name = $('#FName').val();
    let lesson = $('#lessons').val();
    if (type == '' ||
        Name == '' ||
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
    data.append('assignment', $('#assignid').val());
    data.append('subject', $('#subjects').val());
    data.append('lesson', $('#lessons').val());
    return data;
}

function resetForm() {
    $('#dataType').val('');
    $('#FName').val('');
    $('#lessons').val('');
}

$(document).ready(function () {

    $('#dataType').change(function () {
        if (this.value == 'csv') {
            $('.csv').removeClass('d-none');
        } else {
            $('.csv').addClass('d-none');
        }
    });
});
