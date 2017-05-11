$(document).ready(function(){
//$("#test_form").submit(function(e){
    args= { "name": "name" ,"email":"login.live.ps.ps@gmail.com","telephone":"123"}


//    var msg = '<i class="fa fa-spinner fa-spin"></i>';
//    msg +=  " "+$("#email_message").html();
//    $("#notefier").html(msg).removeClass("alert-danger").removeClass("alert-success").addClass('alert-info').show();
alert("svsvbs")
 // e.preventDefault();
//    var data = JSON.parse(JSON.stringify($("#instance_form").serializeArray()));
//    var args = {};
//    $.each(data, function(index, obj) {
//        args[obj['name']] = obj['value']
//    });


    $.ajax({
  method: "POST",
  data:args,
  url: "api/method/erpstyle.appi.add_instance"


})



//    frappe.call({
//        type: "POST",
//        method: "/api/method/erpstyle.appi.add_instance",
//        args : args ,
//        callback: function(r) {
//alert("Done")
//        }
//    });
//});

//    frappe.call({
//    type: "POST",
//    method: "erpstyle.appi.add_instance",
//    args:args
//    ,
//    callback: function(r) {
//        if(r.message) {
//
//        }
//
//    }});



});
//});