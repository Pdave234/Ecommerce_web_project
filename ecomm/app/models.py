from django.db import models
from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField,PasswordChangeForm,PasswordResetForm,SetPasswordForm
from django.contrib.auth.models import User


# Create your models here.
STATE_CHOICES=(
    ('Andhra Pradesh','Andhra Pradesh'),
    ('Haryana','Haryana'),
    ('Maharashtra','Maharashtra'),
    ('Madhya Pradesh','Madhya Pradesh'),
    ('Arunachal Pradesh','Arunachal Pradesh'),
    ('Punjab','Punjab'),
    ('West Bengal','West Bengal'),
    ('Rajasthan','Rajasthan'),
    ('Goa','Goa'),
    ('Jammu and Kashmir','Jammu and Kashmir'),
    ('Delhi','Delhi'),
    ('Kerala','Kerala'),
)

CATEGORY_CHOICES=(
    ('CR','Curd'),
    ('ML','Milk'),
    ('LS','Lassi'),
    ('MS','Milkshake'),
    ('PN','Paneer'),
    ('GH','Ghee'),
    ('CZ','Cheese'),
    ('IC','Ice-Creams'),
)

class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    composition = models.TextField(default='')
    prodapp = models.TextField(default='')
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    product_image = models.ImageField(upload_to='product')
    def __str__(self):
        return self.title
    
class CustomerRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs=
    {'autofocus':'True','class':'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs=
    {'class':'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs=
    {'class':'form-control'}))
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs=
    {'class':'form-control'}))
    
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs=
    {'autofocus':'True','class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs=
    {'autocomplete':'current-password','class':'form-control'}))

class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Old Password",widget=forms.PasswordInput(attrs=
    {'autofocus':'True','autocomplete':'current-password','class':'form-control'}))
    new_password1 = forms.CharField(label="New Password", widget=forms.PasswordInput(attrs=
    {'autocomplete':'current-password','class':'form-control'}))
    new_password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs=
    {'autocomplete':'current-password','class':'form-control'}))

class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))

class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label="New Password", widget=forms.PasswordInput(attrs=
    {'autocomplete':'current-password','class':'form-control'}))
    new_password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs=
    {'autocomplete':'current-password','class':'form-control'}))

class Customer(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    mobile=models.IntegerField(default=0)
    locality=models.CharField(max_length=200)
    city=models.CharField(max_length=200)    
    zipcode=models.IntegerField()
    state=models.CharField(choices=STATE_CHOICES,max_length=100)
    def __str__(self):
        return self.name
    
class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name','mobile','locality','city','zipcode','state']
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'mobile':forms.NumberInput(attrs={'class':'form-control'}),
            'locality':forms.TextInput(attrs={'class':'form-control'}),
            'city':forms.TextInput(attrs={'class':'form-control'}),
            'zipcode':forms.NumberInput(attrs={'class':'form-control'}),
            'state':forms.Select(attrs={'class':'form-control'}),
        }

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price
    
STATUS_CHOICES = (
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On the way','On the way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel'),
    ('Pending','Pending'),
)


class Payment(models.Model): 
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    amount = models.FloatField()
    razorpay_order_id = models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_status = models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_id = models.CharField(max_length=100,blank=True,null=True)
    paid = models.BooleanField(default=False)
        
class OrderPlaced(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_created=True)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES, default="Pending")
    payment = models.ForeignKey(Payment,on_delete=models.CASCADE,default="")

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price
    
class Wishlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)