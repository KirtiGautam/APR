var countdown = setInterval(function () {
  var over = new Date(timeLeft).getTime();
  var now = new Date().getTime();
  var timeleft = over - now;
  var hours = Math.floor((timeleft % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  var minutes = Math.floor((timeleft % (1000 * 60 * 60)) / (1000 * 60));
  var seconds = Math.floor((timeleft % (1000 * 60)) / 1000);
  if (timeleft < 0) {
    clearInterval(countdown);
    $("#left-time").text(`Time UP!`);
  } else $("#left-time").text(`Time left ${hours}:${minutes}:${seconds}`);
}, 1000);
