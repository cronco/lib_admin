
jQuery(document).ready(function($) {

	$("#add-book").click(function() {
		var form_no = Number($("#id_form-TOTAL_FORMS").val());
		$("#checkout-form").append(
				$("#extra-form").html().replace(/__prefix__/g, form_no)
			);
		$("#id_form-TOTAL_FORMS").val(form_no + 1);
	});

	$('.autocomplete').change(function() {

		$.get('autocomplete', {
			book:	$(this).val()
				}, 
			function (data, textStatus, req) {
				console.log(req);
			});
	});
});
