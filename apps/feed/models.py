from django.db import models
from apps.feeder.models import SiteFeeder

class Feed(models.Model):
	site = models.ForeignKey(SiteFeeder, on_delete=models.CASCADE)
	timestamp = models.DateTimeField()
	title = models.CharField(max_length=150)
	description = models.TextField(blank=True)
	add_time = models.DateTimeField(auto_now_add=True)
	feed_url = models.URLField(null=True,blank=True)
	feed_image_url = models.URLField(null=True,blank=True)

	def __str__(self):
		return f"{self.site.name} {self.timestamp} {self.title}"