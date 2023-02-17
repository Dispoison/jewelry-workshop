from django.db import models


class BaseTimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class JewelryType(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        db_table = "workshop_jewelry_type"

    def __str__(self):
        return self.name


class Material(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Gem(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Jewelry(BaseTimestampedModel):
    name = models.CharField(max_length=128)
    weight = models.FloatField()
    price = models.FloatField()
    type = models.ForeignKey(JewelryType, null=True, on_delete=models.SET_NULL)
    materials = models.ManyToManyField(Material)
    gems = models.ManyToManyField(Gem)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', null=True, verbose_name='Зображення')

    def __str__(self):
        return self.name


class Client(BaseTimestampedModel):
    name = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=16)
    email = models.EmailField()

    def __str__(self):
        return f"Name: {self.name}. Email: {self.email}"


class Order(BaseTimestampedModel):
    quantity = models.IntegerField()
    jewelry = models.ForeignKey(Jewelry, null=True, on_delete=models.SET_NULL)
    client = models.ForeignKey(Client, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Order: {self.id}. Product name: {self.jewelry.name}. Quantity: {self.quantity}"
