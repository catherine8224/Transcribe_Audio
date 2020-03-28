//function toggle_display(){
//  el = document.querySelector('.maintainer');
  
//  if(el.style.visibility == 'hidden'){
//     el.style.visibility = 'visible'
//  }else{
//     el.style.visibility = 'hidden'
//  }
//}

//$(document).ready(function() {
  //$('#btn-example-file-reset').on('click', function() {     
   //  $('#example-file').val('');
 // });
//});


$(document).ready(function() {
  de();

  $("#example-file").on("change", function() {



    if ($("#example-file").val() != "") {
      $("input[type=button]").attr("style", "display:block");
    } else {
      de();
    }
  });
  $("input[type=button]").click(function() {
    $(".form-control").val('');
    de();
  })

})

function de() {
  $("input[type=button]").attr("style", "display:none");
}