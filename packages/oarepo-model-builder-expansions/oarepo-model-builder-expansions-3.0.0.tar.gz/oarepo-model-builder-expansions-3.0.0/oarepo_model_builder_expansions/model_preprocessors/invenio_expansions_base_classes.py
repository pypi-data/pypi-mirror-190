from oarepo_model_builder.model_preprocessors import ModelPreprocessor

class InvenioExpansionsBaseClassesModelPreprocessor(ModelPreprocessor):
    TYPE = "invenio_expansions_base_classes"

    def transform(self, schema, settings):
        self.set_default_and_prepend_if_not_present(
            schema.current_model,
            "record-service-bases",
            [],
            "oarepo_runtime.expansions.service.ExpandableFieldsServiceMixin",
        )