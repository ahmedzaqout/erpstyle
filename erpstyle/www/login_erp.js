$("#instance_form").submit(function(e){
//alert("test")

    var msg = '<i class="fa fa-spinner fa-spin"></i>';
    msg +=  " "+$("#email_message").html();
    $("#notefier").html(msg).removeClass("alert-danger").removeClass("alert-success").addClass('alert-info').show();

  e.preventDefault();
    var data = JSON.parse(JSON.stringify($("#instance_form").serializeArray()));
    var args = {};
    $.each(data, function(index, obj) {
        args[obj['name']] = obj['value']
    });

    var code='0';
    //  args= { "name":args["username"],"email":args["email_doc"] ,'telephone':args["telephone_doc"],"pass":args["pass"],"recaptcha_response_field":args["g-recaptcha-response"]}
      //args= { "name":"fghgf","email":"ahmed@outlook.com" ,'telephone':"235","pass":"46","recaptcha_response_field":"4564"}
    args= { "name": args["username"] ,"email":args["email_doc"] ,'telephone':args["telephone_doc"]}
console.log(args);
 frappe.call({
        type: "POST",
        method: "erpstyle.appi.add_instance",
        args : args ,
        callback: function(r) {
     //   frappe.msgprint(r.message['message']);
            code = r.message['activation_code'];
            if(typeof r.message['status'] == "undefined" )
                $("#recaptcha_reload").click();
            else{
             /// $("#submit").css("display","none");
             $("#notefier").html(r.message['message']).show();


                return;
            }
           // $("#submit").css("display","none");
            $("#notefier").html(r.message).show();


        }
    });





});

