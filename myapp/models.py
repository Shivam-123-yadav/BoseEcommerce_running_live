from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.conf import settings
import math
from django.utils.text import slugify
import re
import uuid
# live
class User(AbstractUser):
    user_level=models.IntegerField(null=True,blank=True)
    status=models.CharField(max_length=25,null=True,blank=True)
    is_loggedin = models.BooleanField(default=False)
    assigned_to=models.CharField(max_length=100,null=True,blank=True)
    mobile = models.CharField(max_length=15,null=True,blank=True)
    email = models.CharField(max_length=100,null=True,blank=True,unique=True)
    address = models.TextField(null=True, blank=True)
    state=models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    otp = models.CharField(max_length=4, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)
    shadow_pass=models.CharField(max_length=100,null=True,blank=True)


    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

    def __str__(self):
        return self.user.username
    
    

class Dataupload(models.Model):
    listid=models.CharField(max_length=100,null=True,blank=True)
    listname=models.CharField(max_length=100,null=True,blank=True)
    file=models.FileField(upload_to='uploaded_csv/',blank=True,null=True)
    count = models.BigIntegerField(null=True,blank=True)
    entry=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    status=models.IntegerField(null=True,blank=True,default=1)
    data_count= models.BigIntegerField(null=True,blank=True)
    uploaded_by = models.CharField(max_length=100,null=True,blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='dataupload')



class ItemDetail(models.Model):
    class Category(models.TextChoices):
        REMOTE = 'remote', 'Remote Detail'
        CUSHION = 'cushion', 'Cushion Detail'
        STAYHEAR ='stayhear','StayHear Detail'
        POWER_SUPPLY = 'powersupply', 'Power Supply'
        CABLE = 'cable', 'Cable'
        CARRY_CASE = 'carrycase', 'Carry Case'
        ADAPTER = 'adapter', 'Adapter'
        OTHERS = 'others', 'Others'
        # for headphone category
        WIRELESS = 'wireless', 'Wireless'
        NOISECANCELLING = 'noisecancelling', 'Noise Cancelling'
        EARBUDS = 'earbuds', 'Earbuds'
        # for speakers category
        PORTABLE_BLUETOOTH = 'portablebluetooth', 'Portable Bluetooth'
        HOME_AUDIO = 'homeaudio', 'Home Audio'
        HOME_CINEMA = 'homecinema', 'Home Cinema'
        SOUND_BARS = 'soundbars', 'Sound Bars'
        STEREO = 'stereo', 'Stereo'
        COMPUTER_SPEAKER = 'computerspeaker', 'Computer Speaker'
        PORTABLE_PA = 'portablepa', 'Portable PA'

    title = models.CharField(max_length=100, null=True, blank=True)
    availability = models.CharField(max_length=100, null=True, blank=True)
    add_card = models.CharField(max_length=100, null=True, blank=True)
    mrp_price = models.DecimalField(max_digits=11, decimal_places=2,null=True,blank=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # New field for discount percentage
    discount_amount = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)  # New field for discount amount
    final_price = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)  # New field for final price
    slug = models.SlugField(max_length=255, unique=True, blank=True,null=True)

    image1 = models.ImageField(
        upload_to='ItemDetails/', 
        verbose_name='Image 1',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        null=True,
        blank=True,
        max_length=500 
    )

    image2 = models.ImageField(
        upload_to='ItemDetails/',
        verbose_name='Image 2',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        null=True,
        blank=True,
        max_length=500 
    )
    image3 = models.ImageField(
        upload_to='ItemDetails/',
        verbose_name='Image 3',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        null=True,
        blank=True,
        max_length=500 
    )
    image4 = models.ImageField(
        upload_to='ItemDetails/',
        verbose_name='Image 4',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        null=True,
        blank=True,
        max_length=500 
    )
    image5 = models.ImageField(
        upload_to='ItemDetails/',
        verbose_name='Image 5',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        null=True,
        blank=True,
        max_length=500 
    )


    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    dataupload = models.ForeignKey('Dataupload', on_delete=models.CASCADE, null=True, blank=True, related_name='item_details')
    category = models.CharField(max_length=100, choices=Category.choices)
    shipping_charges= models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
    box_content= models.TextField(null=True, blank=True)
    dimension_weight= models.TextField(null=True, blank=True)
    materials= models.CharField(max_length=1000, null=True, blank=True)
    battery= models.CharField(max_length=1000, null=True, blank=True)
    bluetooth= models.CharField(max_length=1000, null=True, blank=True)
    inputs= models.CharField(max_length=1000, null=True, blank=True)
    microphones= models.CharField(max_length=1000, null=True, blank=True)
    controls= models.CharField(max_length=1000, null=True, blank=True)
    compatible_app= models.TextField(null=True, blank=True)
    additions_informations= models.TextField(null=True, blank=True)
    heading1 = models.CharField(max_length=200,null=True,blank=True)
    heading2 = models.CharField(max_length=200,null=True,blank=True)
    heading3 = models.CharField(max_length=200,null=True,blank=True)
    heading4 = models.CharField(max_length=200,null=True,blank=True)
    heading5 = models.CharField(max_length=200,null=True,blank=True)
    heading6 = models.CharField(max_length=200,null=True,blank=True)
    overview = models.TextField(null=True, blank=True)
    compability = models.TextField(null=True, blank=True)


    class Meta:
        verbose_name = 'Item Detail'
        verbose_name_plural = 'Item Details'

    def __str__(self):
        return str(self.title) or 'Item Detail'
    
    # def save(self, *args, **kwargs):
    #     # Calculate discount amount and final price before saving
    #     if self.mrp_price is not None and self.discount_percentage is not None:
    #         self.discount_amount = (self.discount_percentage / 100) * self.mrp_price
    #         self.final_price = self.mrp_price - self.discount_amount
    #     else:
    #         self.discount_amount = 0  # Set to 0 if MRP or discount percentage is None
    #         self.final_price = self.mrp_price  # Final price is equal to MRP if no discount
    #     if self.shipping_charges:
    #         self.final_price += self.shipping_charges
    #     super().save(*args, **kwargs)



    def save(self, *args, **kwargs):
        if not self.slug:
            accessories_categories = ['remote', 'cushion','stayhear','powersupply', 'cable', 'carrycase', 'adapter','others','stayhear']
            headphone_categories = ['wireless','noisecancelling','earbuds']
            speaker_categories = ['portablebluetooth','homecinema','soundbars','stereo','computerspeaker','portablepa','homeaudio']

            
            if self.category in accessories_categories:
                # self.slug = slugify(f"accessories/{self.category}/{self.title}")
                self.slug = f"accessories/{slugify(self.category)}/{slugify(self.title)}"
            elif self.category in headphone_categories:
                # self.slug = slugify(f"headphones/{self.category}/{self.title}")
                self.slug = f"headphones/{slugify(self.category)}/{slugify(self.title)}"
            elif self.category in speaker_categories:
                # self.slug = slugify(f"speakers/{self.category}/{self.title}")
                self.slug = f"speakers/{slugify(self.category)}/{slugify(self.title)}"
            else:
                self.slug = f"{slugify(self.category)}/{slugify(self.title)}"
            
            
        if self.mrp_price is not None and self.discount_percentage is not None:
            if math.isnan(self.mrp_price) or math.isnan(self.discount_percentage):
                self.discount_amount = 0
                self.final_price = self.mrp_price if self.mrp_price is not None else 0
            else:
                self.discount_amount = (self.discount_percentage / 100) * self.mrp_price
                self.final_price = self.mrp_price - self.discount_amount
        else:
            self.discount_amount = 0
            self.final_price = self.mrp_price if self.mrp_price is not None else 0

        if self.shipping_charges is not None:
            if math.isnan(self.shipping_charges):
                self.shipping_charges = 0 
            self.final_price += self.shipping_charges

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class TypeColor(models.Model):
    product = models.ForeignKey(ItemDetail, on_delete=models.CASCADE, related_name='colors')
    color_name = models.CharField(max_length=50)
    image1 = models.ImageField(
        upload_to='color_images/', 
        verbose_name='Color Image 1',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        null=True,
        blank=True,
        max_length=500 
    )

    image2 = models.ImageField(
        upload_to='color_images/',
        verbose_name='Color Image 2',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        null=True,
        blank=True,
        max_length=500 
    )
    image3 = models.ImageField(
        upload_to='color_images/',
        verbose_name='Color Image 3',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        null=True,
        blank=True,
        max_length=500 
    )
    image4 = models.ImageField(
        upload_to='color_images/',
        verbose_name='Color Image 4',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        null=True,
        blank=True,
        max_length=500 
    )
    image5 = models.ImageField(
        upload_to='color_images/',
        verbose_name='Color Image 5',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        null=True,
        blank=True,
        max_length=500 
    )

    class Meta:
        verbose_name = 'Type Color'
        verbose_name_plural = 'Type Colors'
 

    def _str_(self):
        return f"{str(self.product.name)} - {self.color_name}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    

class UserDetails(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_details')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50,null=True,blank=True)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10)
    country = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'User Detail'
        verbose_name_plural = 'User Details'

    def __str__(self):
        return f"{self.first_name} {self.last_name}'s Details"




class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Cart"
    
    def total_cart_value(self):
        """Calculate the total value of items in the cart."""
        return sum(item.total_price for item in self.cart_items.all())




class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    item = models.ForeignKey(ItemDetail, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    type_color_image_url =models.CharField(max_length=200,null=True,blank=True)
    type_color_name = models.CharField(max_length=100,null=True,blank=True)
    

    def __str__(self):
        return f"{self.item.title} (x{self.quantity}) in Cart"

    @property
    def total_price(self):
        return self.quantity * self.item.final_price

    



class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING = 'pending', 'Pending'
        DELIVERED = 'delivered', 'Delivered'
        CANCELLED = 'cancelled', 'Cancelled'
        PAID = 'paid', 'Paid'
        USER_DROPPED = 'user_dropped', 'User Dropped'  # New status
        INCOMPLETE = 'incomplete', 'Incomplete' 

    order_id = models.CharField(max_length=255, unique=True,default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Associate order with a user
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Allow null and blank
    payment_status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('success', 'Success'), ('failed', 'Failed')], default='pending')
    payment_mode = models.CharField(max_length=50, blank=True, null=True)  # New field for payment mode
    reference_id = models.CharField(max_length=255, blank=True, null=True)  # New field for reference ID
    signature = models.TextField(blank=True, null=True)  # New field for signature
    transaction_time = models.DateTimeField(blank=True, null=True)  # New field for transaction time
    order_note = models.TextField(blank=True, null=True)  # Allow blank and null for order note
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    payment_link = models.URLField(blank=True, null=True)  # Allow blank and null for payment link
    status = models.CharField(max_length=50, choices=OrderStatus.choices, default=OrderStatus.PENDING)

    def __str__(self):
        return f"Order {self.order_id}"

    def calculate_total_amount(self):
        """Calculate and update the total amount for the order based on order items."""
        self.total_amount = sum(item.total_price() for item in self.order_items.all())
        self.save()




class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    item = models.ForeignKey(ItemDetail, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=11, decimal_places=2)
    type_color_name=models.CharField(max_length=200,null=True,blank=True)
    type_color_image_url=models.CharField(max_length=200,null=True,blank=True)

    def save(self, *args, **kwargs):
            # Check if final_price is not None
        if self.item.final_price is None:
            raise ValueError("Item final_price cannot be None.")

        # Calculate total price based on quantity and item price
        self.total_price = self.quantity * self.item.final_price
        super().save(*args, **kwargs)
    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'



class paymentStatus(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link payment to the user
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payment_details')  # One-to-one with Order
    order_item = models.ForeignKey('OrderItem', on_delete=models.CASCADE, related_name='payment_status', blank=True, null=True)  # New foreign key to OrderItem (optional)
    transaction_id = models.CharField(max_length=255, unique=True, blank=True, null=True)  # Transaction ID from gateway
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Payment amount
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')  # Payment status
    update_status=models.CharField(max_length=20,null=True,blank=True)
    customer_name = models.CharField(max_length=255, blank=True, null=True)  # Customer name
    customer_email = models.EmailField(blank=True, null=True)  # Customer email
    customer_phone = models.CharField(max_length=15, blank=True, null=True)  # Customer phone
    customer_address = models.TextField(blank=True, null=True)  # Customer address
    gateway_response = models.JSONField(blank=True, null=True)  # Store full response from payment gateway
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment for Order {self.order.order_id} - Status: {self.status}"


class Wishlist(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlists')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Wishlist'
        verbose_name_plural = 'Wishlists'
       

    def _str_(self):
        return f"{self.user.username}'s Wishlist"



class WishlistItems(models.Model):
    wish = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name="wish_items")
    item = models.ForeignKey(ItemDetail, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('wish', 'item')  # Ensure an item can only appear once in a user's wishlist

    def __str__(self):
        return f"{self.item.title} in Wishlist"   



class Review(models.Model):
    product = models.ForeignKey('ItemDetail', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_reviews')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    review_text = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

    def __str__(self):
        return f'Review by {self.name} for {self.product}'


    def total_likes(self):
        return self.likes.count()

    def total_dislikes(self):
        return self.dislikes.count()    



class LikeUnlike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='like_dislikes')
    liked = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'review') 

    def __str__(self):
        return f"{self.user.username} {'liked' if self.liked else 'disliked'} {self.review.title}"



# for online visit service center

class onsiteVisitServiceCenter(models.Model):
    order_id = models.CharField(max_length=255, unique=True,default=uuid.uuid4)
    device_name = models.CharField(max_length=100,null=True,blank=True) 
    issue_description = models.TextField(verbose_name="Issue Description", null=True, blank=True) 
    device_serial_number =models.CharField(max_length=100,verbose_name="Device Serial Number",null=True,blank=True) 
    service_center_name = models.CharField(max_length=255, verbose_name="Service Center Name") 
    customer_name = models.CharField(max_length=100,verbose_name="Customer Name",null=True,blank=True) 
    customer_email = models.CharField(max_length=100,null=True,blank=True) 
    customer_mobile = models.CharField(max_length=100,verbose_name="Customer Mobile Number",null=True,blank=True) 
    customer_address = models.TextField(verbose_name="Customer Address", null=True, blank=True) 
    visit_type = models.CharField(max_length=100,verbose_name="Visit Type",null=True,blank=True)
    visit_date = models.CharField(max_length=50,null=True,blank=True)
    time_slot = models.CharField(max_length=100,verbose_name="Time Slot",null=True,blank=True) 
    service_charge = models.CharField(max_length=100,verbose_name="Service Charge",null=True,blank=True) 

    payment_status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('paid', 'Paid'), ('failed', 'Failed'),('incomplete', 'Incomplete'),],default='pending')
    payment_mode = models.CharField(max_length=50, blank=True, null=True)  # New field for payment mode
    reference_id = models.CharField(max_length=255, blank=True, null=True)  # New field for reference ID
    signature = models.TextField(blank=True, null=True)  # New field for signature
    transaction_time = models.DateTimeField(blank=True, null=True)  # New field for transaction time

    order_note = models.TextField(null=True, blank=True)
    payment_link = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'device name {self.device_name}'
    

class paymentResponseOnline(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]

    visit_service_id = models.ForeignKey(onsiteVisitServiceCenter, on_delete=models.CASCADE, related_name='payment_details') 
    transaction_id = models.CharField(max_length=255, unique=True, blank=True, null=True,db_index=True)  
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=PAYMENT_STATUS_CHOICES, default='pending') 
    update_status = models.CharField(max_length=100, null=True, blank=True)
    customer_name = models.CharField(max_length=255, blank=True, null=True)
    customer_email = models.EmailField(blank=True, null=True) 
    customer_phone = models.CharField(max_length=15, blank=True, null=True)  
    customer_address = models.TextField(blank=True, null=True)  
    gateway_response = models.JSONField(blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment for Visit Service Center {self.visit_service_id} - Status: {self.status}"



class OffsiteServiceVisit(models.Model):
    device_name = models.CharField(max_length=100, null=True, blank=True)  # device (select device)
    issue_description = models.TextField(verbose_name="Issue Description", null=True, blank=True)  # Problem description
    device_serial_number = models.CharField(max_length=100, verbose_name="Device Serial Number", null=True, blank=True)  # problem (product serial number)
    service_center_name = models.CharField(max_length=255, verbose_name="Service Center Name")  # service center (select service)
    customer_name = models.CharField(max_length=100, verbose_name="Customer Name", null=True, blank=True)  # customer name
    customer_email = models.CharField(max_length=100, null=True, blank=True)  # customer email
    customer_mobile = models.CharField(max_length=100, verbose_name="Customer Mobile Number", null=True, blank=True)  # customer mobile number
    customer_address = models.TextField(verbose_name="Customer Address", null=True, blank=True)  # customer address
    visit_type = models.CharField(max_length=100, verbose_name="Visit Type", null=True, blank=True)  # customer select service visit
    visit_date = models.CharField(max_length=50,null=True,blank=True)
    time_slot = models.CharField(max_length=100, verbose_name="Time Slot", null=True, blank=True)  # customer select time slot
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Device Name: {self.device_name}'




class ManualDisabled(models.Model):
    device_name = models.CharField(max_length=100, null=True, blank=True)
    issue_description = models.TextField(null=True, blank=True)
    device_serial_number = models.CharField(max_length=100, null=True, blank=True)
    service_center_name = models.CharField(max_length=255,null=True, blank=True)
    customer_name = models.CharField(max_length=100, null=True, blank=True)
    customer_email = models.CharField(max_length=100, null=True, blank=True)
    customer_mobile = models.CharField(max_length=100, null=True, blank=True)
    customer_address = models.TextField(null=True, blank=True)
    visit_type = models.CharField(max_length=100, null=True, blank=True)
    visit_date = models.CharField(max_length=50, null=True, blank=True)
    time_slot = models.CharField(max_length=100, null=True, blank=True)
    payment_status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer_name or 'Unknown'} - {self.device_name or 'Device'} ({self.service_center_name})"
