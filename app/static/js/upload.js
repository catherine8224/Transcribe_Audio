/*$(document).ready(function() {

	$('form').on('submit', function(event) {

		event.preventDefault();

		var formData = new FormData($('form')[0]);

		$.ajax({
			xhr : function() {
				var xhr = new window.XMLHttpRequest();

				xhr.upload.addEventListener('progress', function(e) {

					if (e.lengthComputable) {

						console.log('Bytes Loaded: ' + e.loaded);
						console.log('Total Size: ' + e.total);
						console.log('Percentage Uploaded: ' + (e.loaded / e.total))

						var percent = Math.round((e.loaded / e.total) * 100);

						$('#progressBar').attr('aria-valuenow', percent).css('width', percent + '%').text(percent + '%');

					}

				});

				return xhr;
			},
			type : 'POST',
			url : '/upload_form',
			data : formData,
			processData : false,
			contentType : false,
			success : function() {
				alert('File uploaded!');
			}
		});

	});

});
*/


$(document).ready(function() {
  de();

  $("#example-file").on("change", function() {
    if ($("#example-file").val() != "") {
     // $("label[class=btn btn-default btn-file]").attr("style", "display:block");
      $("input[type=button]").attr("style", "display:block");
    } else {
      de();
    }
  });
  $("input[type=button]").click(function() {
	$("#example-file").val('');
	$('#form-control').empty();
	//$('#messages').empty();
	$('#messages').contents().filter(function () {
		return this.id != "noRemove";
	}).remove();
    de();
  })

})

function de() {
  $("input[type=button]").attr("style", "display:none");
}


function download(filename, text) {
	var element = document.createElement('a');
	element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
	element.setAttribute('download', filename);

	element.style.display = 'none';
	document.body.appendChild(element);

	element.click();

	document.body.removeChild(element);
}

