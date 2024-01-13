from decimal import Decimal
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    auto_id = models.PositiveIntegerField(db_index=True,unique=True)
    creator = models.ForeignKey("auth.User",blank=True,related_name="creator_%(class)s_objects",on_delete=models.CASCADE)
    updator = models.ForeignKey("auth.User",blank=True,related_name="updator_%(class)s_objects",on_delete=models.CASCADE)
    date_added = models.DateTimeField(db_index=True,auto_now_add=True)    
    date_updated = models.DateTimeField(auto_now_add=True) 

    class Meta:
        abstract = True


class Company(BaseModel):
    name = models.CharField(_("Company Name"),max_length=128)
    contact_person = models.CharField(_("Contact Person"),max_length=128)
    address = models.TextField(_("Address")) 
    country = models.ForeignKey("main.Country",on_delete=models.CASCADE)
    state = models.ForeignKey("main.State",on_delete=models.CASCADE)
    city = models.CharField(_("City"),max_length=128,blank=True,null=True)
    postal_code = models.CharField(_("Postal Code"),max_length=128,blank=True,null=True)
    email = models.EmailField(_("Email")) 
    phone = PhoneNumberField(_("Phone Number"))
    mobile = PhoneNumberField(_("Mobile Number"),blank=True,null=True)
    fax = models.CharField(_("Fax"),max_length=128,blank=True,null=True)
    website = models.URLField(_("Website"),null=True,blank=True)
    is_deleted = models.BooleanField(_("Is this company deleted ? "),default=False)

    class Meta:
        db_table = 'company'
        verbose_name = _('company')
        verbose_name_plural = _('companies')
        ordering = ('name',)
        
    def __str__(self):
        return self.name
    

# class CompanyTheme(models.Model):
#     name = models.ForeignKey("main.Company",on_delete=models.CASCADE,limit_choices_to={'is_deleted': False})
#     logo = models.ImageField('Light Logo',upload_to="company/",blank=True,null=True)     
#     favicon = models.ImageField('Favicon',upload_to="company/",blank=True,null=True)
#     is_deleted = models.BooleanField(_("Is this theme deleted ? "),default=False)

#     class Meta:
#         db_table = 'company theme'
#         verbose_name = _('company theme')
#         verbose_name_plural = _('company themes')
#         ordering = ('name',)
        
#     def __str__(self):
#         return self.name


class Country(models.Model):
    name = models.CharField(max_length=128)
    iso3 = models.CharField(max_length=128)
    iso2 = models.CharField(max_length=128)
    numeric_code = models.CharField(max_length=128)
    phone_code = models.CharField(max_length=128)
    capital = models.CharField(max_length=128)
    currency = models.CharField(max_length=128)
    currency_symbol = models.CharField(max_length=128)
    tld = models.CharField(max_length=128)
    native = models.CharField(max_length=128)
    region = models.CharField(max_length=128)
    subregion = models.CharField(max_length=128)
    latitude = models.CharField(max_length=128)
    longitude = models.CharField(max_length=128)

    class Meta:
        db_table = 'countries'
        verbose_name = _('country')
        verbose_name_plural = _('countries')

    def __str__(self): 
        return "%s" %(self.name)


class State(models.Model):
    country = models.ForeignKey('main.Country',on_delete=models.CASCADE,)
    name = models.CharField(max_length=128)
    country_code = models.CharField(max_length=128)
    state_code = models.CharField(max_length=128)
    latitude = models.CharField(max_length=128)
    longitude = models.CharField(max_length=128)

    class Meta:
        db_table = 'states'
        verbose_name = _('state')
        verbose_name_plural = _('states')

    def __str__(self): 
        return "%s" %(self.name)

