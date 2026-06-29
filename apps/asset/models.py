from decimal import Decimal, InvalidOperation
from django.db import models
from django.utils import timezone
from datetime import timedelta
from apps.main.models import BaseModel
from django.utils.translation import gettext_lazy as _


class Asset(BaseModel):
    company = models.ForeignKey("main.Company",on_delete=models.CASCADE,limit_choices_to={'is_deleted': False})
    name = models.CharField(_("Asset Name"),max_length=255)
    description = models.TextField(_("Asset Description"),null=True,blank=True)
    purchase_date = models.DateField(_("Purchase Date"))
    purchase_price = models.DecimalField(_("Purchase Price"),max_digits=10, decimal_places=2)
    useful_life_years = models.PositiveIntegerField(_("Useful Life in Years [After how many years will this asset expire?]"))
    salvage_value = models.DecimalField(_("Salvage/Scrap Value"),max_digits=10, decimal_places=2) 
    bill = models.FileField(_("Upload Purchase Bill"),null=True,blank=True)
    photo = models.ImageField(_("Images of Asset "),upload_to='assets/images/', null=True, blank=True)
    is_deleted = models.BooleanField(_('Is This Asset Deleted ?'),default=False)

    class Meta:
        db_table = ('asset_asset')
        verbose_name = _('Asset')
        verbose_name_plural = _('Assets')
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def depreciation_amount(self):
        try:
            if self.useful_life_years > 0:
                return (self.purchase_price - self.salvage_value) / self.useful_life_years
            else:
                return Decimal(0)
        except InvalidOperation:
            return Decimal(0)

    @property
    def accumulated_depreciation(self):
        if self.useful_life_years > 0:
            years_elapsed = Decimal((timezone.now().date() - self.purchase_date).days) / Decimal(365.25)
            accumulated_depreciation = min(self.purchase_price - self.salvage_value, years_elapsed * self.depreciation_amount)
            return accumulated_depreciation.quantize(Decimal('0.01'))
        else:
            return self.purchase_price - self.salvage_value

    @property
    def current_value(self):
        if self.useful_life_years > 0:
            value = self.purchase_price - self.accumulated_depreciation
        else:
            value = self.salvage_value
        return value.quantize(Decimal('0.01'))


# class AssetMaintenance(BaseModel):
#     asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='maintenance_records')
#     maintenance_date = models.DateField()
#     cost = models.DecimalField(max_digits=10, decimal_places=2)
#     description = models.TextField()
#     bill = models.FileField()

#     def __str__(self):
#         return f"Maintenance {self.id} for {self.asset.name}"
    
    
