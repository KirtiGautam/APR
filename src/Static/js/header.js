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
      let html = '';
      if (response.notifications.length > 0) {
        response.notifications.forEach(notif => {
          html += `<a class="dropdown-item p-2 ${notif.read ? 'unread' : ''}" href="${notif.link}">${notif.message}</a><div class="dropdown-divider"></div>`
        });
      } else {
        html += '<span class="dropdown-item p-2">No notifications</span>';
      }
      $('#notif-list').html(html);
    }, error: function (error) {
      console.log(error.responseText);
    }
  });

});
