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
    $('#edit_btn').click(function () {
        let Sdata = []
        $('input.ques_checks:checkbox:checked').each(function () {
            Sdata.push($(this).val());
        });
        if (Sdata.length != 1) {
            alert('Please select single question to update')
            return
        }
        $('#hidden_question_field').val(Sdata[0]);
        $.ajax({
            type: "GET",
            headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr('content') },
            url: '/get-question',
            data: {
                question: Sdata[0],
            },
            dataType: 'json',
            success: function (data) {
                $('#question_Name').val(data.Name);
                let counter = 0;
                html = '';
                for (let x in data.choices) {
                    counter++;
                    $(`#hidden_choice_${counter}`).val(data.choices[x].id)
                    $(`#choice_${counter}`).val(data.choices[x].Name)
                    html += `<option value="${data.choices[x].id}">Choice ${counter}</option>`
                }
                $('#Difficulty').val(data.Difficulty.substring(0, 1))
                $('#Answer').html(html);
                $('#Answer').val(data.Answer)
                $('#edit').modal('show');
            }, error: function (error) {
                alert(error.responseText);
            }
        });
    })

    $('#update_btn').click(function () {
        if (!$('#question_Name').val() ||
            !$('#choice_1').val() ||
            !$('#choice_2').val() ||
            !$('#choice_3').val() ||
            !$('#choice_4').val()) {
            alert('Please fill all the values')
            return;
        }
        let Sdata = []
        for (let x = 1; x < 5; x++) {
            Sdata.push(JSON.stringify({
                id: $(`#hidden_choice_${x}`).val(),
                Name: $(`#choice_${x}`).val()
            }));
        }
        console.log($('#hidden_question_field').val());
        $.ajax({
            type: "POST",
            headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr('content') },
            url: '/edit-question',
            data: {
                question: $('#hidden_question_field').val(),
                Name: $('#question_Name').val(),
                Difficulty: $('#Difficulty').val(),
                choices: Sdata,
                answer: $('#Answer').val()
            },
            dataType: 'json',
            success: function (data) {
                location.reload();
                alert(data.message);
            }, error: function (error) {
                alert(error.responseText);
            }
        });
    })

    $('#delete_btn').click(function () {
        let Sdata = []
        $('input.ques_checks:checkbox:checked').each(function () {
            Sdata.push($(this).val());
        });
        if (Sdata.length < 1) {
            alert('Please select questions to delete')
            return;
        }
        if (confirm('Are you sure you want to delete selected data?')) {
            $.ajax({
                type: "POST",
                headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr('content') },
                url: '/delete-questions',
                data: {
                    data: Sdata,
                },
                dataType: 'json',
                success: function (data) {
                    location.reload();
                    alert(data.message)
                }, error: function (error) {
                    alert(error.responseText);
                }
            });
        }
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