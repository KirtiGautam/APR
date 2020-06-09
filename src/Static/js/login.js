function check() {
    let account = $('#Type').val();
    let username = $('#username').val();
    let password = $('#password').val();
    if (
        account == '' ||
        account == null) {
        alert('Please select account Type');
        return false;
    }
    if (
        username == '' ||
        username == null) {
        alert('Please enter your username');
        return false;
    }
    if (
        password == '' ||
        password == null) {
        alert('Please enter your password');
        return false;
    }
    return true;
}