from django.db import models


class PFM2100Device(models.Model):
    order = models.PositiveIntegerField(default=0)
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
    image = models.ImageField(upload_to='pfm2100/devices/', blank=True, null=True,
                              help_text='Device photo (JPG, PNG)')
    datasheet = models.FileField(upload_to='pfm2100/datasheets/', blank=True, null=True,
                                 help_text='Datasheet PDF')
    datasheet_url = models.URLField(blank=True,
                                    help_text='External datasheet URL (optional)')

    class Meta:
        ordering = ['order']

    def __str__(self):
        label = self.part_number if self.part_number and self.part_number != '_' else '—'
        return f"{label} — {self.description}"


class PFM2100Cable(models.Model):
    device = models.ForeignKey(PFM2100Device, on_delete=models.CASCADE, related_name='cables')
    cable_id = models.CharField(max_length=20)
    cable_part_number = models.CharField(max_length=50, blank=True)
    connection_details = models.CharField(max_length=200, blank=True)
    junction_box_ref = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.cable_id} ({self.device.description})"


class PFM2100WireTerminal(models.Model):
    cable = models.ForeignKey(PFM2100Cable, on_delete=models.CASCADE, related_name='wires')
    order = models.PositiveIntegerField(default=0)
    wire_color = models.CharField(max_length=30)
    device_pin = models.CharField(max_length=30, blank=True)
    terminal_ref = models.CharField(max_length=100, blank=True)
    notes = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.wire_color} — Pin {self.device_pin} → {self.terminal_ref}"
