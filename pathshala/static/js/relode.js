 $("#next").click(function(){
    var text = document.getElementById('postcomment').value;
    var slug='{{slug}}'
    $.ajax({
      url: '/videos',
      type: "get",
      data: {postcomment: text,slug:slug},
      success: function(response) {
        $("#Comments").html(response);
      },
      error: function(xhr) {
        //Do Something to handle error
      }
    });

 });
