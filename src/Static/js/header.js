$(document).ready(function () {
  if ($(window).width() <= 800) {
    $(".leftside").addClass("d-none");
    $(".second-side").addClass("d-none");
  }

  $("#sidebarCollapse").click(function () {
    $(".leftside").toggleClass("d-none");
    if ($(window).width() <= 800) {
      $(".second-side").addClass("d-none");
    }
  });

  $("#right-nav").click(function () {
    $(".second-side").toggleClass("d-none");
    if ($(window).width() <= 800) {
      $(".leftside").addClass("d-none");
    }
  });

  $(window).resize(function () {
    if ($(window).width() <= 800) {
      $(".leftside").addClass("d-none");
      $(".second-side").addClass("d-none");
    } else {
      $(".leftside").removeClass("d-none");
      $(".second-side").removeClass("d-none");
    }
  });
});
