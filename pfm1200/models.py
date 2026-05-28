from django.db import models


class PFM1200Device(models.Model):
    order = models.PositiveIntegerField(default=0)
    device_ref = models.CharField(max_length=20, blank=True,
                                  help_text='Device reference ID (e.g. U205, H113, Y0)')
    part_number = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=200)
    classification = models.CharField(max_length=100)
    designation = models.TextField()
    type_function = models.TextField()
    signal_form = models.TextField()
    details = models.TextField(blank=True)
    classification_notes = models.TextField(blank=True)
    connector_type = models.CharField(max_length=20, blank=True)
    connector_part_number = models.CharField(max_length=50, blank=True)
    image = models.ImageField(upload_to='pfm1200/devices/', blank=True, null=True,
                              help_text='Device photo (JPG, PNG)')
    datasheet = models.FileField(upload_to='pfm1200/datasheets/', blank=True, null=True,
                                 help_text='Datasheet PDF')
    datasheet_url = models.URLField(blank=True,
                                    help_text='External datasheet URL (optional)')

    class Meta:
        ordering = ['order']

    def __str__(self):
        label = self.part_number if self.part_number and self.part_number != '_' else '—'
        return f"{label} — {self.description}"


class PFM1200Cable(models.Model):
    device = models.ForeignKey(PFM1200Device, on_delete=models.CASCADE, related_name='cables')
    cable_id = models.CharField(max_length=20)
    cable_part_number = models.CharField(max_length=50, blank=True)
    connection_details = models.CharField(max_length=200, blank=True)
    length_mm = models.PositiveIntegerField(
        default=0,
        help_text='Total cable length in mm (0 = not specified in drawing)',
    )
    junction_box_ref = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.cable_id} ({self.device.description})"


class PFM1200WireTerminal(models.Model):
    cable = models.ForeignKey(PFM1200Cable, on_delete=models.CASCADE, related_name='wires')
    order = models.PositiveIntegerField(default=0)
    wire_color = models.CharField(max_length=30)
    device_pin = models.CharField(max_length=30, blank=True)
    terminal_ref = models.CharField(max_length=100, blank=True)
    notes = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.wire_color} — Pin {self.device_pin} → {self.terminal_ref}"
