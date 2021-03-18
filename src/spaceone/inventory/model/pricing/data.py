from schematics import Model
from schematics.types import ModelType, ListType, StringType, DictType, IntType, \
    DateTimeType, FloatType


class PriceDimension(Model):
    price_dimension_code = StringType(default='')
    applies_to = ListType(StringType, default=[], deserialize_from='appliesTo')
    begin_range = StringType(serialize_when_none=False, deserialize_from='beginRange')
    description = StringType(serialize_when_none=False)
    end_range = StringType(serialize_when_none=False, deserialize_from='endRange')
    price_per_unit = DictType(FloatType, deserialize_from='pricePerUnit')
    rate_code = StringType(serialize_when_none=False, deserialize_from='rateCode')
    unit = StringType(serialize_when_none=False)


class Terms(Model):
    effective_date = DateTimeType(serialize_when_none=False)
    offer_term_code = StringType()
    term_type = StringType(choices=('OnDemand', 'Reserved'))
    price_dimensions = ListType(ModelType(PriceDimension), default=[])
    term_attributes = DictType(StringType)

class Product(Model):
    service_code = StringType()
    region_name = StringType()
    product_family = StringType()
    sku = StringType()
    attributes = DictType(StringType)
    publication_date = DateTimeType(serialize_when_none=False)
    version = StringType()
    terms = ListType(ModelType(Terms), default=[])

    def reference(self):
        return {
            "resource_id": self.sku
        }
