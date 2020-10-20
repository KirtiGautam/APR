var toolbarOptions = [
  ["bold", "italic", "underline", "strike"], // toggled buttons
  ["blockquote", "code-block"],

  [{ header: 1 }, { header: 2 }], // custom button values
  [{ list: "ordered" }, { list: "bullet" }],
  [{ script: "sub" }, { script: "super" }], // superscript/subscript
  [{ indent: "-1" }, { indent: "+1" }], // outdent/indent
  [{ direction: "rtl" }], // text direction

  [{ size: ["small", false, "large", "huge"] }], // custom dropdown
  [{ header: [1, 2, 3, 4, 5, 6, false] }],

  [{ color: [] }, { background: [] }], // dropdown with defaults from theme
  [{ font: [] }],
  [{ align: [] }],
  ["link"],
  ["clean"], // remove formatting button
];

var quill = new Quill("#body", {
  modules: {
    toolbar: toolbarOptions,
  },
  theme: "snow",
});

let offset = 0;
let loaded = false;
let allLoaded = true;

function _(el) {
  return document.getElementById(el);
}

function progressHandler(event) {
  var percent = (event.loaded / event.total) * 100;
  $("#prog-bar")
    .attr("aria-valuenow", Math.round(percent))
    .css("width", Math.round(percent) + "%")
    .text(Math.round(percent) + "%");
}

function completeHandler(event) {
  $("#posts-box").prepend(JSON.parse(event.target.responseText));
  $("#photo").val("");
  quill.root.innerHTML = "";
  $("#tag").val("");
  $("#message").val("Uplaod Successfull");
  $("#progress-wrap, #post-pic-prev").addClass("d-none");
  $("#prog-bar")
    .attr("aria-valuenow", 0)
    .css("width", 0 + "%")
    .text(0 + "%");
}

function errorHandler(event) {
  $("#message").val("Uplaod Failed");
  $("#progress-wrap, #post-pic-prev").addClass("d-none");
  quill.root.innerHTML = "";
  $("#photo").val("");
  $("#tag").val("");
  $("#prog-bar")
    .attr("aria-valuenow", 0)
    .css("width", 0 + "%")
    .text(0 + "%");
}

function abortHandler(event) {
  $("#progress-wrap, #post-pic-prev").addClass("d-none");
  $("#message").val("Uplaod Abort");
  quill.root.innerHTML = "";
  $("#photo").val("");
  $("#tag").val("");
  $("#prog-bar")
    .attr("aria-valuenow", 0)
    .css("width", 0 + "%")
    .text(0 + "%");
}

const posts = () => {
  $("#loader").removeClass("d-none");
  $.ajax({
    type: "GET",
    url: `/post${getParams}`,
    data: {
      offset: offset,
    },
    dataType: "json",
    success: (data) => {
      if (data.all) {
        allLoaded = false;
      } else {
        $("#posts-box").append(data);
        offset++;
      }
      loaded = true;
      $("#loader").addClass("d-none");
    },
    error: function (error) {
      alert(error.responseText);
    },
  });
};

const like = (id) => {
  $.ajax({
    type: "POST",
    headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr("content") },
    url: "/like-post",
    data: {
      id: id,
    },
    dataType: "json",
    success: function (data) {
      alert(data.liked);
      document.getElementById(`post-like-counter${id}`).innerText = data.count;
    },
    error: function (error) {
      alert(error.responseText);
    },
  });
};

const copyLink = (url) => {
  $("#clipboar").removeClass("d-none");
  /* Get the text field */
  var copyText = document.getElementById("clipboar");
  copyText.value = url;

  /* Select the text field */
  copyText.select();
  copyText.setSelectionRange(0, 99999); /*For mobile devices*/

  /* Copy the text inside the text field */
  document.execCommand("copy");

  /* Alert the copied text */
  alert("Link copied to clipboard");
  $("#clipboar").addClass("d-none");
};

$(function () {
  posts();
  $(window).on("scroll", function () {
    console.log("scroll");
    if (
      $(this).scrollTop() + $(this).innerHeight() >=
        $("#posts-box")[0].scrollHeight &&
      loaded &&
      allLoaded
    ) {
      loaded = false;
      posts();
    }
  });
  $("#photo").on("change", function () {
    var reader = new FileReader();

    reader.onload = function (e) {
      $("#post-pic-prev").attr("src", e.target.result).removeClass("d-none");
    };

    reader.readAsDataURL(this.files[0]);
  });

  $("#submit-btn").on("click", function () {
    if (!$("#body").text() && !$("#photo").val()) {
      alert("Please type some text or add a picture to post");
      return;
    }
    var formdata = new FormData();
    if ($("#photo").val()) {
      var file = _("photo").files[0];
      formdata.append("photo", file);
    }
    if ($("#body").text()) formdata.append("body", quill.root.innerHTML);
    else formdata.append("body", "");
    formdata.append("category", $("#tag").val());
    var ajax = new XMLHttpRequest();
    ajax.upload.addEventListener("progress", progressHandler, false);
    ajax.addEventListener("load", completeHandler, false);
    ajax.addEventListener("error", errorHandler, false);
    ajax.addEventListener("abort", abortHandler, false);
    ajax.open("POST", "/post"); // http://www.developphp.com/video/JavaScript/File-Upload-Progress-Bar-Meter-Tutorial-Ajax-PHP
    ajax.setRequestHeader(
      "X-CSRFToken",
      $('meta[name="csrf-token"]').attr("content")
    );
    ajax.send(formdata);
    $("#progress-wrap").removeClass("d-none");
  });
});
