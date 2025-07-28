from django.db import models

# Create your models here.

from django.db import models

class ProdMast(models.Model):  # Product Master
    prod_name = models.CharField(max_length=255)
    sku = models.CharField(max_length=100, unique=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)  

    def __str__(self):
        return f"{self.prod_name} ({self.sku})"


class StckMain(models.Model):  # Transaction Header
    transaction_type = models.CharField(
        max_length=50,
        choices=[('In', 'Stock In'), ('Out', 'Stock Out')]
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    reference_number = models.CharField(max_length=100, unique=True, null=True, blank=True)
    notes = models.TextField(blank=True)
    created_by = models.CharField(max_length=100,default='admin')

    def __str__(self):
        return f"{self.transaction_type} - {self.reference_number}"


class StckDetail(models.Model):  # Transaction Line Items
    transaction = models.ForeignKey(StckMain, on_delete=models.CASCADE, related_name="details")
    product = models.ForeignKey(ProdMast, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.prod_name} x {self.quantity} ({self.transaction.reference_number})"


         