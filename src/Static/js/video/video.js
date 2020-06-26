let thumbarr = [];

const MAS = (url, id) => {
  $.ajax({
    type: "POST",
    headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr("content") },
    url: url,
    data: {
      id: id,
    },
    dataType: "json",
    success: function (response) {
      location.reload()
      alert(response.message);
    }, error: function (error) {
      alert(error.responseText);
    }
  });
}