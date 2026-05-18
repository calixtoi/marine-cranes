from django.core.management.base import BaseCommand
from pal40.models import Crane, ControlSystem, Connector, Device, Pin


DEVICES = [
    {"identification": "B310",  "name": "Slewing Sensor",           "device_type": "sensor",    "cable": "W310",
     "description": "Angle/position transducer with lever switch. Provides slewing direction commands and position feedback."},
    {"identification": "B312",  "name": "Main Boom Sensor",         "device_type": "sensor",    "cable": "W312",
     "description": "Angle/position transducer with lever switch. Measures main boom elevation angle for load radius calculation."},
    {"identification": "B314",  "name": "Knuckle Boom Sensor",      "device_type": "sensor",    "cable": "W314",
     "description": "Angle/position transducer with lever switch. Measures knuckle boom angle, used with B312 for geometry."},
    {"identification": "B316",  "name": "Extension Sensor",         "device_type": "sensor",    "cable": "W316",
     "description": "Position transducer with lever switch. Measures extension boom position for load radius calculation."},
    {"identification": "B318",  "name": "Winch Control",            "device_type": "sensor",    "cable": "W318",
     "description": "Lever switch assembly for winch hoist/lower commands. 4-wire: supply, GND, up, down."},
    {"identification": "Y0",    "name": "Emergency Stop Valve",     "device_type": "valve",     "cable": "W0",
     "description": "Normally-closed hydraulic solenoid valve. Blocks all crane hydraulic functions when de-energized. Dual-coil: crane enable (Pin 1) and support enable (Pin 2)."},
    {"identification": "H5",    "name": "Overload Horn",            "device_type": "indicator", "cable": "W5",
     "description": "Acoustic alarm activated when load exceeds programmed SWL threshold (typically 90-100%)."},
    {"identification": "H6",    "name": "Warning Horn",             "device_type": "indicator", "cable": "W6",
     "description": "General-purpose audible warning for remote control activation, zone warnings, and operator alerts."},
    {"identification": "H113",  "name": "Orange Flashing Beacon",   "device_type": "indicator", "cable": "W71",
     "description": "360-degree rotating/strobe beacon. Active during crane operation and remote control mode."},
    {"identification": "K56",   "name": "Working Light Relay",      "device_type": "relay",     "cable": "W71",
     "description": "Power relay switching the working light circuit. Protects PAL40 outputs from lamp inrush current."},
    {"identification": "F160",  "name": "Main Supply Fuse",         "device_type": "fuse",      "cable": "W70",
     "description": "Fuse protecting the main PAL40 logic and sensor supply input (UIN1) on C70 Pin 56."},
    {"identification": "F161",  "name": "Output Supply Fuse",       "device_type": "fuse",      "cable": "W71",
     "description": "Fuse protecting the PAL40 output driver supply input (UIN2) on C71 Pin 16."},
    {"identification": "DV1",   "name": "Auxiliary Directional Valve", "device_type": "valve",  "cable": "W71",
     "description": "Auxiliary hydraulic solenoid directional control valve for supplementary crane functions."},
]


# (pin_number, function, signal_type, direction, cable, wire_color, terminal, device_id, safety_related, description)
C70_PINS = [
    (1,  "Ground", "GND", "REF", "", "", "", None, False, "Chassis ground."),
    (2,  "Ground", "GND", "REF", "", "", "", None, False, "Chassis ground."),
    (3,  "Ground", "GND", "REF", "", "", "", None, False, "Chassis ground."),
    (4,  "Ground", "GND", "REF", "", "", "", None, False, "Chassis ground."),
    (5,  "Ground – B312 Mainboom sensor signal return", "GND", "REF", "W312", "YE", "B312 Pin 5", "B312", False,
         "Sensor signal ground return for main boom angle sensor B312. Routed through W312 harness."),
    (6,  "Ground – B310 Slewing sensor signal return", "GND", "REF", "W310", "YE", "B310 Pin 3", "B310", False,
         "Sensor signal ground return for slewing sensor B310. Routed through W310 harness."),
    (7,  "Ground", "GND", "REF", "", "", "", None, False, "Chassis ground."),
    (8,  "Ground", "GND", "REF", "", "", "", None, False, "Chassis ground."),
    (9,  "Ground", "GND", "REF", "", "", "", None, False, "Chassis ground."),
    (10, "Ground", "GND", "REF", "", "", "", None, False, "Chassis ground."),
    (11, "Ground", "GND", "REF", "", "", "", None, False, "Chassis ground."),
    (12, "Ground", "GND", "REF", "", "", "", None, False, "Chassis ground."),
    (13, "Ground", "GND", "REF", "", "", "", None, False, "Chassis ground."),
    (14, "Emergency stop – support enable", "DO", "OUT", "W0", "GN", "Y0 Pin 2", "Y0", True,
         "Drives the support-enable coil of emergency stop valve Y0 (Pin 2). De-energizing closes Y0 and halts all crane hydraulic motion."),
    (15, "CAN Bus 0 Low – slewing / outer boom / IO modules", "CAN", "BIDI", "W70", "YE", "Terminal 628", None, True,
         "CAN Bus 0 differential Low wire. Bus 0 connects slewing sensor, outer boom sensor, and peripheral I/O modules. ISO 11898."),
    (16, "External emergency stop chain 2", "DI", "IN", "W70", "BK", "Terminal 101", None, True,
         "Second channel of the dual-channel external E-stop safety chain (IEC 13849 PL c, Cat. 3). Low = E-stop active → Y0 de-energized."),
    (17, "External emergency stop chain 1", "DI", "IN", "W70", "GY", "Terminal 102", None, True,
         "First channel of the dual-channel external E-stop safety chain. Monitored independently from Pin 16 for cross-channel plausibility."),
    (18, "Knuckle boom up (LEVER)", "DI", "IN", "W314", "WH", "B314 Pin 1", "B314", False,
         "Lever command: knuckle boom raise. B314 Pin 1 (WH) goes active. PAL40 enables knuckle-boom-up hydraulic valve if load conditions allow."),
    (19, "Main boom up (LEVER)", "DI", "IN", "W312", "WH", "B312 Pin 1", "B312", False,
         "Lever command: main boom raise. B312 Pin 1 (WH) goes active. PAL40 validates against load moment before enabling valve."),
    (20, "Slewing left (LEVER)", "DI", "IN", "W310", "WH", "B310 Pin 1", "B310", False,
         "Lever command: crane rotation counter-clockwise (left). B310 Pin 1 (WH) goes active."),
    (21, "Top Stop – Stabilizer B (NC contact)", "DI", "IN", "", "", "", None, True,
         "Normally-closed limit switch: stabilizer B top-stop position. NC open = limit reached (fail-safe). Paired with Pin 35 (NO contact)."),
    (22, "FPI2 – Stabilizer A (NC contact)", "DI", "IN", "", "", "", None, True,
         "FPI2 normally-closed interlock: stabilizer A deployment confirm. NC open = stabilizer not in required position. Paired with Pin 36 (NO)."),
    (23, "End Layer Winch 2 – Boom A (NC contact)", "DI", "IN", "", "", "", None, True,
         "NC contact: winch 2 rope end-layer detection (minimum safe wraps). Fail-safe: open = end-layer reached. Paired with Pin 37 (NO)."),
    (24, "Overload Winch 2 – Boom B (NC contact)", "DI", "IN", "", "", "", None, True,
         "NC contact: winch 2 overload detection (excess rope tension). Fail-safe: open = overload detected. Paired with Pin 38 (NO)."),
    (25, "Pressure rod sensor (600 bar) – 4–20 mA wire A", "AI", "IN", "W70", "WH", "Terminal 105", None, True,
         "Wire A of the rod-side hydraulic pressure sensor current loop (0–600 bar, 4–20 mA). 4 mA=0 bar, 20 mA=600 bar. Loop return on Pin 39."),
    (26, "Pressure piston sensor (600 bar) – 4–20 mA wire A", "AI", "IN", "W70", "VT", "Terminal 103", None, True,
         "Wire A of the piston-side hydraulic pressure sensor current loop (0–600 bar, 4–20 mA). 4 mA=0 bar, 20 mA=600 bar. Loop return on Pin 40."),
    (27, "Ground – Y0 Emergency Stop Valve coil return", "GND", "REF", "W0", "YE", "Y0 Pin 3", "Y0", True,
         "Ground return for the Y0 emergency stop valve solenoid coil. Routed through W0 harness alongside Pins 14 and 28."),
    (28, "Emergency stop solenoid – crane enable", "DO", "OUT", "W0", "WH", "Y0 Pin 1", "Y0", True,
         "Main solenoid drive output to Y0 crane-enable coil (Pin 1). De-energized on overload, E-stop, CAN fault, or internal fault. Reaction < 20 ms."),
    (29, "CAN Bus 0 High – outer boom / slewing / IO modules", "CAN", "BIDI", "W70", "GN", "Terminal 629", None, True,
         "CAN Bus 0 differential High wire. Paired with Pin 15 (Low) for ISO 11898 Bus 0 differential pair."),
    (30, "Overload protection (OLP) input", "DI", "IN", "", "", "", None, True,
         "External overload protection interlock input. Can receive override or interlock signal from external OLP relay."),
    (31, "Pendulum (inclinometer)", "AI", "IN", "", "", "", None, True,
         "Vessel heel angle sensor input. Marine cranes use this to compensate load radius calculation for vessel inclination."),
    (32, "Knuckle boom down (LEVER)", "DI", "IN", "W314", "GN", "B314 Pin 2", "B314", False,
         "Lever command: knuckle boom lower. B314 Pin 2 (GN) goes active."),
    (33, "Main boom down (LEVER)", "DI", "IN", "W312", "GN", "B312 Pin 2", "B312", False,
         "Lever command: main boom lower. B312 Pin 2 (GN) goes active."),
    (34, "Slewing right (LEVER)", "DI", "IN", "W310", "GN", "B310 Pin 2", "B310", False,
         "Lever command: crane rotation clockwise (right). B310 Pin 2 (GN) goes active."),
    (35, "Top Stop – Stabilizer B (NO contact)", "DI", "IN", "", "", "", None, True,
         "Normally-open companion to Pin 21 (NC). Dual-contact monitoring detects welded/stuck contacts on stabilizer B top-stop switch."),
    (36, "FPI2 – Stabilizer A (NO contact)", "DI", "IN", "", "", "", None, True,
         "Normally-open companion to Pin 22 (NC). Dual-contact monitoring for stabilizer A FPI2 interlock."),
    (37, "End layer Winch 2 – Boom B (NO contact)", "DI", "IN", "", "", "", None, True,
         "Normally-open companion to Pin 23 (NC). Dual-contact monitoring for winch 2 end-layer detection."),
    (38, "Overload Winch 2 – Boom A (NO contact)", "DI", "IN", "", "", "", None, True,
         "Normally-open companion to Pin 24 (NC). Dual-contact monitoring for winch 2 overload detection."),
    (39, "Pressure rod sensor (600 bar) – 4–20 mA wire B", "AI", "IN", "W70", "GY/PK", "Terminal 106", None, True,
         "Wire B (return) of the rod-side pressure sensor 4–20 mA current loop. Completes the loop started at Pin 25 (Terminal 105)."),
    (40, "Pressure piston sensor (600 bar) – 4–20 mA wire B", "AI", "IN", "W70", "BN", "Terminal 104", None, True,
         "Wire B (return) of the piston-side pressure sensor 4–20 mA current loop. Completes the loop started at Pin 26 (Terminal 103)."),
    (41, "Ground – H5 Overload Horn return", "GND", "REF", "W5", "BK", "H5", "H5", False,
         "Ground return for overload horn H5. Both supply (Pin 42) and ground routed via PAL40 for full circuit control."),
    (42, "Horn H5 – overload horn drive", "DO", "OUT", "W5", "RD", "H5", "H5", False,
         "Output drive for overload horn H5. Activated when load exceeds SWL threshold. Ground return on Pin 41."),
    (43, "Protected battery supply (UIN1)", "PWR", "OUT", "", "", "", None, False,
         "Short-circuit-protected sensor supply output. Internal current limit protects PAL40 from wiring faults."),
    (44, "Protected battery supply", "PWR", "OUT", "", "", "", None, False, "Protected sensor supply output."),
    (45, "Protected battery supply", "PWR", "OUT", "", "", "", None, False, "Protected sensor supply output."),
    (46, "Protected battery supply – B314 Knuckleboom sensor", "PWR", "OUT", "W314", "BN", "B314 Pin 4", "B314", False,
         "Excitation supply to knuckle boom sensor B314 Pin 4 (BN wire). Part of 4-wire sensor connection: supply(BN), GND(YE), up(WH), down(GN)."),
    (47, "Protected battery supply – B312 Mainboom sensor", "PWR", "OUT", "W312", "BN", "B312 Pin 4", "B312", False,
         "Excitation supply to main boom sensor B312 Pin 4 (BN wire). Part of 4-wire sensor connection."),
    (48, "Protected battery supply – B310 Slewing sensor", "PWR", "OUT", "W310", "BN", "B310 Pin 4", "B310", False,
         "Excitation supply to slewing sensor B310 Pin 4 (BN wire). Part of 4-wire sensor connection."),
    (49, "Protected battery supply", "PWR", "OUT", "", "", "", None, False, "Protected sensor supply output."),
    (50, "Protected battery supply", "PWR", "OUT", "", "", "", None, False, "Protected sensor supply output."),
    (51, "Protected battery supply", "PWR", "OUT", "", "", "", None, False, "Protected sensor supply output."),
    (52, "Protected battery supply", "PWR", "OUT", "", "", "", None, False, "Protected sensor supply output."),
    (53, "Protected battery supply", "PWR", "OUT", "", "", "", None, False, "Protected sensor supply output."),
    (54, "Protected battery supply", "PWR", "OUT", "", "", "", None, False, "Protected sensor supply output."),
    (55, "Ground – W70 harness common (Terminal 800)", "GND", "REF", "W70", "BU", "Terminal 800", None, False,
         "Common signal ground for the W70 harness referenced to Terminal 800 bus bar."),
    (56, "Battery positive – main ECU supply (UIN1)", "PWR", "IN", "W70", "RD", "Terminal 160", "F160", False,
         "Main 12/24 V DC supply input to PAL40 logic and sensor regulators. Protected by fuse F160."),
]

C71_PINS = [
    (1,  "Ground", "GND", "REF", "", "", "", None, False, "Chassis ground."),
    (2,  "Ground – W71 harness common (Terminal 800)", "GND", "REF", "W71", "BU", "Terminal 800", None, False,
         "Common signal ground for the W71 harness referenced to Terminal 800 bus bar."),
    (3,  "Ground", "GND", "REF", "", "", "", None, False, "Chassis ground."),
    (4,  "Ground – H6 Warning Horn return", "GND", "REF", "W6", "BK", "H6", "H6", False,
         "Ground return for warning horn H6. Paired with supply drive on Pin 18."),
    (5,  "Ground", "GND", "REF", "", "", "", None, False, "Chassis ground."),
    (6,  "Ground", "GND", "REF", "", "", "", None, False, "Chassis ground."),
    (7,  "Ground", "GND", "REF", "", "", "", None, False, "Chassis ground."),
    (8,  "Ground", "GND", "REF", "", "", "", None, False, "Chassis ground."),
    (9,  "Ground – B316 Extension sensor signal return", "GND", "REF", "W316", "YE", "B316 Pin 3", "B316", False,
         "Sensor signal ground return for extension sensor B316. Routed through W316 harness."),
    (10, "Ground – B318 Winch sensor signal return", "GND", "REF", "W318", "YE", "B318 Pin 3", "B318", False,
         "Sensor signal ground return for winch control B318. Routed through W318 harness."),
    (11, "Ground", "GND", "REF", "", "", "", None, False, "Chassis ground."),
    (12, "Ground", "GND", "REF", "", "", "", None, False, "Chassis ground."),
    (13, "Ground", "GND", "REF", "", "", "", None, False, "Chassis ground."),
    (14, "Ground", "GND", "REF", "", "", "", None, False, "Chassis ground."),
    (15, "CAN Bus 1 Low – Remote control / telemetry / Main Boom", "CAN", "BIDI", "W71", "YE", "Terminal 620", None, True,
         "CAN Bus 1 differential Low wire. Bus 1 connects RRC receiver, telematics module, and main boom CAN sensor node. Isolated from Bus 0."),
    (16, "Battery positive supply – UIN2 (Paltronic outputs)", "PWR", "IN", "W71", "RD", "Terminal 161", "F161", False,
         "Secondary 12/24 V DC supply for PAL40 output drivers (horns, lights, valves). Protected by fuse F161. Separate from UIN1 logic supply."),
    (17, "Warning beacon – H113 flashing light (RRC)", "DO", "OUT", "W71", "BN", "Terminal 111", "H113", False,
         "Output drives orange flashing beacon H113. Active during crane operation and remote control mode. 360-degree visibility."),
    (18, "Warning Horn H6", "DO", "OUT", "W6", "RD", "H6", "H6", False,
         "Output drives warning horn H6 for general alerts (RRC activation, zone entry). Ground return on Pin 4."),
    (19, "100% load indicator – Utilization / FPO1", "DO", "OUT", "", "", "", None, False,
         "FPO1 (Free Programmable Output 1): activates when load reaches 100% SWL. Drives load-at-limit indicator."),
    (20, "90% load indicator – Utilization / FPO2", "DO", "OUT", "", "", "", None, False,
         "FPO2 (Free Programmable Output 2): activates when load reaches 90% SWL. Early warning before overload trip."),
    (21, "Working light – K56 relay coil", "DO", "OUT", "W71", "BK", "K56/A1", "K56", False,
         "Drives coil of relay K56. K56 contacts switch the high-current working light circuit."),
    (22, "Load Limit C out", "DO", "OUT", "", "", "", None, False,
         "Output signal indicating Load Limit C profile is currently active. Signals external equipment of selected SWL profile."),
    (23, "Extension boom retract (LEVER)", "DI", "IN", "W316", "GN", "B316 Pin 1", "B316", False,
         "Lever command: extension boom retract (telescope in). B316 Pin 1 (GN) goes active."),
    (24, "Winch down (LEVER)", "DI", "IN", "W318", "WH", "B318 Pin 2", "B318", False,
         "Lever command: winch lower (pay out rope). B318 Pin 2 (WH) goes active. Validated against end-layer and overload conditions."),
    (25, "SE end position (NO) – End layer winch 1", "DI", "IN", "", "", "", None, True,
         "Normally-open contact: winch 1 end-layer (minimum rope wraps on drum). Paired with Pin 39 (NC) for dual-contact monitoring."),
    (26, "SE overload (NO) – Winch 1", "DI", "IN", "W71", "WH", "Terminal 109", None, True,
         "Normally-open contact: winch 1 overload (excess rope tension). Halts hoisting to prevent rope/sheave damage. Paired with Pin 40 (NC)."),
    (27, "Load limit C select (NO)", "DI", "IN", "", "", "", None, False,
         "Normally-open contact: Load Limit C profile selector. Closes to activate reduced SWL profile C. Paired with Pin 41 (NC)."),
    (28, "FPI1 (NO contact)", "DI", "IN", "", "", "", None, True,
         "FPI1 normally-open contact: stabilizer A deployment interlock. Paired with Pin 42 (NC) for dual-contact monitoring."),
    (29, "CAN Bus 1 High – Remote control / telemetry / Main Boom", "CAN", "BIDI", "W71", "GN", "Terminal 621", None, True,
         "CAN Bus 1 differential High wire. Paired with Pin 15 (Low) for ISO 11898 Bus 1 differential pair."),
    (30, "CAN Bus 1 termination (stirrup)", "CAN", "REF", "", "Stirrup", "", None, False,
         "120 Ω CAN Bus 1 termination resistor point. Stirrup connects internal terminator. One of two terminators required on Bus 1."),
    (31, "DV1 – auxiliary directional valve drive", "DO", "OUT", "W71", "GY", "Terminal 15", "DV1", False,
         "Output drive for auxiliary hydraulic directional valve DV1. Used for supplementary crane functions or circuit mode selection."),
    (32, "Override button / 2nd Hand", "DI", "IN", "", "", "", None, False,
         "Override / second-operator enable button. Allows controlled bypass of normal restrictions. All activations are logged by PAL40."),
    (33, "Rotator left (LEVER)", "DI", "IN", "", "", "", None, False,
         "Lever command: hydraulic rotator counter-clockwise. Optional end-of-line accessory function."),
    (34, "Rotator right (LEVER)", "DI", "IN", "", "", "", None, False,
         "Lever command: hydraulic rotator clockwise. Optional end-of-line accessory function."),
    (35, "Open grapple (LEVER)", "DI", "IN", "", "", "", None, False,
         "Lever command: open hydraulic grapple/grab. Optional attachment function."),
    (36, "Close grapple (LEVER)", "DI", "IN", "", "", "", None, False,
         "Lever command: close hydraulic grapple/grab. Optional attachment function."),
    (37, "Extension boom out (LEVER)", "DI", "IN", "W316", "WH", "B316 Pin 2", "B316", False,
         "Lever command: extension boom extend (telescope out). B316 Pin 2 (WH) goes active. Extending increases load radius; PAL40 re-checks SWL continuously."),
    (38, "Winch up (LEVER)", "DI", "IN", "W318", "GN", "B318 Pin 1", "B318", False,
         "Lever command: winch hoist (pull in rope). B318 Pin 1 (GN) goes active."),
    (39, "End layer winch 1 (NC)", "DI", "IN", "", "", "", None, True,
         "Normally-closed companion to Pin 25 (NO). NC opens on end-layer condition: fail-safe (broken wire = limit active). Dual-contact monitoring."),
    (40, "Overload winch 1 (NC)", "DI", "IN", "W71", "BU/RD", "Terminal 140", None, True,
         "Normally-closed companion to Pin 26 (NO). NC opens on winch overload: fail-safe. Dual-contact cross-check with Pin 26."),
    (41, "Load limit C select (NC)", "DI", "IN", "", "", "", None, False,
         "Normally-closed companion to Pin 27 (NO). Dual-contact monitoring for Load Limit C selector switch."),
    (42, "FPI1 (NC contact)", "DI", "IN", "", "", "", None, True,
         "FPI1 normally-closed companion to Pin 28 (NO). Dual-contact monitoring confirms stabilizer A deployment reliably."),
    (43, "Protected battery supply", "PWR", "OUT", "", "", "", None, False, "Protected sensor supply output."),
    (44, "Protected battery supply / CAN termination", "PWR", "OUT", "", "Stirrup", "", None, False,
         "Protected supply output. Also coincides with CAN Bus 1 termination stirrup point in this connector."),
    (45, "Protected battery supply", "PWR", "OUT", "", "", "", None, False, "Protected sensor supply output."),
    (46, "Protected battery supply", "PWR", "OUT", "", "", "", None, False, "Protected sensor supply output."),
    (47, "Protected battery supply", "PWR", "OUT", "", "", "", None, False, "Protected sensor supply output."),
    (48, "Protected battery supply", "PWR", "OUT", "", "", "", None, False, "Protected sensor supply output."),
    (49, "Protected battery supply", "PWR", "OUT", "", "", "", None, False, "Protected sensor supply output."),
    (50, "Protected battery supply", "PWR", "OUT", "", "", "", None, False, "Protected sensor supply output."),
    (51, "Protected battery supply – B316 Extension sensor", "PWR", "OUT", "W316", "BN", "B316 Pin 4", "B316", False,
         "Excitation supply to extension sensor B316 Pin 4 (BN wire). Part of 4-wire sensor connection."),
    (52, "Protected battery supply – B318 Winch sensor", "PWR", "OUT", "W318", "BN", "B318 Pin 4", "B318", False,
         "Excitation supply to winch control B318 Pin 4 (BN wire). Part of 4-wire sensor connection."),
    (53, "Protected battery supply", "PWR", "OUT", "", "", "", None, False, "Protected sensor supply output."),
    (54, "Protected battery supply", "PWR", "OUT", "", "", "", None, False, "Protected sensor supply output."),
    (55, "Protected battery supply", "PWR", "OUT", "", "", "", None, False, "Protected sensor supply output."),
    (56, "Protected battery supply", "PWR", "OUT", "", "", "", None, False, "Protected sensor supply output."),
]


class Command(BaseCommand):
    help = "Load all PAL40 connector, pin, and device data into the database"

    def add_arguments(self, parser):
        parser.add_argument("--flush", action="store_true", help="Delete existing data before loading")

    def handle(self, *args, **options):
        if options["flush"]:
            self.stdout.write("Flushing existing PAL40 data...")
            Pin.objects.all().delete()
            Connector.objects.all().delete()
            ControlSystem.objects.all().delete()
            Crane.objects.all().delete()
            Device.objects.all().delete()

        # --- Devices ---
        self.stdout.write("Creating devices...")
        device_map = {}
        for d in DEVICES:
            obj, created = Device.objects.update_or_create(
                identification=d["identification"],
                defaults={
                    "name": d["name"],
                    "device_type": d["device_type"],
                    "cable": d["cable"],
                    "description": d["description"],
                },
            )
            device_map[d["identification"]] = obj
            self.stdout.write(f"  {'Created' if created else 'Updated':8s} {obj}")

        # --- Crane + ControlSystem ---
        self.stdout.write("Creating crane and control system...")
        crane, _ = Crane.objects.update_or_create(
            model_number="PAL40",
            defaults={"name": "PALFINGER Marine Crane", "serial_number": ""},
        )
        cs, _ = ControlSystem.objects.update_or_create(
            crane=crane,
            model="PAL40",
            defaults={
                "name": "PALTRONIC 40",
                "supply_voltage_min": 8.0,
                "supply_voltage_max": 32.0,
                "safety_level": "PL c",
                "max_current_a": 10.0,
                "description": (
                    "Main electronic overload protection and crane motion control ECU. "
                    "Monitors boom geometry, hydraulic pressure, and safety interlocks. "
                    "Controls the emergency stop valve Y0 to enforce SWL limits. "
                    "Two CAN buses: Bus 0 (C70) for internal machine, Bus 1 (C71) for remote control and telematics."
                ),
            },
        )

        # --- Connectors + Pins ---
        connectors = [
            ("C70", "Blue",  "56-pin Molex",
             "Primary motion control and safety interface. Carries main boom lever commands, "
             "hydraulic pressure sensor inputs (4-20 mA), CAN Bus 0, emergency stop chain, "
             "overload horn, and main battery supply.",
             C70_PINS),
            ("C71", "Grey",  "56-pin Molex",
             "Auxiliary, remote control, and load indication interface. Carries CAN Bus 1 "
             "(RRC, telematics), warning outputs, winch safety inputs, extension lever commands, "
             "and secondary battery supply for output drivers.",
             C71_PINS),
        ]

        for desig, color, ctype, role, pin_data in connectors:
            self.stdout.write(f"Creating connector {desig}...")
            conn, _ = Connector.objects.update_or_create(
                control_system=cs,
                designation=desig,
                defaults={"color": color, "connector_type": ctype, "primary_role": role},
            )
            created_count = 0
            for row in pin_data:
                (pnum, func, sig, direction, cable, wire, terminal,
                 dev_id, safety, desc) = row
                device = device_map.get(dev_id) if dev_id else None
                _, created = Pin.objects.update_or_create(
                    connector=conn,
                    pin_number=pnum,
                    defaults={
                        "function": func,
                        "signal_type": sig,
                        "direction": direction,
                        "cable": cable,
                        "wire_color": wire,
                        "terminal": terminal,
                        "device": device,
                        "safety_related": safety,
                        "description": desc,
                    },
                )
                if created:
                    created_count += 1
            self.stdout.write(
                f"  {desig}: {created_count} pins created, "
                f"{len(pin_data) - created_count} updated"
            )

        total = Pin.objects.count()
        self.stdout.write(self.style.SUCCESS(
            f"\nDone. {total} pins loaded across {Connector.objects.count()} connectors."
        ))
