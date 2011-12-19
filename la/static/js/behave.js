
jQuery(document).ready(function($) {

	$("#add-book").click(function() {
		var form_no = Number($("#id_form-TOTAL_FORMS").val());
		$("#checkout-form").append(
				$("#extra-form").html().replace(/__prefix__/g, form_no)
			);
		$("#id_form-TOTAL_FORMS").val(form_no + 1);
	});

	$('.autocomplete').autocomplete({
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
						label: item.fields.name,
						value: item.pk,
					}
				}));
			
			});
		}
	});
});
