//UPLOADING AND DELETING FILES TO BE TRANSCRIBED IN FRENCH CHINESE ENGLISH 
function de() {
  $("input[type=button]").attr("style", "display:none");
}

$(document).ready(function() {
  de();

  $("#example-file").on("change", function() {
    if ($("#example-file").val() != "") {
     // $("label[class=btn btn-default btn-file]").attr("style", "display:block");
      $("button[type=button]");//.attr("style", "display:block");
    } else {
      de();
    }
  });
  $("button[type=button]").click(function() {
	$("#example-file").val('');
	$('#form-control').empty();
	//$('#messages').empty();
	$('#messages').contents().filter(function () {
		return this.id != "noRemove";
	}).remove();
    de();
  })

})

function download(filename, text) {
	var element = document.createElement('a');
	element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
	element.setAttribute('download', filename);

	element.style.display = 'none';
	document.body.appendChild(element);

	element.click();

	document.body.removeChild(element);
}

