from marshmallow import Schema, fields, validates_schema

from argrelay.enum_desc.ReservedEnvelopeClass import ReservedEnvelopeClass
from argrelay.misc_helper.TypeDesc import TypeDesc
from argrelay.schema_config_interp.FunctionEnvelopeInstanceDataSchema import function_envelope_instance_data_desc

envelope_id_ = "envelope_id"
"""
Not required (yet) field within `envelope_metadata` with unique id for `data_envelope`.
If provided, it is given to MongoDB as `id_` (otherwise, if not provided, MongoDB auto-generates one).
"""

envelope_class_ = "envelope_class"
"""
Required field within `envelope_metadata` with unique id for `envelope_class` which defines schema for `instance_data`.
"""

instance_data_ = "instance_data"
"""
Data specific to `envelope_class`.
Unlike `envelope_payload` `argrelay` does not inspect, `instance_data` can be inspected
(if not inspected by `argrelay`, but by its plugins) and this data has schema implied or defined somewhere.
"""

envelope_payload_ = "envelope_payload"
"""
Data `argrelay` does not inspect.
"""

context_control_ = "context_control"

envelope_metadata_ = "envelope_metadata"
"""
All search keys `argrelay` uses to find this `data_envelope`.
"""


class DataEnvelopeSchema(Schema):
    """
    Schema for all :class:`StaticDataSchema.data_envelopes`
    """

    class Meta:
        strict = True

    envelope_metadata = fields.Dict(
        required = True,
    )

    """
    Data specific to `envelope_class`.
    Each envelope class may define its own schema for that data.
    For example, `ReservedEnvelopeClass.ClassFunction` defines `FunctionEnvelopeInstanceDataSchema`.
    """
    instance_data = fields.Dict(
        # TODO: make it required for predictability - isn't it required?
        required = False,
    )

    """
    Arbitrary schemaless data (payload) wrapped by `DataEnvelopeSchema`.
    It is not inspected by `argrelay`.
    """
    envelope_payload = fields.Dict(
        # TODO: make it required for predictability - isn't it required?
        required = False,
    )

    """
    List of arg types to be pushed to the next `args_context` to query next `data_envelope`-s.
    """
    context_control = fields.List(
        fields.String(),
        # TODO: make it required for predictability - isn't it required?
        required = False,
    )

    @validates_schema
    def validate_known(self, input_dict, **kwargs):
        if input_dict[envelope_metadata_][envelope_class_] == ReservedEnvelopeClass.ClassFunction.name:
            function_envelope_instance_data_desc.validate_dict(input_dict[instance_data_])


data_envelope_desc = TypeDesc(
    dict_schema = DataEnvelopeSchema(),
    ref_name = DataEnvelopeSchema.__name__,
    dict_example = {
        instance_data_: function_envelope_instance_data_desc.dict_example,
        envelope_payload_: {},
        context_control_: [
            "SomeTypeB",
        ],
        # TODO: All these keys were supposed to be at the top-level, but `marshmallow` cannot dump arbitrary keys.
        #       Try to figure out how, or remote this TODO.
        envelope_metadata_: {
            envelope_id_: "some_unique_id",
            envelope_class_: ReservedEnvelopeClass.ClassFunction.name,
            "SomeTypeA": "A_value_1",
            "SomeTypeB": "B_value_1",
            "SomeTypeC": "C_value_1",
        },
    },
    default_file_path = "",
)
