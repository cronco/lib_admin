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
	
@register.filter
def neighborhood(iterable):
	iterator = iter(iterable)
	prev = None
	item = iterator.next()  # throws StopIteration if empty.
	for next in iterator:
		yield (prev,item,next)
		prev = item
		item = next
	yield (prev,item,None)   
