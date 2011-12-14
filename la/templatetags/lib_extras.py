from django import template

register = template.Library()

@register.inclusion_tag("paginate.html")
def paginate(pages, page, request, context = ""):
	return {
			'request' : request,
			'context' :context,
			'pages' : pages,
			'page' : page,
			}
	
