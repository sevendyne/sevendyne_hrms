from decimal import Decimal
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    auto_id = models.PositiveIntegerField(db_index=True,unique=True)
    a_id = models.PositiveIntegerField()   
    creator = models.ForeignKey("auth.User",blank=True,related_name="creator_%(class)s_objects",on_delete=models.CASCADE)
    updator = models.ForeignKey("auth.User",blank=True,related_name="updator_%(class)s_objects",on_delete=models.CASCADE)
    date_added = models.DateTimeField(db_index=True,auto_now_add=True)    
    date_updated = models.DateTimeField(auto_now_add=True) 

    class Meta:
        abstract = True


class Company(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    auto_id = models.PositiveIntegerField(db_index=True,unique=True)
    creator = models.ForeignKey("auth.User",blank=True,related_name="creator_%(class)s_objects",on_delete=models.CASCADE,)
    updator = models.ForeignKey("auth.User",blank=True,related_name="updator_%(class)s_objects",on_delete=models.CASCADE,)
    date_added = models.DateTimeField(db_index=True,auto_now_add=True)    
    date_updated = models.DateTimeField(auto_now_add=True) 
    name = models.CharField(_("Company Name"),max_length=128)
    contact_person = models.CharField(_("Contact Person"),max_length=128)
    address = models.TextField(_("Address"),blank=True,null=True) 
    country = models.ForeignKey("main.Country",on_delete=models.CASCADE)
    state = models.ForeignKey("main.State",on_delete=models.CASCADE)
    city = models.CharField(_("City"),max_length=128,blank=True,null=True)
    postal_code = models.CharField(_("Postal Code"),max_length=128,blank=True,null=True)
    email = models.EmailField(_("Email")) 
    phone = models.CharField(_("Phone Number"),max_length=128)
    mobile = models.CharField(_("Mobile Number"),max_length=128,blank=True,null=True)
    fax = models.CharField(_("Fax"),max_length=128,blank=True,null=True)
    website = models.URLField(_("Website"),null=True,blank=True)
    logo = models.ImageField(_("Photo"), upload_to='logos/', null=True, blank=True)
    is_deleted = models.BooleanField(_("Is this company deleted ? "),default=False)

    class Meta:
        db_table = 'company'
        verbose_name = _('company')
        verbose_name_plural = _('companies')
        ordering = ('name',)
        
    def __str__(self):
        return self.name    


class CompanyAccess(models.Model):
    user = models.ForeignKey('auth.User',null=True,on_delete=models.CASCADE)
    company = models.ForeignKey('main.Company',blank=True,on_delete=models.CASCADE,limit_choices_to={'is_deleted' : False})
    group = models.ForeignKey('auth.Group',on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)
    is_default = models.BooleanField(default=False)       

    class Meta:
        db_table = 'company_access'
        verbose_name = _('company_access')
        verbose_name_plural = _('company_access')
        ordering = ('company',)
    
    class Admin:
        list_dispay = ('company','group','is_accepted',)
    
    def __str__(self):
        return self.company.name + ' ' + self.group.name  
    

    

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


class Portfolio(models.Model):
    title = models.CharField(_('Title'), max_length=80)
    description = models.CharField(_('Description'), max_length=200)
    image = models.ImageField(upload_to='portfolio_images/')
    is_deleted = models.BooleanField(default=False)   

    class Meta:
        db_table = ('main_portfolio')
        verbose_name = _('portfolio')
        verbose_name_plural = _('portfolio')

    def __str__(self):
        return self.title