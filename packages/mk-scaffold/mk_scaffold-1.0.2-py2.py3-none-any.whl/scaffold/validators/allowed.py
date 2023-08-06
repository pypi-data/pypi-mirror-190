import sys

from prompt_toolkit.validation import ValidationError


def validate(value, schema):
    allowed = schema.get("allowed")
    if allowed is None:
        return False, None

    # FIXME: we should convert before hand fake floats (3.7) to strings
    if str(value) not in allowed:
        allowed = ", ".join(allowed)
        raise ValidationError(message=f"Answer must be within [{allowed}]")

    return False, value
