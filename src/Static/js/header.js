$(document).ready(function () {
  if ($(window).width() <= 800) {
    $(".leftside").addClass("d-none");
    $(".content").addClass("no-margin");
    $(".second-side").addClass("d-none");
  }

  $("#sidebarCollapse").click(function () {
    $(".leftside").toggleClass("d-none");
    $(".content").toggleClass("no-margin");
    if ($(window).width() <= 800) {
      $(".second-side").addClass("d-none");
      $(".content").addClass("no-margin");
    }
  });

  $("#right-nav").click(function () {
    $(".second-side").toggleClass("d-none");
    if ($(window).width() <= 800) {
      $(".leftside").addClass("d-none");
      $(".content").addClass("no-margin");
    }
  });

  $(window).resize(function () {
    if ($(window).width() <= 800) {
      $(".leftside").addClass("d-none");
      $(".second-side").addClass("d-none");
      $(".content").addClass("no-margin");
    } else {
      $(".leftside").removeClass("d-none");
      $(".second-side").removeClass("d-none");
      $(".content").removeClass("no-margin");
    }
  });
});
