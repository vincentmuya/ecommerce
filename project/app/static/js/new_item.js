$(document).ready(function(){
  $('form').submit(function(event){
    event.preventDefault()
    form = $("form")

    $.ajax({
      'url':'/ajax/newitem/',
      'type':'POST',
      'data':form.serialize(),
      'dataType':'json',
      'success': function(data){
        alert(data['success'])
      },
    })// END of Ajax method
    $('#id_seller_number').val('')
    $("#id_seller_location").val('')
    $("#id_item_name").val('')
    $("#id_category").val('')
    $("#id_item_price").val('')
    $("#id_item_image").val('')
    $("#id_email").val('')
  }) // End of submit event
    
}) // End of document ready function
