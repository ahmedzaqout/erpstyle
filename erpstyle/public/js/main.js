jQuery( document ).ready(function( $ ) {
"use strict"
/*-----------------------------------------------------------------------------------*/
/*		STICKY NAVIGATION
/*-----------------------------------------------------------------------------------*/
$(".sticky").sticky({topSpacing:0});
/*-----------------------------------------------------------------------------------*/
/* 	LOADER
/*-----------------------------------------------------------------------------------*/
$("#loader").delay(500).fadeOut("slow");
/*-----------------------------------------------------------------------------------
    TESTNMONIALS STYLE 1
/*-----------------------------------------------------------------------------------*/
$('#carousel').flexslider({
    animation: "slide",
    controlNav: false,
    animationLoop: false,
    slideshow: false,
    itemWidth: 122,
    itemMargin: 5,
    asNavFor: '#slider'
});
$('#slider').flexslider({
    animation: "fade",
    controlNav: false,
    animationLoop: false,
    slideshow: false,
    sync: "#carousel"
  });


$('.testi-slides-flex').flexslider({
   animation: "slide"
});

/*-----------------------------------------------------------------------------------*/
/* 	SLIDER REVOLUTION
/*-----------------------------------------------------------------------------------*/
jQuery('.tp-banner-fix').show().revolution({
	dottedOverlay:"none",
	delay:10000,
	startwidth:1170,
	startheight:670,
	navigationType:"bullet",
	navigationArrows:"solo",
	navigationStyle:"preview4",
	parallax:"mouse",
	parallaxBgFreeze:"on",
	parallaxLevels:[7,4,3,2,5,4,3,2,1,0],
	keyboardNavigation:"on",
	fullWidth:"off",
	fullScreen:"off"
});
/*-----------------------------------------------------------------------------------*/
/*	ISOTOPE PORTFOLIO
/*-----------------------------------------------------------------------------------*/
var $container = $('.port-wrap .items');
    $container.imagesLoaded(function () {
    $container.isotope({
    itemSelector: '.portfolio-item',
    layoutMode: 'masonry'
});
});
$('.portfolio-filter li a').on('click', function () {
    $('.portfolio-filter li a').removeClass('active');
    $(this).addClass('active');
    var selector = $(this).attr('data-filter');
    $container.isotope({
      filter: selector
    });
return false;
});
/*-----------------------------------------------------------------------------------*/
/* 	SINGLE SLIDE
/*-----------------------------------------------------------------------------------*/
$(".single-slides").owlCarousel({
    items : 1,
	autoplay:false,
	autoplayHoverPause:true,
	singleItem	: true,
	navText: ["<i class='fa fa-angle-left'></i>","<i class='fa fa-angle-left'></i>"],
	lazyLoad:true,
	nav: true,
	loop: true,
	animateOut: 'fadeOut'
});
});

/*-----------------------------------------------------------------------------------*/
/*    CONTACT FORM
/*-----------------------------------------------------------------------------------*/
function checkmail(input){
  var pattern1=/^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;
  	if(pattern1.test(input)){ return true; }else{ return false; }}
    function proceed(){
    	var name = document.getElementById("name");
		var email = document.getElementById("email");
		var company = document.getElementById("company");
		var web = document.getElementById("website");
		var msg = document.getElementById("message");
		var errors = "";
		if(name.value == ""){
		name.className = 'error';
	  	  return false;}
		  else if(email.value == ""){
		  email.className = 'error';
		  return false;}
		    else if(checkmail(email.value)==false){
		        alert('Please provide a valid email address.');
		        return false;}
		    else if(company.value == ""){
		        company.className = 'error';
		        return false;}
		   else if(web.value == ""){
		        web.className = 'error';
		        return false;}
		   else if(msg.value == ""){
		        msg.className = 'error';
		        return false;}
		   else
		  {
	$.ajax({
		type: "POST",
		url: "php/submit.php",
		data: $("#contact_form").serialize(),
		success: function(msg){
		//alert(msg);
		if(msg){
			$('#contact_form').fadeOut(1000);
			$('#contact_message').fadeIn(1000);
				document.getElementById("contact_message");
			 return true;
		}}
	});
}};



$("#lead_form").submit(function(e){
  e.preventDefault();
  return frappe.call({
    type: "POST",
    method: "erpstyle.mail_data.api.add_Issue",
    args: {
      user_name: $("#user_name").val(),
      raised_by_email_id:$("#raised_by_email_id").val(),
      user_phone:$("#user_phone").val(),
      subject:$("#subject").val(),
      description:$("#description").val(),
      category:$("#Lead-category").val(),
      priority:$("#Lead-priority").val()
    }
    ,
    callback: function(r) {
      if(!r.exc && r.message) {
        console.log(r.message);
        $('#myModal').modal('toggle');
       $("#user_name").val("");
        $("#raised_by_email_id").val("");
        $("#user_phone").val("");
        $("#subject").val("");
        $("#description").val("");
      }
    }

  });
});



$("#lead_form_login").submit(function(e){
  e.preventDefault();
  return frappe.call({
    type: "POST",
    method: "erpstyle.mail_data.api.add_lead_login",
    args: {
      lead_name: $("#lead_name").val(),
      email_id:$("#email_id").val(),
      company_name:$("#company_name").val()
    }
    ,
    callback: function(r) {
      if(!r.exc && r.message) {
        console.log(r.message);
      }
    }
  });

});
$("#mail_list").submit(function(e){
  e.preventDefault();
  return frappe.call({
    type: "POST",
    method: "erpstyle.mail_data.api.add_mail",
    args: {
      email:$("#email_list").val()
    }
    ,
    callback: function(r) {
      if(!r.exc && r.message) {
        console.log(r.message);
        $('#myModal').modal('toggle');
      }
    }
  });

});

$('.ownmenu li').click(function(){
    $('.ownmenu li').removeClass('active');
    $(this).addClass('active');
})

$( "#try_now" ).click(function(e) {
  e.preventDefault();
  var args1 = {};
  args1.cmd = "login";
  args1.usr = "user@erpdevelopers.com";
  args1.pwd = "1";
  args1.device = "desktop";

  return frappe.call({
    type: "POST",
    method: "login",
    args:args1
    ,
    callback: function(r) {
      if(!r.exc && r.message) {
        window.location = "/desk";

      }
    }

  });
});
//jQuery to collapse the navbar on scroll
$(window).scroll(function() {
});
//jQuery for page scrolling feature - requires jQuery Easing plugin
$(function() {
    $('a.page-scroll').bind('click', function(event) {
        var $anchor = $(this);
        $('html, body').stop().animate({
            scrollTop: $($anchor.attr('href')).offset().top
        }, 1500, 'easeInOutExpo');
        event.preventDefault();
    });

if($('[name="doctype"]').val() == "Correspondence"){
	var _form = $('[name="doctype"]').parent('form');


	_form.find('#department').on('change' , function(e){
		console.log(e);
		getEmployees($(this).val() , function(data){
				if( data.message ){
					console.log(data.message);
					options = ""
					$.each(data.message , function(i , v){
						console.log(i , v);
						options += '<option value="'+v.name+'" > '+v.employee_name+' </option>'
					});

					_form.find('#employee_to').html(options)

				}else{
					_form.find('#employee_to').html("")
				}
			})
	});

}
});

var files = [];
$(document).ready(function(){
if($('[name="doctype"]').val() == "Correspondence"){
	var _form = $('[name="doctype"]').parent('form');
	_form.find("#department").trigger('change');
	_form.append('<label class="btn btn-primary custom-file_upload" aria-label="right Align"><input type="file" name="files" multiple/><span class="glyphicon glyphicon-plus" aria-hidden="true"> ارفق ملفات </span></label>')
	_form.append('<table class="table table-bordered table-striped" id="attaches"></table>')


	// Variable to store your files


	// Add events
	$('input[type=file]').on('change', prepareUpload);
	$(document).on('click', '#attaches .close', removeAttachedFile);

	// Grab the files and set them to our variable
	function prepareUpload(event){
		fileList = event.target.files;
		$.each(fileList, function(key, value){
			files.push(value);
		});
		//data = new FormData();
		showAttachedFiles();
	}

	function showAttachedFiles(){
		$("#attaches").empty();
		$.each(files, function(key, value)
		{
			$("#attaches").append('<tr data-index='+key+'><td>'+(key+1)+'</td><td>'+value.name+'</td><td><button type="button" class="close btn btn-danger" style=" font-size: 15px;font-family: sans-serif">x</button></td><td id="b64'+key+'"></td></tr>');
		});
	}

	function removeAttachedFile(event){
		var $tr = $(this).closest('tr');
		var index = $tr.attr('data-index');
		var $input = $('input[type=file]');
		var filedata = $input.prop('filedata');
		//debugger;
		files.splice( index, 1 );
		filedata.splice( index, 1 );
		//input.filedata =  || [];
		showAttachedFiles();
	}


}
});
var handleFileSelect = function(evt) {
    var files = evt.target.files;
    var file = files[0];

    if (files && file) {
        var reader = new FileReader();

        reader.onload = function(readerEvt) {
            var binaryString = readerEvt.target.result;
            document.getElementById("base64textarea").value = btoa(binaryString);
        };

        reader.readAsBinaryString(file);
    }
};
var getEmployees = function(department , callbackFunction){

    frappe.call({
		type: "GET",
		method: "erpstyle.api.getEmployeesByDepartment",
		args: {
		  department: department
		},
		callback: function(data) {
			callbackFunction(data)
		}
	});
}





function logout() {
    return frappe.call({
        method: 'logout',
        callback: function (r) {
            if (r.exc) {
                console.log(r.exc);
                return;
            }
            redirect_to_login();
        }
    })
}
function redirect_to_login() {
    window.location.href = '/';
}
