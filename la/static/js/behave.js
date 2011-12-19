
jQuery(document).ready(function($) {

	$("#add-book").click(function() {
		var form_no = Number($("#id_form-TOTAL_FORMS").val());
		$("#checkout-form").append(
				$("#extra-form").html().replace('__prefix__', form_no)
			);
		$("#id_form-TOTAL_FORMS").val(form_no + 1);
	});
});
