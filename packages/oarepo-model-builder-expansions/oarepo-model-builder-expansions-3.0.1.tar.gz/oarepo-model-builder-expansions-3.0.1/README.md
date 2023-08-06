# OARepo model builder expansions
Plugin for oarepo-model-builder to allow invenio expandable fields. Expandable fields allow saving fields of other referenced records in the referencing record object.
<br>
Expandable fields are specified on model level as a list and the yaml for 
single expandable field has following structure:
- `field name` path to the field in the referencing record
- `referenced keys` list of paths to the fields in the referenced record
- `service` service for the referenced record, used to retrieve the referenced 
record to get the field values
- `service-alias` not required, specify alias for the service in the previous option
- `pid-field` not required, specify the field in the referencing record holding the 
pid of the referenced record.
- `expandable-field-class` not required, specify the class of the expandable 
field, by default it's [oarepo_runtime.expansions.expandable_fields.ReferencedRecordExpandableField](https://github.com/oarepo/oarepo-runtime/blob/main/oarepo_runtime/expansions/expandable_fields.py)

Plugin use case example is in tests.
