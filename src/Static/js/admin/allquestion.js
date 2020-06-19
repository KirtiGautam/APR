$(document).ready(function () {
    $('.AQL').addClass('active');
    $('.AQT').addClass('stw');
    $('.AQI').addClass('siw');

    $('#class').change(function () {
        $.ajax({
            type: "POST",
            headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr('content') },
            url: '/get-subjects',
            data: {
                'id': this.value,
            },
            dataType: 'json',
            success: function (data) {
                let html = '<option value="" selected disabled>Subjects</option>';
                for (x in data.subjects) {
                    html += `<option value="${data.subjects[x].id}" >${data.subjects[x].Name}</option>`
                }
                $('#subject').html(html);
            }, error: function (error) {
                alert(error.responseText);
            }
        });
    })

    $('#subject').change(function () {
        $.ajax({
            type: "POST",
            headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr('content') },
            url: '/get-lesson',
            data: {
                'id': this.value,
            },
            dataType: 'json',
            success: function (data) {
                html = '<option value="" selected disabled>Lessons</option>';
                for (x in data.lessons) {
                    html += `<option value="${data.lessons[x].id}" >${data.lessons[x].Name}</option>`
                    $('#lesson').html(html);
                }
            }, error: function (error) {
                alert(error.responseText);
            }
        });
    })

    $('#upload_btn').click(function () {
        if ($('#file').get(0).files.length === 0) {
            alert("No files selected.");
            return;
        }
        let file = document.getElementById("file").files[0];
        var selectedFile = file;
        var reader = new FileReader();
        reader.onload = (function (file) {
            return function (event) {
                var dat = event.target.result;
                var workbook = XLSX.read(dat, {
                    type: 'binary'
                });
                let json_data;
                workbook.SheetNames.forEach(function (sheetName) {

                    var XL_row_object = XLSX.utils.sheet_to_row_object_array(workbook.Sheets[sheetName]);
                    var json_object = JSON.stringify(XL_row_object);
                    console.log(json_object);
                    json_data = json_object;
                })
                $.ajax({
                    type: "POST",
                    headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr('content') },
                    url: '/upload-questions',
                    data: {
                        'file': json_data,
                        'lesson': $('#lesson').val(),
                    },
                    dataType: 'json',
                    success: function (data) {
                        console.log(data)
                        $('#file').val('');
                        alert(data.message)
                    }
                });
            };
        })(file);

        reader.onerror = function (event) {
            console.error("File could not be read! Code " + event.target.error.code);
        };

        reader.readAsBinaryString(selectedFile);
    })

})

const check = () => {
    if (!$('#class').val()) {
        alert('Please Select class');
        return false;
    }
    if (!$('#subject').val()) {
        alert('Please Select subject');
        return false;
    }
    if (!$('#lesson').val()) {
        alert('Please Select lesson');
        return false;
    }
}