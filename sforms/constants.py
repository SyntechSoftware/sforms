class FieldTypes:
    FIELD_TYPE_TEXT = 'text'
    FIELD_TYPE_EMAIL = 'email'
    FIELD_TYPE_PASSWORD = 'password'
    FIELD_TYPE_NUMBER = 'number'
    FIELD_TYPE_TEXTAREA = 'textarea'
    FIELD_TYPE_CHECKBOX = 'checkbox'
    FIELD_TYPE_MULTICHECKBOX = 'multicheckbox'
    FIELD_TYPE_RADIO = 'radio'
    FIELD_TYPE_SELECT = 'choice'
    FIELD_TYPE_HIDDEN = 'hidden'
    FIELD_TYPE_LABEL = 'label'
    FIELD_TYPE_ATTACH = 'attach'

    CHOICES = (
        (FIELD_TYPE_TEXT, 'Text'),
        (FIELD_TYPE_EMAIL, 'E-mail'),
        (FIELD_TYPE_PASSWORD, 'Password'),
        (FIELD_TYPE_NUMBER, 'Number'),
        (FIELD_TYPE_TEXTAREA, 'Textarea'),
        (FIELD_TYPE_CHECKBOX, 'Checkbox'),
        (FIELD_TYPE_MULTICHECKBOX, 'Multicheckbox'),
        (FIELD_TYPE_RADIO, 'Radio'),
        (FIELD_TYPE_SELECT, 'Choice'),
        (FIELD_TYPE_HIDDEN, 'Hidden'),
        (FIELD_TYPE_LABEL, 'Label'),
        (FIELD_TYPE_ATTACH, 'Attachment'),
    )

    HAS_VALUES = (FIELD_TYPE_SELECT, FIELD_TYPE_MULTICHECKBOX, FIELD_TYPE_RADIO)
