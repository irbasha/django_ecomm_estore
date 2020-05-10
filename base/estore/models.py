from django.db import models
from django.shortcuts import reverse
from django.conf import settings


BRANDS_CHOICE =(
    ('RS', 'Roadster'),
    ('PM', 'Puma'),
    ('WR', 'WROGN'),
    ('FC', 'Fort Collins'),
    ('HR', 'HRX'),
    ('HN', 'HERE & NOW'),
    ('MH', 'Mast & Harbour'),
    ('CS', 'Campus Sutra'),
    ('MR', 'Moda Rapido'),
    ('AD', 'Adidas'),
    ('KK', 'Kook & Keech'),
    ('LO', 'Locomotive'),
    ('HL', 'HIGH LANDER'),
)

SEX_CHOICE = (
    ('M', 'MEN'),
    ('W', 'WOMEN')
)

CLOTH_CHOICE =(
    ('TS', 'T-Shirts'),
    ('FS', 'Formal Shirts'),
    ('CS', 'Casual Shirts'),
    ('JS', 'Jackets')
)

WEAR_TYPE_CHOICE = (
    ('TP', 'Top Wear'),
    ('BW', 'Botom Wear'),
    ('IW', 'Inner Wear'),
    ('FW', 'Festive Wear'),
    ('IW', 'Indian Wear'),
    ('WW', 'Western Wear')
)

SIZE_CHOICE = (
    ('S', 'Small'),
    ('M', 'Medium'),
    ('L', 'Large'),
    ('XL', 'Xtra Large'),
    ('XXL', 'Xtra Xtra Large')
)


class Product(models.Model):
    brand = models.CharField(choices=BRANDS_CHOICE, max_length=2)
    title = models.CharField(max_length=30)
    sex_type = models.CharField(choices=SEX_CHOICE, max_length=2)
    cloth_type = models.CharField(choices=CLOTH_CHOICE, max_length=2)
    wear_type = models.CharField(choices=WEAR_TYPE_CHOICE, max_length=2)
    size = models.CharField(choices=SIZE_CHOICE, max_length=3)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    discount_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    slug = models.SlugField()
    image = models.ImageField(upload_to='static/img/', blank=True, null=True)

    def get_absolute_url(self):
        return reverse("estore:product", kwargs={"slug": self.slug})

    def get_add_to_cart_url(self):
        return reverse("estore:cart_add", kwargs={"slug": self.slug})

    def get_remove_from_cart_url(self):
        return reverse("estore:cart_remove", kwargs={"slug": self.slug})

    def get_discount_percentage(self):
        return int((self.price - self.discount_price)/(self.price / 100))

    def __str__(self):
        return self.title


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_item_discount_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_item_discount_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_item_discount_price()
        return self.get_total_item_price()

    def get_image_url(self):
        return self.item.image.url



class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
    def get_total_amount(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total
    
    def get_total_items(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.quantity
        return total

    def get_amount(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_item_price()
        return total

    def get_total_saved_amount(self):
        return self.get_amount() - self.get_total_amount()
    
    def get_delivery_charges(self):
        return self.get_amount() - self.get_total_amount()
    
