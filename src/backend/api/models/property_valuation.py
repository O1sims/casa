from rest_framework import serializers

from api.models.property_data import PropertyAmenitiesModel, HOUSE_STYLE_CHOICES, HEATING_CHOICES

# Postcodes for Belfast and Holywood
POSTCODE_CHOICES = (
    "BT1", "BT2", "BT3", "BT4", "BT5",
    "BT6", "BT7", "BT8", "BT9", "BT10",
    "BT11", "BT12", "BT13", "BT14",
    "BT15", "BT16", "BT17", "BT18",
    "BT28", "BT36", "BT37",
)


class PropertyDetailsModel(serializers.Serializer):
    bedrooms = serializers.IntegerField(min_value=1)
    aggregateStyle = serializers.ChoiceField(
        choices=HOUSE_STYLE_CHOICES)
    heating = serializers.ChoiceField(
        choices=HEATING_CHOICES)
    amenities = PropertyAmenitiesModel()


class PropertyValuationEstimationModel(serializers.Serializer):
    postcode = serializers.ChoiceField(
        choices=POSTCODE_CHOICES)
    details = PropertyDetailsModel()


class PropertyValuationDifferentialModel(serializers.Serializer):
    givenPrice = serializers.FloatField(
        min_value=1)
    propertyInfo = PropertyValuationEstimationModel()

