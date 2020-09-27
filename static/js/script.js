$(document).ready(function() {
    alert("ok")
    var form = $('#conv_form');
    form.submit(function(ev) {
      ev.preventDefault();
      $.ajax({
        type: form.attr('method'),
        url: form.attr('action'),
        data: form.serialize(),
        success: function(data) {
          alert('ok');
        }
      });
    });
  });