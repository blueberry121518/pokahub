from decimal import Decimal
from marshmallow import Schema, fields, validate, ValidationError

def validate_two_decimals(value: Decimal):
    # Checks for at most two decimal places
    if value.as_tuple().exponent < -2:
        raise ValidationError("Must have at most two decimal places.")

class SessionSchema(Schema):
    # The buy in must be a positive number
    buy_in = fields.Decimal(required=True, as_string=True, validate=[validate.Range(min=0), validate_two_decimals])

    # The buy out must be a positive number
    buy_out = fields.Decimal(required=True, as_string=True, validate=[validate.Range(min=0), validate_two_decimals])

    # Expecting ISO8601 formatted datetime strings
    start_time = fields.DateTime(required=True)
    end_time = fields.DateTime(required=True)

    # The title must be a string
    title = fields.String(validate=validate.Length(max=255))
    caption = fields.String(required=False, allow_none=True)

    # List of image urls with at most 5 images
    images = fields.List(
        fields.String(validate=validate.Length(max=500)),
        required=False,
        validate=validate.Length(max=5)
    )

    # Requires a public or private setting
    public = fields.Boolean(required=True)

    # Requires at least one blind, up to 3
    blinds = fields.List(
        fields.Decimal(as_string=True, validate=validate.Range(min=0)),
        required=True,
        validate=validate.Length(min=1, max=3)
    )

    # Optional ante
    ante = fields.Decimal(required=False, as_string=True, allow_none=True, validate=[validate.Range(min=0), validate_two_decimals])