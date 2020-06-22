$(document).ready(function () {
    $('#change').click(function (e) {
        e.preventDefault();
        let ne = $('#new').val(), rene = $('#renew').val(), pre = $('#pre').val();
        if (!ne ||
            !rene ||
            !pre) {
            alert('Please Fill all values');
            return;
        } else if (ne.length < 8) {
            alert('Passwords cannot be shorter than 8 characters');
            return;
        } else if (ne == $('#pre').val()) {
            alert('New Password cannot be same as current');
            return;
        } else if (ne !=
            rene) {
            alert("Passwords don't match");
            return;
        }
        $.ajax({
            type: "POST",
            headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr("content") },
            url: '/settings/change-password',
            data: {
                'password': ne,
                'pre': $('#pre').val(),
            },
            dataType: 'json',
            success: function (data) {
                $('#new').val('');
                $('#renew').val('');
                $('#pre').val('');
                alert(data.message);
            }
        });
    });
})