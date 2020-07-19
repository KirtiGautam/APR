const notif_read = (id, e) => {
  $.ajax({
    type: "POST",
    headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr("content") },
    url: '/notification-read',
    data: {
      id: id,
    },
    dataType: "json",
    success: function (response) {
      console.log(response)
      window.location.href = e.value;
    }, error: function (error) {
      console.log(error.responseText);
    }
  });

}

$(document).ready(function () {
  if ($(window).width() <= 1100) {
    $(".leftside").addClass("d-none");
    $(".content").addClass("no-margin");
    $(".second-side").addClass("d-none");
  }

  $("#sidebarCollapse").click(function () {
    $(".leftside").toggleClass("d-none");
    $(".content").toggleClass("no-margin");
    if ($(window).width() <= 1100) {
      $(".second-side").addClass("d-none");
      $(".content").addClass("no-margin");
    }
  });

  $("#right-nav").click(function () {
    $(".second-side").toggleClass("d-none");
    if ($(window).width() <= 1100) {
      $(".leftside").addClass("d-none");
      $(".content").addClass("no-margin");
    }
  });

  $(window).resize(function () {
    if ($(window).width() <= 1100) {
      $(".leftside").addClass("d-none");
      $(".second-side").addClass("d-none");
      $(".content").addClass("no-margin");
    } else {
      $(".leftside").removeClass("d-none");
      $(".second-side").removeClass("d-none");
      $(".content").removeClass("no-margin");
    }
  });

  $.ajax({
    type: "GET",
    headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr("content") },
    url: '/get-all-notifications',
    dataType: "json",
    success: function (response) {
      let html = '', count = 0;
      if (response.notifications.length > 0) {
        response.notifications.forEach(notif => {
          if (notif.read) {
            html += `<button class="dropdown-item p-2 read"><a href="${notif.link}">${notif.message}<br><small class="text-secondary float-right">${notif.time}</small></a></button>`
          } else {
            count += 1;
            html += `<button class="dropdown-item p-2 unread" onclick="notif_read(${notif.id}, this);" value="${notif.link}">${notif.message}<br><small class=" text-secondary float-right">${notif.time}</small></button>`
          }
        });
      } else {
        html += '<span class="dropdown-item p-2">No notifications</span>';
      }
      $('#notif-list').html(html);
      $('.noti-badge').html(count);
    }, error: function (error) {
      console.log(error.responseText);
    }
  });

});
