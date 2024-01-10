from dal import autocomplete
from django.db.models import Q
from main.models import State,Country

class StateAutocomplete(autocomplete.Select2QuerySetView):
	def get_queryset(self):
		country = self.forwarded.get('country', None)
		if country:
			country_instance = Country.objects.get(id=country)
			items = State.objects.filter(country=country_instance)

		else:
			items = State.objects.all()
		# if items:
		if self.q:
			items = items.filter(Q(name__icontains=self.q))
		return items
		# else:
		# 	return []