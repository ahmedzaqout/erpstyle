// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// MIT License. See license.txt


frappe.require([
    "/assets/erpstyle/js/vendors/jquery.calendars/jquery.calendars.picker11.css",
    "/assets/erpstyle/js/vendors/jquery.calendars/jquery.plugin.js",
    "/assets/erpstyle/js/vendors/jquery.calendars/jquery.calendars.all.js",
    "/assets/erpstyle/js/vendors/jquery.calendars/jquery.calendars.islamic.js",
    "/assets/erpstyle/js/vendors/Hijri.js"], function () {

    console.log('Hijri loaded');
});


frappe.ui.form.ControlDate.prototype.get_calendar_type = function () {
    // return Gregorian or Hijri
    return this.df.calendar_type || 'Gregorian';
}
frappe.ui.form.ControlDate.prototype.is_gregorian = function () {
    return this.get_calendar_type() == 'Gregorian';
}
frappe.ui.form.ControlDate.prototype.make_input = function () {
    if (this.is_gregorian()) {
        if(this.$input) return;

		this.$input = $("<"+ this.html_element +">")
			.attr("type", this.input_type)
			.attr("autocomplete", "off")
			.addClass("input-with-feedback form-control")
			.prependTo(this.input_area)

		if (in_list(['Data', 'Link', 'Dynamic Link', 'Password', 'Select', 'Read Only', 'Attach', 'Attach Image'],
			this.df.fieldtype)) {
				this.$input.attr("maxlength", this.df.length || 140);
		}

		this.set_input_attributes();
		this.input = this.$input.get(0);
		this.has_input = true;
		this.bind_change_event();
		this.bind_focusout();
    }
    else {
        // this.df.calendar_type
        this.$view_input = $("<input type='text' class='input-for-view form-control'>")
            .prependTo(this.input_area)

        this.$input = $("<input type='hidden' class='input-with-feedback'>")
            .prependTo(this.input_area)

        this.set_input_attributes();
        this.input = this.$input.get(0);
        this.has_input = true;
        this.bind_change_event();
        this.bind_focusout();
    }
    this.set_t_for_today();
    this.set_datepicker();
}
frappe.ui.form.ControlDate.prototype.set_datepicker = function () {
    if (this.is_gregorian()) {
        this.datepicker_options.dateFormat =
            (frappe.boot.sysdefaults.date_format || 'yyyy-mm-dd').replace("yyyy", "yy")
        this.$input.datepicker(this.datepicker_options);
    }
    else {
//			import_calendarspickers();
        var calendar = $.calendars.instance('Islamic');
        var me = this;
        this.$view_input.calendarsPicker({
            calendar: calendar, dateFormat: 'dd-mm-yyyy', onSelect: function (dates) {
                var date = new Date(dates[0].toJSDate())
                // debugger;
                var date_str = moment(date).format("DD-MM-YYYY");
                // debugger;
                me.$input.val(date_str);
                me.$input.trigger("change");
            }
        });
    }
}
frappe.ui.form.ControlDate.prototype.get_formatted_hijri = function (value) {
    var date = new Date(value);
    var islamicCalendars = new $.calendars.calendars.islamic();
    var jsDate = islamicCalendars.fromJSDate(date);
    return this.pad_number(jsDate.day()) + '-' + this.pad_number(jsDate.month()) + '-' + jsDate.year();

}
frappe.ui.form.ControlDate.prototype.set_input = function (value) {
    if (value) {
        this.value = value;
        this.$input && this.$input.val(this.format_for_input(value));
        this.set_disp_area();
        this.last_value = value;
        this.set_mandatory && this.set_mandatory(value);

        //var hijri = H(val, {type:'object'});
        // var hijri_date = new Date(hijri.y, hijri.m, hijri.d);
        if (!this.is_gregorian()) {
            this.$view_input.val(this.get_formatted_hijri(value));
        }
    }

}

frappe.ui.form.ControlDate.prototype.set_disp_area = function () {
    // console.log(this.value);
    if (!this.is_gregorian()) {
        this.disp_area && $(this.disp_area)
            .html(this.get_formatted_hijri(this.value));
        return;
    }
    this.disp_area && $(this.disp_area)
        .html(frappe.format(this.value || this.get_value(), this.df, {no_icon: true, inline: true},
            this.doc || (this.frm && this.frm.doc)));
}


frappe.ui.form.ControlDate.prototype.pad_number = function (number) {
    return number > 9 ? number : '0' + number;
}


frappe.ui.form.ControlDateHijri2 = frappe.ui.form.ControlData.extend({
    make_input: function () {
        this.$input = $("<input type='text' class='input-for-view form-control'>")
            .prependTo(this.input_area)

        this.set_input_attributes();
        this.input = this.$input.get(0);
        this.has_input = true;
        this.bind_change_event();
        this.bind_focusout();
        this.set_t_for_today();
        this.set_datepicker();
    },
    set_datepicker: function () {
//			import_calendarspickers();
        var calendar = $.calendars.instance('Islamic');
        var me = this;
        this.$input.calendarsPicker({
            calendar: calendar, dateFormat: 'dd-mm-yyyy', onSelect: function (dates) {
                var date = new Date(dates[0].toJSDate());
                var date_str = moment(date).format("DD-MM-YYYY");
                // debugger;
                me.$input.val(dates[0]);
                me.$input.trigger("change");
            }
        });
    },
    set_input: function (value) {
        if (value) {
            this._super(value);
            var date = new Date(value);
            var islamicCalendars = new $.calendars.calendars.islamic();
            var jsDate = islamicCalendars.fromJSDate(date);
            //	this.$view_input.val(this.pad_number(jsDate.day()) + '-' + this.pad_number(jsDate.month()) + '-' + jsDate.year());
        }

    },
    parse: function (value) {
        if (value) {
            value = value.toString();
        }
        return value;
    },
    pad_number: function (number) {
        return number > 9 ? number : '0' + number;
    }
});

// else{
//
// 	import_calendarspickers();
// 	var calendar = $.calendars.instance('Islamic');
// 	var me = this;
// 	this.$view_input.calendarsPicker({calendar: calendar, dateFormat: 'dd-mm-yyyy', onSelect: function (dates) {
// 		frappe.call({
// 			type: "GET",
// 			// apps/erpnext/erpnext.setup.doctype.global_defaults.global_defaults.py
// 			method: "erpnext.setup.doctype.global_defaults.global_defaults.get_hijri_fix",
// 			callback: function(r) {
// 				alert(r.message);
// 				var date = new Date(dates[0].toJSDate());
// 				alert(date);
// 				date.setDate(date.getDate() + parseInt(r.message));
// 				var date_str = moment(date).format("DD-MM-YYYY");
// 				alert(date);
// 				// debugger;
// 				me.$input.val(date_str);
// 				me.$input.trigger("change");
// 			}
// 		});
// 	}});
// }


// $(document).on('DOMNodeInserted', 'div.frappe-control[data-fieldtype="Date"][data-fieldname*="hijri"]', function (event) {
//     console.log($(this).html().trim());
//     $controlValue = $(this).find('.control-value');
//     console.log( $controlValue.text() );
//     if ($controlValue.text()) {
//         var strDate = $controlValue.text().split("-");
//         var date = new Date(strDate[2], strDate[1], strDate[0]);
//         var islamicCalendars = new $.calendars.calendars.islamic();
//         var jsDate = islamicCalendars.fromJSDate(date);
//         $controlValue.text(pad_number(jsDate.day()) + '-' + pad_number(jsDate.month()) + '-' + jsDate.year());
//     }
//
// });
function pad_number(number) {
    return number > 9 ? number : '0' + number;
}
