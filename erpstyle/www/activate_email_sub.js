$(document).ready(function(){
    frappe.call({
    type: "POST",
    method: "erpstyle.mail_data.api.activate_mail",
    args: {
      code: $("#code").val()
    },
    callback: function(r) {
        if(r.message) {
            $('#myModal').find('.modal-body').html(r.message);
            $('#myModal').modal('toggle');
            $("#notefier").html(r.message);
        }

    }});

})
