from drf_yasg import openapi
from drf_yasg.app_settings import swagger_settings
from drf_yasg.inspectors import SwaggerAutoSchema, SerializerInspector


def check_meta_examples(obj, schema_or_ref, resolver=None):
    has_examples = hasattr(obj, 'Meta') and hasattr(obj.Meta, 'examples')
    if isinstance(schema_or_ref, openapi.Schema.OR_REF) and has_examples:
        schema = openapi.resolve_ref(schema_or_ref, resolver)
        if 'properties' in schema:
            properties = schema['properties']
            for name in properties.keys():
                if name in obj.Meta.examples:
                    properties[name]['example'] = obj.Meta.examples[name]

    return schema_or_ref


class ExampleInspector(SerializerInspector):
    def process_result(self, result, method_name, obj, **kwargs):
        ret = check_meta_examples(obj, schema_or_ref=result, resolver=self.components)

        return ret


class MyAutoSchema(SwaggerAutoSchema):
    field_inspectors = [
        # ExampleInspector,
    ] + swagger_settings.DEFAULT_FIELD_INSPECTORS

    def __init__(self, view, path, method, components, request, overrides, operation_keys=None):
        super(MyAutoSchema, self).__init__(view, path, method, components, request, overrides, operation_keys)

    def get_operation(self, operation_keys=None):
        ret = super(MyAutoSchema, self).get_operation(operation_keys)
        description = ret.get('description', None)
        description = description.splitlines() if description else None
        if description and not ret.get('summary', None):
            ret['operationId'] = description.pop(0)
            ret['description'] = ''.join(description)
        if self.overrides:
            consumes = self.overrides.get('consumes', None)
            if consumes:
                ret['consumes'] = [consumes]

        return ret
    #
    # def _get_request_body_override(self):
    #     schema = super()._get_request_body_override()
    #     obj = super().get_view_serializer()
    #     ret = check_meta_examples(obj, schema)
    #
    #     return ret
