
jQuery(document).ready(function($) {

	$("#add-book").click(function() {
		var form_no = Number($("#id_form-TOTAL_FORMS").val());
		$("#checkout-form").append(
				$("#extra-form").html().replace(/__prefix__/g, form_no)
			);
		$("#id_form-TOTAL_FORMS").val(form_no + 1);
	});

	var options = {

			minLength : 2,
			source : function(request, response) {

						var term = request.term;
						request.book = term;
						$.getJSON('autocomplete', {
							book : term 
						},
						function(data, status, xhr) {
							response( $.map(data, function(item) {
								return {
									label: item.fields.name + ' - ' + item.fields.isbn,
									value: item.fields.name,
									id: item.pk
								}
								}));

						});
					},
			select : function(event, ui) {

						 console.log(ui, $(this).next());
						 $(this).next().val(ui.item.id);
					 }
	};
	$('.autocomplete').live('keydown.autocomplete', function() {
		$(this).autocomplete(options);
	});

	$('.extrauserfield').load(function() {
		$(this).val($("#id_form-0-user").val());
	});

	$("#id_form-0-user").change( function() {
		$('.extrauserfield').val($(this).val());
	});
});
