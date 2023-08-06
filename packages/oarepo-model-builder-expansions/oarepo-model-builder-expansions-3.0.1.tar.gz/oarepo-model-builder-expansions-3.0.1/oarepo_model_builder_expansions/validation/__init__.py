import marshmallow as ma
from marshmallow import fields

class ExpandableFieldsPropertiesSchema(ma.Schema):
    field_name = fields.String(data_key="field-name")
    referenced_keys = fields.List(fields.String, data_key="referenced-keys")
    service = fields.String()
    service_alias = fields.String(data_key="service-alias", required=False)
    expandable_field_class = fields.String(data_key="expandable-field-class", required=False)
    pid_field = fields.String(data_key="pid-field", required=False)


class ExpandableFieldsModelSchema(ma.Schema):
    expandable_fields = fields.List(fields.Nested(ExpandableFieldsPropertiesSchema), data_key="expandable-fields")

validators = {"model": ExpandableFieldsModelSchema}