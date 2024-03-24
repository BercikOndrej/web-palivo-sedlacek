from django.db import models
from math import ceil

# Create your models here.

class WoodItem:
  """Class representing wood item for a price list"""

  def __init__(
    self, 
    name,
    wood_type,
    syp_25,
    skl_25,
    syp_33,
    skl_33,
    syp_50,
    skl_50,
    skl_100,
    sleva_skl
    ):
    self.name = name
    if wood_type == "null":
      self.wood_type = "---"
    else:
      self.wood_type = wood_type
    self.syp_25 = syp_25
    self.skl_25 = skl_25
    self.syp_33 = syp_33
    self.skl_33 = skl_33
    self.syp_50 = syp_50
    self.skl_50 = skl_50
    self.skl_100 = skl_100
    self.sleva_skl = sleva_skl

    if sleva_skl != "null":
      # Skl
      self.skl_25_disc = self.count_discount_skl(self.skl_25)
      self.skl_33_disc = self.count_discount_skl(self.skl_33)
      self.skl_50_disc = self.count_discount_skl(self.skl_50)
      self.skl_100_disc = self.count_discount_skl(self.skl_100)
      # Syp
      self.syp_25_disc = self.count_discount_syp(self.skl_25)
      self.syp_33_disc = self.count_discount_syp(self.skl_33)
      self.syp_50_disc = self.count_discount_syp(self.skl_50)

  # Methods
  def count_discount_skl(self, skl_price_string):
    """ Return string representing number after discount on skladane wood"""
    skl_price = WoodItem.separated_str2num(skl_price_string)
    discount_price = skl_price - WoodItem.separated_str2num(self.sleva_skl)
    return WoodItem.num2separated_str(discount_price)

  def count_discount_syp(self, skl_price_string):
    """ Return string representing numer after discount on sypane wood
    @param: skl_number The number representing a price of same size wood but in skladane wood.
    If we want discount price of 33cm syp wood we must enter price of 33cm skl wood without discount
    """
    skl_price = WoodItem.separated_str2num(skl_price_string)
    discount_price = (skl_price - WoodItem.separated_str2num(self.sleva_skl)) * 0.61
    round_discount_price = WoodItem.round_up_on_decimals(discount_price)
    return WoodItem.num2separated_str(round_discount_price)

  # Static methods
  def num2separated_str(number):
    return f'{number:_}'.replace('_', ' ')
  
  def separated_str2num(string):
    return int(string.replace(' ',''))
  
  def round_up_on_decimals(number):
    rounded_up_number = ceil(number)
    last_number = rounded_up_number - (rounded_up_number // 10) * 10
    if last_number == 0:
      return rounded_up_number
    else:
      return rounded_up_number + 10 - last_number

  
  