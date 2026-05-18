from django.db import models


class Crane(models.Model):
    name = models.CharField(max_length=100)
    model_number = models.CharField(max_length=50)
    serial_number = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.name} ({self.model_number})"


class ControlSystem(models.Model):
    crane = models.ForeignKey(Crane, on_delete=models.CASCADE, related_name='control_systems')
    name = models.CharField(max_length=100)
    model = models.CharField(max_length=50)
    supply_voltage_min = models.FloatField()
    supply_voltage_max = models.FloatField()
    safety_level = models.CharField(max_length=20)
    max_current_a = models.FloatField()
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} — {self.crane}"


class Connector(models.Model):
    control_system = models.ForeignKey(ControlSystem, on_delete=models.CASCADE, related_name='connectors')
    designation = models.CharField(max_length=10)
    color = models.CharField(max_length=20)
    connector_type = models.CharField(max_length=50)
    primary_role = models.TextField()

    def __str__(self):
        return f"{self.designation} ({self.color}) — {self.control_system.name}"


class Device(models.Model):
    DEVICE_TYPES = [
        ('sensor', 'Sensor'),
        ('actuator', 'Actuator'),
        ('switch', 'Switch / Limit Switch'),
        ('valve', 'Hydraulic Valve'),
        ('indicator', 'Indicator / Horn / Light'),
        ('relay', 'Relay'),
        ('fuse', 'Fuse'),
        ('other', 'Other'),
    ]
    identification = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    device_type = models.CharField(max_length=20, choices=DEVICE_TYPES)
    description = models.TextField(blank=True)
    cable = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.identification} — {self.name}"


class Pin(models.Model):
    SIGNAL_TYPES = [
        ('DI', 'Digital Input'),
        ('DO', 'Digital Output'),
        ('AI', 'Analog Input'),
        ('AO', 'Analog Output'),
        ('CAN', 'CAN Bus'),
        ('PWR', 'Power Supply'),
        ('GND', 'Ground'),
    ]
    DIRECTIONS = [
        ('IN', 'Input'),
        ('OUT', 'Output'),
        ('BIDI', 'Bidirectional'),
        ('REF', 'Reference / Return'),
    ]
    connector = models.ForeignKey(Connector, on_delete=models.CASCADE, related_name='pins')
    pin_number = models.IntegerField()
    function = models.CharField(max_length=200)
    signal_type = models.CharField(max_length=5, choices=SIGNAL_TYPES)
    direction = models.CharField(max_length=5, choices=DIRECTIONS)
    cable = models.CharField(max_length=20, blank=True)
    wire_color = models.CharField(max_length=30, blank=True)
    terminal = models.CharField(max_length=50, blank=True)
    device = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True, blank=True, related_name='pins')
    safety_related = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ('connector', 'pin_number')
        ordering = ['connector', 'pin_number']

    def __str__(self):
        return f"{self.connector.designation} Pin {self.pin_number} — {self.function}"


class SignalGroup(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    pins = models.ManyToManyField(Pin, related_name='signal_groups')

    def __str__(self):
        return self.name


class SafetyFunction(models.Model):
    SAFETY_LEVELS = [
        ('PL_c', 'PL c (IEC 13849)'),
        ('PL_d', 'PL d (IEC 13849)'),
        ('SIL_1', 'SIL 1'),
        ('SIL_2', 'SIL 2'),
    ]
    name = models.CharField(max_length=100)
    safety_level = models.CharField(max_length=10, choices=SAFETY_LEVELS)
    description = models.TextField()
    pins = models.ManyToManyField(Pin, related_name='safety_functions')
    reaction_time_ms = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.safety_level})"


class TroubleshootingNote(models.Model):
    pin = models.ForeignKey(Pin, on_delete=models.CASCADE, related_name='troubleshooting')
    symptom = models.CharField(max_length=200)
    likely_cause = models.CharField(max_length=200)
    diagnostic_procedure = models.TextField()

    def __str__(self):
        return f"[{self.pin}] {self.symptom}"
