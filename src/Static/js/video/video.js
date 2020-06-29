if ($('#video_player').attr('src').includes('vimeo')) {
  var head = document.getElementsByTagName('head')[0];
  var js = document.createElement("script");

  js.type = "text/javascript";

  js.src = "https://player.vimeo.com/api/player.js"

  head.appendChild(js);

}

let thumbarr = [];

const MAS = () => {
  $.ajax({
    type: "POST",
    headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr("content") },
    url: url,
    data: {
      id: id,
    },
    dataType: "json",
    success: function (response) {
      alert(response.message);
      location.reload()
    }, error: function (error) {
      alert(error.responseText);
    }
  });
}

const loadplayer = () => {
  let cue_mark;
  var iframe = $('#video_player');
  var player = new Vimeo.Player(iframe);
  player.getDuration().then(function (vid_duration) {
    $('#main_vid_dura').html(duration(vid_duration))
    cue_mark = Math.floor(0.8 * vid_duration);
  });

  player.on('play', function () {
    setInterval(() => {
      player.getCurrentTime().then(function (seconds) {
        if (cue_mark < seconds && !marked) {
          marked = true;
          $.ajax({
            type: "POST",
            headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr("content") },
            url: url,
            data: {
              id: id,
            },
            dataType: "json",
            success: function (response) {
              $('#mark_complete_btn').removeClass('mark');
              $('#mark_complete_btn').addClass('marked');
              console.log(response.message);
            }, error: function (error) {
              marked = false;
              alert(error.responseText);
            }
          });
        }
      });
    }, 900);
  });

}

$(function () {
  setTimeout(loadplayer, 1000)
})