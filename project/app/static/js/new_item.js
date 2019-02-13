
$('#id_ajax_upload_form').submit(function(e){
        e.preventDefault();
        $form = $(this)
        var formData = new NewItemForm(this);
        $.ajax({
            url: '/ajax/newitem/',
            type: 'POST',
            data: formData,
            async: false,
            success: function(data){
              alert(data['success'])
            },
            cache: false,
            contentType: false,
            processData: false
        });
    });
    // end
