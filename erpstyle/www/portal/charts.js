$('form').on('submit',function (e) {
        e.preventDefault();
        $('.modal-loader').show();
        $form = $(this);
        var data = JSON.parse(JSON.stringify($form.serializeArray()));
        // debugger;
        var args = {};
        $.each(data, function (index, obj) {
            args[obj['name']] = obj['value'];
        });
        args['chart_type'] = $("#chart_type").val();
        frappe.call({
            type: "POST",
            method: "erpstyle.www.portal.charts.get_data",
            args: args,
            callback: function (r) {
                $('#totals').html("");
                if(r.message){
                    $('#msg').addClass('hidden');
                    totals(r.message)

                }else{
                    $('#msg').removeClass('hidden');
                }
                $('.modal-loader').hide();

            }
        });
    });//submit


function totals(data){
    var html = "";
    var dic = {
        'Absent' : 'الغياب',
        'Present': 'الحضور',
        'Internal': 'داخلي',
        'Count': 'العدد',
        'External': 'خارجي'
    };
    $.each(data , function(key , value){

        html += " <b>"+ key +"</b> <br/>";
        html += '<table class="table table-striped table-bordered table-hover table-condensed">'
        for(var i = 0 ; i < value.length; i++){
            html+="<tr>"
            html+="<th>"+(dic[value[i][1]]!=undefined ? dic[value[i][1]]:value[i][1])+"</th>";
            html+="<td>"+value[i][0]+"</td>";
            html+="</tr>"
        }
        html += "</table>"

    });
   $('#totals').html(html);
}