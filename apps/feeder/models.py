from django.db import models

class SiteFeeder(models.Model):
    class Meta:
        verbose_name_plural = "Сайты"

    SMALL_PERIOD = "SMALL_PERIOD"
    MIDDLE_PERIOD = "MIDDLE_PERIOD"
    BIG_PERIOD = "BIG_PERIOD"

    CHOICES_PERIOD = (
        (SMALL_PERIOD,'small period - 20 sec'),
        (MIDDLE_PERIOD,'middle period - 1min'),
        (BIG_PERIOD,'big period - 5 min'),
        )

    name = models.CharField(max_length=100)
    url = models.URLField(null=True)
    active = models.BooleanField(default=True,null=True)
    icon = models.ImageField(null=True,blank=True,verbose_name="Иконка")
    feedscount = models.PositiveSmallIntegerField(null=True,verbose_name="Парсить фидов")
    scan_period = models.CharField(null=True,max_length=50,choices=CHOICES_PERIOD,default=MIDDLE_PERIOD)

    def __str__(self):
        return f"{self.id}. {self.name}"

