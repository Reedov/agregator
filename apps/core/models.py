from django.db import models

class SiteSetting(models.Model):
	key = models.CharField(max_length=50)
	value = models.CharField(max_length=50, blank=True)

	def __str__(self):
		return f"{self.key} - {self.value}"
