const getChatList = () => {
  $.ajax({
    type: "GET",
    url: "/get-conversations",
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
            `<li onclick="startChat(${element.id});">${element.name}</li>`
        )
      ),
    error: function (error) {
      alert(error.responseText);
    },
  });
};

const getNewMessages = (id) => {
  $.ajax({
    type: "GET",
    url: "/get-new-messages",
    data: {
      id: id,
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

const startChat = (id) => {
  $("#user-search-modal").modal("hide");
  $("#message-loader").removeClass("d-none");
  $.ajax({
    type: "GET",
    url: "/get-messages",
    data: {
      id: id,
    },
    dataType: "json",
    success: (data) => {
      $("#message-loader").addClass("d-none");
      $("#reciever-name").html(data.user);
      $("#reciever-status").html(data.status);
      $("#messages-box").html(data.messages);
      $("#reciever-id").val(id);
      clearInterval(inter);
      inter = setInterval(() => getNewMessages(id), 5000);
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
const mod = () => {
  search();
  $("#user-search-modal").modal();
};

$(function () {
  $("#user-search-box").keyup((el) => {
    search(el.currentTarget.value);
  });
  $("#text-to-send").keyup((el) => {
    $("#send-btn").attr("disabled", !el.currentTarget.value);
  });
});
