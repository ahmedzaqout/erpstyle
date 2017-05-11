$("#myModal").refresh(function(e){
// $("#close").click(function(e){
//     e.preventDefault();
    console.log('mmm')
    frappe.call({
    type: "POST",
    method: "erpstyle.appi.install_instance",
    args: {
      code: '4f19778aae6b4bf38f3b4464cba0cc32'
    },
    callback: function(r) {
console.log(r.message)
        if(r.message) {
            $('#myModal').find('.modal-body').html(r.message);
            $('#myModal').modal('toggle');
            $("#notefier").html(r.message);
        }

    }});

});
