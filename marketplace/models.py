from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# ============================================================
# USER PROFILE
# ============================================================

class UserProfile(models.Model):

    USER_TYPES = [
        ("farmer", "Farmer"),
        ("buyer", "Buyer"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    role = models.CharField(
        max_length=10,
        choices=USER_TYPES
    )

    phone = models.CharField(
        max_length=15,
        blank=True
    )

    address = models.TextField(
        blank=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.role}"


# ============================================================
# CROP
# ============================================================

class Crop(models.Model):

    farmer = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    name = models.CharField(
        max_length=100
    )

    variety = models.CharField(
        max_length=100
    )

    quantity = models.FloatField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    image = models.ImageField(
        upload_to="crop_pics/",
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.name} ({self.farmer.username})"


# ============================================================
# CONTRACT / OFFER
# ============================================================

class Contract(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    ]

    farmer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="farmer_contracts"
    )

    buyer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="buyer_contracts"
    )

    crop = models.ForeignKey(
        Crop,
        on_delete=models.CASCADE
    )

    offered_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.crop.name} - {self.status}"


# ============================================================
# MESSAGE / CHAT
# ============================================================

class Message(models.Model):

    contract = models.ForeignKey(
        Contract,
        on_delete=models.CASCADE
    )

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    text = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.sender.username}: {self.text[:20]}"


# ============================================================
# SIGNALS
# ============================================================

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Automatically create a UserProfile whenever
    a new Django User is created.
    """

    if created:
        UserProfile.objects.get_or_create(
            user=instance,
            defaults={
                "role": "farmer"
            }
        )


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Automatically save the UserProfile whenever
    the related User is saved.
    """

    if hasattr(instance, "userprofile"):
        instance.userprofile.save()