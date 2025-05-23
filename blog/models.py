from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.db.models.signals import post_save
from django.dispatch import receiver

class CryptoUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    total_invested = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    total_profit = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    
    # Fix the table name clash
    class Meta:
        db_table = 'blog_cryptouser'
        
    # Fix the related_name clashes
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='crypto_user_set',
        related_query_name='crypto_user'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='crypto_user_set',
        related_query_name='crypto_user'
    )

class Category(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    author = models.ForeignKey(CryptoUser, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(upload_to="blog_images/", null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField("Category", related_name="posts")

    def __str__(self):
        return self.title

class Comment(models.Model):
    author = models.CharField(max_length=60)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.author} on '{self.post}'"

class Transaction(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ]
    
    PAYMENT_METHODS = [
        ('bitcoin', 'Bitcoin'),
        ('ethereum', 'Ethereum'),
        ('usdt', 'USDT'),
        ('bank', 'Bank Transfer')
    ]

    # Update this line to use your custom user model
    user = models.ForeignKey('CryptoUser', on_delete=models.CASCADE)
    plan_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    wallet_address = models.CharField(max_length=255, blank=True)
    transaction_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    return_rate = models.DecimalField(max_digits=5, decimal_places=2)
    expected_return = models.DecimalField(max_digits=10, decimal_places=2)
    completion_date = models.DateField(null=True, blank=True)
    
    class Meta:
        ordering = ['-transaction_date']

class Balance(models.Model):
    user = models.OneToOneField('CryptoUser', on_delete=models.CASCADE, related_name='account_balance')
    amount = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Balance: ${self.amount}"

@receiver(post_save, sender=CryptoUser)  # Use your actual CryptoUser model class here.
def create_user_balance(sender, instance, created, **kwargs):
    if created:
        Balance.objects.create(user=instance)

@receiver(post_save, sender=CryptoUser)
def save_user_balance(sender, instance, **kwargs):
    # Optionally ensure the balance object exists
    if not hasattr(instance, 'account_balance'):
        Balance.objects.create(user=instance)

