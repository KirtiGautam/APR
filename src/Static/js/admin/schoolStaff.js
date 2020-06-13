const getStaff = () => {
    $.ajax({
        type: "GET",
        headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr('content') },
        url: '/get-staff',
        data: {
            'term': $('#search').val(),
            'type': $('#type').val(),
        },
        dataType: 'json',
        success: function (data) {
            let html = '';
            for (let x = 0; x < data.staff.length; x++) {
                let staff = data.staff[x];
                html += `<tr><td><input type="checkbox" class="users" value="${staff['id']}"></td><td>${x + 1}</td><td>${staff['Name']}</td><td>${staff['Email']}</td>`;
            }
            $('#Staff').html(html);
        }
    });
}

const getUser = id => {
    $.ajax({
        type: "GET",
        headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr('content') },
        url: '/get-user',
        data: {
            'id': id
        },
        dataType: 'json',
        success: function (data) {
            for (x in data) {
                $('#' + x).val(data[x]);
            }
            console.log(data);
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
    getStaff()

    $('.SSL').addClass('active');
    $('.SSLT').addClass('stw');
    $('.SSLI').addClass('siw');

    $('#search').keyup(delay(function (e) {
        getStaff();
    }, 500));

    $('#type').change(function () {
        getStaff();
    });

    $('#excel').click(function () {
        $.ajax({
            type: "GET",
            headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr('content') },
            url: '/get-staff',
            data: {
                'term': $('#search').val(),
                'type': $('#type').val(),
            },
            dataType: 'json',
            success: function (data) {

                JSONToCSVConvertor(data.staff, "Staff", true)
            }
        });
    });

    $('#newStaff').click(function () {
        $('#US').addClass('d-none');
        $('#ANS').removeClass('d-none');
        $('#first_name').val('')
        $('#last_name').val('')
        $('#email').val('')
        $('#add').modal('show');
    });

    $('#ANS').click(function () {
        if (
            $('#first_name').val() == '' ||
            $('#last_name').val() == '' ||
            $('#email').val() == ''
        ) {
            alert('Please fill all necessary values');
            return;
        }
        $.ajax({
            type: "POST",
            headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr('content') },
            url: '/new-staff',
            data: {
                'first_name': $('#first_name').val(),
                'last_name': $('#last_name').val(),
                'email': $('#email').val(),
            },
            dataType: 'json',
            success: function (data) {
                alert(data.message);
                getStaff();
            }
        });
    });

    $('#US').click(function () {
        if (
            $('#first_name').val() == '' ||
            $('#last_name').val() == '' ||
            $('#email').val() == ''
        ) {
            alert('Please fill all necessary values');
            return;
        }
        $.ajax({
            type: "POST",
            headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr('content') },
            url: '/update-staff',
            data: {
                'id': $('#UID').val(),
                'first_name': $('#first_name').val(),
                'last_name': $('#last_name').val(),
                'email': $('#email').val(),
            },
            dataType: 'json',
            success: function (data) {
                alert(data.message);
                getStaff();
            }
        });
    });

    $('#edit').click(function () {
        let users = getSelectedUsers();
        if (users.length != 1) {
            alert('Cannot perform this operation, Please select only single user');
            return;
        }
        getUser(users[0]);
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
                url: '/delete-staff',
                data: {
                    'id[]': users,
                },
                dataType: 'json',
                success: function (data) {
                    alert(data.message);
                    getStaff();
                }
            });
        }
    });
});