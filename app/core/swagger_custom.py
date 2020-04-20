from drf_yasg import openapi
from drf_yasg.app_settings import swagger_settings
from drf_yasg.inspectors import SwaggerAutoSchema, SerializerInspector


# Get Examples from Serializer
class ExampleInspector(SerializerInspector):
    def process_result(self, result, method_name, obj, **kwargs):
        has_examples = hasattr(obj, 'Meta') and hasattr(obj.Meta, 'examples')
        if isinstance(result, openapi.Schema.OR_REF) and has_examples:
            schema = openapi.resolve_ref(result, self.components)
            if 'properties' in schema:
                properties = schema['properties']
                for name in properties.keys():
                    if name in obj.Meta.examples:
                        properties[name]['example'] = obj.Meta.examples[name]
        return result


class MyAutoSchema(SwaggerAutoSchema):
    field_inspectors = [
       ExampleInspector,
    ] + swagger_settings.DEFAULT_FIELD_INSPECTORS

    def __init__(self, view, path, method, components, request, overrides, operation_keys=None):
        super(MyAutoSchema, self).__init__(view, path, method, components, request, overrides, operation_keys)

    def get_operation(self, operation_keys=None):
        ret = super(MyAutoSchema, self).get_operation(operation_keys)
        summary = ret.get('summary', None)
        if summary:
            ret['operationId'] = summary
        if self.overrides:
            consumes = self.overrides.get('consumes', None)
            if consumes:
                ret['consumes'] = [consumes]

        return ret

    # Make Permissions description

    def get_summary_and_description(self):
        """Return summary and description extended with permission docs."""
        summary, description = super().get_summary_and_description()
        permissions_description = self._get_permissions_description()
        if permissions_description:
            description += permissions_description
        return summary, description

    def _get_permissions_description(self):
        permission_class = getattr(self.view, 'permission_classes', None)
        if permission_class:
            return f'\n**Permissions:** `{permission_class.pop().__name__}`'
        else:
            return None
