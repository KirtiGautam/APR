const getStudents = () => {
    $.ajax({
        type: "GET",
        headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr('content') },
        url: '/get-students',
        data: {
            'term': $('#search').val(),
            'class': $('#class').val(),
        },
        dataType: 'json',
        success: function (data) {
            let html = '';
            for (let x = 0; x < data.students.length; x++) {
                let stu = data.students[x];
                html += `<tr><td><input type="checkbox" class="users" value="${stu['id']}"></td><td>${x + 1}</td><td>${stu['Name']}</td><td>${stu['Gender']}</td><td>${stu['DOB']}</td><td>${stu['Email']}</td><td>${stu['Contact']}</td><td>${stu['Address']}</td><td>${stu['Pincode']}</td><td>${stu['City']}</td><td>${stu['District']}</td><td>${stu['State']}</td></tr>`;
            }
            $('#students').html(html);
        }, error: function (error) {
            alert(error.responseText);
        }
    });
}

const getStudent = id => {
    $.ajax({
        type: "GET",
        headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr('content') },
        url: '/get-student',
        data: {
            'id': id
        },
        dataType: 'json',
        success: function (data) {
            $('.Class').val(data['Class']);
            delete data['Class'];
            for (x in data) {
                $('#' + x).val(data[x]);
            }
            console.log(data);
        }, error: function (error) {
            alert(error.responseText);
        }
    });
}

const getSelectedUsers = () => {
    let data = [];
    $('input.users:checkbox:checked').each(function () {
        data.push($(this).val());
    });
    return data;
}

function delay(callback, ms) {
    var timer = 0;
    return function () {
        var context = this, args = arguments;
        clearTimeout(timer);
        timer = setTimeout(function () {
            callback.apply(context, args);
        }, ms || 0);
    };
}

$(document).ready(function () {
    getStudents();

    $('.SIL').addClass('active');
    $('.SI').addClass('siw');
    $('.ST').addClass('stw');

    $('#search_btn').click(function (e) {
        getStudents();
    });
    $('#class').change(function () {
        getStudents();
    });

    $('#excel').click(function () {
        $.ajax({
            type: "GET",
            headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr('content') },
            url: '/get-students',
            data: {
                'term': $('#search').val(),
                'class': $('#class').val(),
            },
            dataType: 'json',
            success: function (data) {

                JSONToCSVConvertor(data.students, "Students", true)
            }, error: function (error) {
                alert(error.responseText);
            }
        });
    });


    $('#newStudent').click(function () {
        $('#US').addClass('d-none');
        $('#ANS').removeClass('d-none');
        $('#first_name').val('')
        $('#last_name').val('')
        $('#gender').val('')
        $('#email').val('')
        $('#Address').val('')
        $('#City').val('')
        $('#District').val('')
        $('#State').val('')
        $('#Pincode').val('')
        $('.Class').val('')
        $('#dob').val('')
        $('#Contact').val('')
        $('#add').modal('show');
    });

    $('#ANS').click(function () {
        if (
            $('#first_name').val() == '' ||
            $('#last_name').val() == '' ||
            $('#gender').val() == '' ||
            $('#email').val() == '' ||
            $('#Address').val() == '' ||
            $('#City').val() == '' ||
            $('#District').val() == '' ||
            $('#State').val() == '' ||
            $('#Pincode').val() == '' ||
            $('.Class').val() == '' ||
            $('#dob').val() == '' ||
            $('#Contact').val() == ''
        ) {
            alert('Please fill all necessary values');
            return;
        }
        $.ajax({
            type: "POST",
            headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr('content') },
            url: '/new-student',
            data: {
                'first_name': $('#first_name').val(),
                'last_name': $('#last_name').val(),
                'gender': $('#gender').val(),
                'email': $('#email').val(),
                'dob': $('#dob').val(),
                'Address': $('#Address').val(),
                'City': $('#City').val(),
                'District': $('#District').val(),
                'State': $('#State').val(),
                'Pincode': $('#Pincode').val(),
                'Contact': $('#Contact').val(),
                'Class': $('.Class').val()
            },
            dataType: 'json',
            success: function (data) {
                alert(data.message);
                getStudents();
            }, error: function (error) {
                alert(error.responseText);
            }
        });
    });


    $('#US').click(function () {
        if (
            $('#first_name').val() == '' ||
            $('#dob').val() == '' ||
            $('#last_name').val() == '' ||
            $('#gender').val() == '' ||
            $('#email').val() == '' ||
            $('#Address').val() == '' ||
            $('#City').val() == '' ||
            $('#District').val() == '' ||
            $('#State').val() == '' ||
            $('#Pincode').val() == '' ||
            $('.Class').val() == '' ||
            $('#Contact').val() == ''
        ) {
            alert('Please fill all necessary values');
            return;
        }
        $.ajax({
            type: "POST",
            headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr('content') },
            url: '/update-student',
            data: {
                'id': $('#UID').val(),
                'first_name': $('#first_name').val(),
                'last_name': $('#last_name').val(),
                'gender': $('#gender').val(),
                'email': $('#email').val(),
                'dob': $('#dob').val(),
                'Address': $('#Address').val(),
                'City': $('#City').val(),
                'District': $('#District').val(),
                'State': $('#State').val(),
                'Pincode': $('#Pincode').val(),
                'Contact': $('#Contact').val(),
                'Class': $('.Class').val()
            },
            dataType: 'json',
            success: function (data) {
                alert(data.message);
                getStudents();
            }, error: function (error) {
                alert(error.responseText);
            }
        });
    });

    $('#edit').click(function () {
        let users = getSelectedUsers();
        if (users.length != 1) {
            alert('Cannot perform this operation, Please select only single user');
            return;
        }
        getStudent(users[0]);
        $('#US').removeClass('d-none');
        $('#ANS').addClass('d-none');
        $('#UID').val(users[0]);
        $('#add').modal('show')
    });
    $('#delete').click(function () {
        let users = getSelectedUsers();
        if (users.length < 1) {
            alert('Please select a user to be deleted');
            return;
        }
        if (confirm('Are you sure you want to delete selection ?')) {
            $.ajax({
                type: "POST",
                headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr('content') },
                url: '/delete-students',
                data: {
                    'id[]': users,
                },
                dataType: 'json',
                success: function (data) {
                    alert(data.message);
                    getStudents();
                }, error: function (error) {
                    alert(error.responseText);
                }
            });
        }
    });

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
                    url: '/upload-students',
                    data: {
                        'file': json_data,
                        'lesson': $('#lesson').val(),
                    },
                    dataType: 'json',
                    success: function (data) {
                        console.log(data)
                        $('#file').val('');
                        alert(data.message)
                    }, error: function (error) {
                        alert(error.responseText);
                    }
                });
            };
        })(file);

        reader.onerror = function (event) {
            console.error("File could not be read! Code " + event.target.error.code);
        };

        reader.readAsBinaryString(selectedFile);
    })
});