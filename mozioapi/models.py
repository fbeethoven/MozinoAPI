from django.contrib.gis.db import models




class provider(models.Model):
    name = models.CharField(max_length = 50)
    email = models.EmailField(max_length = 150)
    phone_number = models.CharField(max_length = 50)
    language  = models.CharField(max_length = 50)
    currency = models.CharField(max_length = 10)

    def __str__(self):
        return self.name

class area(models.Model):
    name = models.CharField(max_length = 50)
    price = models.DecimalField(max_digits = 7, decimal_places = 2)
    provider = models.ForeignKey(provider, on_delete=models.CASCADE, related_name="provider", null=False)

    # The Polygon will be a geoField
    service_area = models.PolygonField()

    def __str__(self):
        return self.name



