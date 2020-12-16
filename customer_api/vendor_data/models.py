from django.db import models

# Create your models here.
#Customer is main object from POST JSON data
class Customer(models.Model):
    #Id will be the primary key for this table
    id = models.CharField(max_length=200, primary_key=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    address_1 = models.CharField(max_length=200)
    address_2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=20)
    postal_code = models.CharField(max_length=20)

class Subscription(models.Model):
    #Assuming all subscriptions aren't separated by product
    #Won't have 1: ID A, Digital; 2: ID A, Print --> Will be 1: ID A, Digital and Print
    id = models.CharField(max_length=200, primary_key=True)

    plan_name = models.CharField(max_length=200)

    #Price will be int since it's in pennies
    price = models.IntegerField()

class Gifts(models.Model):
    id = models.CharField(max_length=200, default="", primary_key=True)

    plan_name = models.CharField(max_length=200)

    #Price will be int since it's in pennies
    price = models.IntegerField()

    recipient_email = models.CharField(max_length=200)




    

