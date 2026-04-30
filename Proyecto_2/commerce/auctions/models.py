from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser): #Using "abstractUser" allows us to add custom fields without breaking the database
    pass

#ADVERTISEMENT TEMPLATE
class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    starting_price = models.DecimalField(max_digits=10, decimal_places=2) #Use DecimalField (so that the money is not float and thus avoid rounding problems)
    category = models.CharField(max_length=50, blank=True) #"blank=True" Indicates that the field is optional
    image_url = models.URLField(max_length=500, blank=True, null=True)

    #On_delete=models.CASCADE If you delete users, the program also deletes their listings
    #When we use related_name="listings", we are telling Django that when we are in a "user" object we refer to its listings as if they were listings, allowing us to distinguish between active and closed listings
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings") #"created_by" is a ForeignKey that connects the ad to a User; If you delete the user, their ads disappear (automatic cleanup)
    is_active = models.BooleanField(default=True) 

    def __str__(self): #"__str__" determines how the object appears in the Administration Panel
        return self.title

#BIDDING TEMPLATE 
#This model is an intermediary table that connects a user to an advertisement through a price
#In this case we use 2 foreign keys because we need to know which user placed the bid and on which item
class Bid(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids") #Gives you all the bids a person has made
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids") #It gives you the complete bidding history for a specific item

    def __str__(self):
        return f"{self.amount} by {self.user}"

#COMMENT TEMPLATE
class Comment(models.Model):
    text = models.TextField() #"TextField" does not have a strict character limit, allowing the user to elaborate on their comment

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments") #Match the comment to its author
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments") #Relate the comment to the specific ad

    def __str__(self):
        return f"Comment by {self.user} on {self.listing}"