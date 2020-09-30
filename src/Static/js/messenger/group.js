let selected = [];

const getChatList = () => {
  $.ajax({
    type: "GET",
    url: "/get-conversations",
    data: {
      type: "G",
    },
    dataType: "json",
    success: (data) => {
      const el = $("#modal-container-div");
      $("#conversations-box").html(data.body).append(el);
      if ($("#reciever-id").val())
        $(`.reciever-class${$("#reciever-id").val()}`).addClass(
          "row-1-4-active"
        );
    },
    error: function (error) {
      alert(error.responseText);
    },
  });
};
getChatList();
const chatList = setInterval(getChatList, 5000);

const search = (val = "") => {
  $.ajax({
    type: "GET",
    url: "/search-users",
    data: {
      q: val,
    },
    dataType: "json",
    success: (data) =>
      $("#users-list").html(
        data.users.map(
          (element) =>
            `<tr class="text-6"><td><input type="checkbox" class="input-2" value="${
              element.id
            }" onclick="clickHandle(this);" ${
              selected.includes(parseInt(element.id)) ? "checked" : ""
            }></td><td class="text-11">${element.name}</td></tr>`
        )
      ),
    error: function (error) {
      alert(error.responseText);
    },
  });
};

const mod = () => {
  search();
  $("#user-search-modal").modal();
};

const clickHandle = (el) => {
  el = parseInt(el.value);
  if (selected.includes(el)) {
    selected.splice(
      selected.findIndex((ele) => ele == el),
      1
    );
  } else {
    selected.push(el);
  }
};

const getNewMessages = (id) => {
  $.ajax({
    type: "GET",
    url: "/get-new-messages",
    data: {
      id: id,
      type: "G",
    },
    dataType: "json",
    success: (data) => {
      $("#reciever-status").html(data.status);
      $("#messages-box").append(data.messages);
    },
    error: function (error) {
      alert(error.responseText);
    },
  });
};

let inter;

const startChat = (id = "") => {
  let type, data;
  if (id == "") {
    if (!$("#g-name").val() || !$("#g-text").val()) {
      alert("Please Type a text and Group Name");
      return;
    }
    if (selected.length < 2) {
      alert("Please Select at least 2 members");
      return;
    }
    data = {
      selected: selected,
      name: $("#g-name").val(),
      text: $("#g-text").val(),
    };
    type = "POST";
  } else {
    data = {
      id: id,
      type: "G",
    };
    type = "GET";
  }
  $("#user-search-modal").modal("hide");
  $("#message-loader").removeClass("d-none");
  $.ajax({
    type: type,
    headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr("content") },
    url: "/get-messages",
    data: data,
    dataType: "json",
    success: (data) => {
      $("#message-loader").addClass("d-none");
      $("#reciever-name").html(data.name);
      $("#messages-box").html(data.messages);
      $("#reciever-id").val(data.group);
      clearInterval(inter);
      inter = setInterval(() => getNewMessages(data.group), 5000);
    },
    error: function (error) {
      $("#message-loader").addClass("d-none");
      alert(error.responseText);
    },
  });
};

const sendText = () => {
  const text = $("#text-to-send").val();
  $("#text-to-send").val("").keyup();

  $.ajax({
    type: "POST",
    headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr("content") },
    url: "/send-message",
    data: {
      id: $("#reciever-id").val(),
      text: text,
      type: "G",
    },
    dataType: "json",
    success: (data) => {
      $("#messages-box").append(data.message);
    },
    error: function (error) {
      $("#message-loader").addClass("d-none");
      alert(error.responseText);
    },
  });
};

$(function () {
  $("#user-search-box").keyup((el) => {
    search(el.currentTarget.value);
  });
  $("#text-to-send").keyup((el) => {
    $("#send-btn").attr("disabled", !el.currentTarget.value);
  });
});
