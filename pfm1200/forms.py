from django import forms
from django.forms import modelformset_factory
from .models import PFM1200WireTerminal, PFM1200Cable

WIRE_COLOR_CHOICES = [
    ('',      '— not specified'),
    ('BN',    'BN — Brown'),
    ('BK',    'BK — Black'),
    ('BU',    'BU — Blue'),
    ('WH',    'WH — White'),
    ('GN',    'GN — Green'),
    ('YE',    'YE — Yellow'),
    ('RD',    'RD — Red'),
    ('GY',    'GY — Grey'),
    ('VT',    'VT — Violet'),
    ('PK',    'PK — Pink'),
    ('OG',    'OG — Orange'),
    ('GN/YE', 'GN/YE — Green / Yellow'),
    ('BU/RD', 'BU/RD — Blue / Red'),
    ('GY/PK', 'GY/PK — Grey / Pink'),
    ('RD/BU', 'RD/BU — Red / Blue'),
]


class WireTerminalForm(forms.ModelForm):
    wire_color = forms.ChoiceField(
        choices=WIRE_COLOR_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'wf-select'}),
    )

    class Meta:
        model  = PFM1200WireTerminal
        fields = ['order', 'wire_color', 'device_pin', 'terminal_ref', 'notes']
        widgets = {
            'order':        forms.NumberInput(attrs={'class': 'wf-order', 'min': 0}),
            'device_pin':   forms.TextInput(attrs={'class': 'wf-pin',   'placeholder': '1'}),
            'terminal_ref': forms.TextInput(attrs={'class': 'wf-term',  'placeholder': 'T.160.7'}),
            'notes':        forms.TextInput(attrs={'class': 'wf-notes', 'placeholder': 'Optional notes'}),
        }


def make_wire_formset(extra=1):
    return modelformset_factory(
        PFM1200WireTerminal,
        form=WireTerminalForm,
        extra=extra,
        can_delete=True,
    )


class CableMetaForm(forms.ModelForm):
    class Meta:
        model  = PFM1200Cable
        fields = ['cable_id', 'cable_part_number', 'connection_details', 'length_mm', 'junction_box_ref', 'notes']
        widgets = {
            'cable_id':          forms.TextInput(attrs={'class': 'wf-input'}),
            'cable_part_number': forms.TextInput(attrs={'class': 'wf-input'}),
            'connection_details':forms.TextInput(attrs={'class': 'wf-input'}),
            'length_mm':         forms.NumberInput(attrs={'class': 'wf-input', 'min': 0, 'placeholder': '0 = not specified'}),
            'junction_box_ref':  forms.TextInput(attrs={'class': 'wf-input'}),
            'notes':             forms.Textarea(attrs={'class': 'wf-input', 'rows': 2}),
        }
