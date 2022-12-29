from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

# Categoria de alguna subasta
class Categories(models.Model):
    categoryName = models.CharField(max_length=64)
    def __str__(self):
        return(f"{self.categoryName}")

# Acciones realizada por usuarios

# Para crear subastas 
class Auctions(models.Model):
    # Informacion del item a subastar
    titleItem = models.CharField(max_length=64)
    descriptionItem = models.CharField(max_length=254)
    imageItem = models.CharField(max_length=500)
    # Informacion de la subasta
    priceAuction = models.IntegerField()
    auctionStarted = models.DateTimeField(auto_now_add=True)
    isActiveAuction = models.BooleanField(default=True)

    categoryAuction = models.ForeignKey(Categories, on_delete=models.CASCADE)
    userAuction = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return(f"Auction{self.id}: {self.titleItem} is being auctioned by {self.userAuction}")

# Los comentarios que dejan los usuarios en la subasta
class Comments(models.Model):
    comment = models.CharField(max_length=500)
    commentPosted = models.DateTimeField(auto_now_add=True)
    userComment = models.ForeignKey(User,on_delete=models.CASCADE)
    auctionComment = models.ForeignKey(Auctions, on_delete=models.CASCADE)
    def __str__(self):
        return(f"Comment {self.id} made by {self.userComment.username} in the auction {self.auctionComment.titleItem}")
    
# Para realizar la apuesta a una subasta
class Bid(models.Model):
    bidPrice = models.IntegerField()
    bidDate = models.DateTimeField(auto_now_add=True)
    userBid = models.ForeignKey(User, on_delete=models.CASCADE)
    auctionBid = models.ForeignKey(Auctions, on_delete=models.CASCADE)
    def __str__(self):
        return(f"Bid {self.id} made by {self.userBid.username} in the auction {self.auctionBid.titleItem}")
    
# Para guardar alguna oferta en la lista de deseos
class Watchlist(models.Model):
    userWatchlist = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userWatchlist")
    auctionWatchlist = models.ForeignKey(Auctions, on_delete=models.CASCADE)
    def __str__(self):
        return(f"{self.userWatchlist.username} add {self.auctionWatchlist.titleItem} to his watchlist")

