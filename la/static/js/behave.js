
jQuery(document).ready(function($) {

	$('#add-book').click(function() {
		var form_no = Number($("#id_form-TOTAL_FORMS").val());
		$("#checkout-form").append(
				$("#extra-form").html().replace(/__prefix__/g, form_no)
			);
		$("#id_form-TOTAL_FORMS").val(form_no + 1);
	});

	var options = {

			minLength : 2,
			select : function(event, ui) {
							 $(this).next().val(ui.item.id);
					 }
		};
	

	$('.autocomplete').live('keydown.autocomplete', function() {
	
		var that = this;
		var autocomplete_source = function(request, response) {
			var term = request.term,
				term_name = $(that).data('search'),
				role = $(that).data('role');
				search_object = {};
				// role needed to see what we're searching for exactly
				if(role) {
					search_object[role] = 1;
				}
				if(term_name == 'book')
					search_object['user_id'] = $("#id_form-0-user_1").val();
				search_object[term_name] = term;
				$.getJSON('autocomplete', search_object,
					function(data, status, xhr) {
						response( $.map(data, function(item) {
							if (term_name == 'book') {
								return {
									label: item.fields.name + ' - ' + item.fields.isbn,
									value: item.fields.name,
									id: item.pk
									}
							} else if(term_name == 'user') {
							
								return {
									label : item.fields.last_name + ' ' + item.fields.first_name + ' - ' + item.fields.email,
									value: item.fields.last_name + ' ' + item.fields.first_name,
									id: item.pk
								}
							}
							}));
				});

		};


		$(this).autocomplete(options);
		$(this).autocomplete("option", 'source', autocomplete_source);

		if($(this).hasClass('checkin-user')) {

			$(this).autocomplete("option",  'select', function(event, ui) {

				$(this).next().val(ui.item.id);
				$.get('autocomplete',{
					  user_id : ui.item.id,
					 checkouts: 1
				 }, function(data, status, req) {
						$("#added-forms").html(data);
						$("#added-forms .autohidden").addClass("hidden");
				 });
			});
		}
	
	});

	$(".extrauserfield").load(function() {
		$(this).val($("#id_form-0-user").val());
	});

	$("#id_form-0-user").change(function() {
		$(".extrauserfield").val($(this).val());
	});

	$("body").delegate(".autohide-label", "click", (function() {
		var field = $(this).attr("for");
		
		$("#" + field).toggleClass("hidden");

	}));


});
