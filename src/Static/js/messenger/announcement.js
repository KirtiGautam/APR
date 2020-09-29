let individual = [];
let group = [];
let Class = [];
let Media = [];

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

var quill = new Quill("#message-textarea", {
  modules: {
    toolbar: toolbarOptions,
  },
  theme: "snow",
});

const addGroup = (el) => {
  if (group.includes(el)) {
    group.splice(
      group.findIndex((ele) => ele === el),
      1
    );
  } else {
    group.push(el);
  }
  console.log(group);
};
const addIndividual = (el) => {
  el = parseInt(el);
  if (individual.includes(el)) {
    individual.splice(
      individual.findIndex((ele) => ele === el),
      1
    );
  } else {
    individual.push(el);
  }
  console.log(individual);
};
const addClass = (el) => {
  el = parseInt(el);
  if (Class.includes(el)) {
    Class.splice(
      Class.findIndex((ele) => ele === el),
      1
    );
  } else {
    Class.push(el);
  }
  console.log(Class);
};
const addMedia = (el) => {
  if (Media.includes(el)) {
    Media.splice(
      Media.findIndex((ele) => ele === el),
      1
    );
  } else {
    Media.push(el);
  }
  console.log(Media);
};

const sendAnnouncement = () => {
  if (group.length < 1 && individual.length < 1 && Class.length < 1) {
    alert("Please add atleast one Recipient");
    return;
  }
  if (Media.length < 1) {
    alert("Please add atleast one Medium for sending announcement");
    return;
  }
  if (!$("#title-input").val()) {
    alert("Please give appropriate title to announcement");
    return;
  }
  console.log(quill.root.textContent);
  if (!quill.root.textContent) {
    alert("Please enter some text");
    return;
  }
  $("#send-btn").addClass("d-none");
  $("#spinner").removeClass("d-none");
  $.ajax({
    type: "POST",
    headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr("content") },
    url: "/make-announcement",
    data: {
      group: group,
      individual: individual,
      Class: Class,
      Media: Media,
      title: $("#title-input").val(),
      text: quill.root.innerHTML,
    },
    dataType: "json",
    success: (data) => {
      console.log(data);
      $("#send-btn").removeClass("d-none");
      $("#spinner").addClass("d-none");
      location.reload();
    },
    error: function (error) {
      $("#send-btn").removeClass("d-none");
      $("#spinner").addClass("d-none");
      alert(error.responseText);
    },
  });
  console.log(quill.root.innerHTML);
};

let annss;

const getAnnouncements = () => {
  $.ajax({
    type: "GET",
    headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr("content") },
    url: "/announcements",
    dataType: "json",
    success: (data) => {
      $("#conversations-box").html(
        data.map(
          (
            element
          ) => `
          <div class="row row-12 reciever-class${element.id}" onclick="startChat(${element.id});">
            <div>
              <img src="static/Images/lesson/back.png" alt="" class="col-12 image-1">
            </div>
            <div>
              <div class="row">
                <div class="col-6 text-truncate text-2">
                  ${element.Title}
                </div>
                <div class="col-6 text-truncate text-3">${element.Created}</div>
                <div class="col-12 text-4">${element.Message}</div>
              </div>
            </div>
          </div>`
        )
      );

      annss = data;
      console.log(data);
    },
    error: function (error) {
      $("#message-loader").addClass("d-none");
      alert(error.responseText);
    },
  });
};
getAnnouncements();
const chatList = setInterval(getAnnouncements, 10000);

const startChat = (id) => {
  const element = annss.find((el) => el.id === parseInt(id));
  $("#no-sel-prev, #new-announcement-container").addClass("d-none");
  $("#anns-title").html(element.Title);
  $("#anns-Created").html(element.Created);
  $("#anns-Message").html(element.Message);
  $("#announcement-prev").removeClass("d-none");
};

$(function () {
  $("#add-ann-btn").click(() => {
    $("#new-announcement-container").removeClass("d-none");
    $("#no-sel-prev, #announcement-prev").addClass("d-none");
  });
  $("#group-tab-btn, #class-tab-btn, #individual-tab-btn").click(function () {
    $("#group-tab, #class-tab, #individual-tab").addClass("d-none");
    $("#group-tab-btn, #class-tab-btn, #individual-tab-btn").removeClass(
      "btn-2-active"
    );
    console.log(`#${this.id.substring(0, this.id.length - 4)}`);
    $(`#${this.id.substring(0, this.id.length - 4)}`).removeClass("d-none");
    $(this).addClass("btn-2-active");
  });
});
