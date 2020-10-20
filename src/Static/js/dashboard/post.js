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

const likeComment = (id) => {
  $.ajax({
    type: "POST",
    headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr("content") },
    url: "/like-post-comment",
    data: {
      id: id,
    },
    dataType: "json",
    success: function (data) {
      alert(data.liked);
      document.getElementById(`com${id}`).innerText = data.count;
    },
    error: function (error) {
      alert(error.responseText);
    },
  });
};

const toggleReply = (id) => {
  $(`.hidden-reply-div${id}`).toggleClass("d-none");
};

const update = () => {
  $.ajax({
    type: "POST",
    headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr("content") },
    url: "/update/post",
    data: {
      id: $("#hidden_post_id").val(),
      updated_body: quill.root.innerHTML,
    },
    dataType: "json",
    success: function (data) {
      location.reload();
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
