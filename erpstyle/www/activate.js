
    frappe.call({
    type: "POST",
    method: "erpstyle.appi.install_instance",
    args: {code: $("#name").val()}
    ,
    callback: function(r) {
        if(r.message) {
            $('#myModal').find('.modal-body').html(r.message);
            $('#myModal').modal('toggle');
            $("#notefier").html(r.message);
        }

    }});

