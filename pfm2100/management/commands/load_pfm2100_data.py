from django.core.management.base import BaseCommand
from pfm2100.models import PFM2100Device, PFM2100Cable, PFM2100WireTerminal

# ──────────────────────────────────────────────────────────────────────────────
# DATA — each entry: (order, part_number, description, classification,
#   designation, type_function, signal_form, details, classification_notes,
#   connector_type, connector_part_number,
#   cables: [ (cable_id, cable_part_number, connection_details, junction_box_ref, notes,
#              wires: [(order, wire_color, device_pin, terminal_ref, notes), ...] ) ] )
# ──────────────────────────────────────────────────────────────────────────────
DEVICES = [
    {
        "order": 1,
        "device_ref": "U205",
        "part_number": "EEA18563",
        "description": "Slewing Encoder",
        "classification": "Analogue Sensor",
        "designation": "Rotary encoder TBN58-SA16384 (CANopen Safety SIL2)",
        "type_function": "Absolute monotour magnetic encoder for slewing angle measurement",
        "signal_form": "CANopen Safety SIL2 digital",
        "details": "(4-pole, A-coded), 3 m length\n[pins: 1 +Vs, 2 0 V, 3 CAN+, 4 CAN–]",
        "classification_notes": "Provides rotation and speed signals to controller; SIL2 certified",
        "connector_type": "M12",
        "connector_part_number": "EEA3900",
        "cables": [
            {
                "cable_id": "W205",
                "cable_part_number": "EEA12216",
                "connection_details": "2 × 2 × 0.34 mm²",
                "junction_box_ref": "Junction Box (XX3)",
                "notes": "CANopen Bus 0: CAN H → Terminal 628, CAN L → Terminal 629",
                "wires": [
                    (1, "RD", "Pin 1", "Terminal 160", "Supply +Vs"),
                    (2, "BK", "Pin 2", "Terminal 800", "Ground 0 V"),
                    (3, "YE", "Pin 3", "Terminal 629", "CAN Low (Bus 0)"),
                    (4, "GN", "Pin 4", "Terminal 628", "CAN High (Bus 0)"),
                ],
            }
        ],
    },
    {
        "order": 2,
        "device_ref": "U206",
        "part_number": "EEA14709",
        "description": "Mainboom Angle Sensor",
        "classification": "Analogue Sensor",
        "designation": "Rotary encoder TBN25-MS16384 (CANopen Safety SIL2)",
        "type_function": "Absolute magnetic encoder for boom position feedback",
        "signal_form": "CANopen Safety SIL2 digital",
        "details": "(4-pole, A-coded), 7 m length",
        "classification_notes": "Feeds boom angle data to PALTRONIC system; redundant SIL2 outputs",
        "connector_type": "M16",
        "connector_part_number": "EEA3901",
        "cables": [
            {
                "cable_id": "W206",
                "cable_part_number": "EEA13797",
                "connection_details": "2 × 2 × 0.34 mm²",
                "junction_box_ref": "Junction Box (XX3)",
                "notes": "CANopen Bus 1: CAN H → Terminal 620, CAN L → Terminal 621",
                "wires": [
                    (1, "RD", "Pin 1", "Terminal 160", "Supply +Vs"),
                    (2, "BU", "Pin 2", "Terminal 800", "Ground 0 V"),
                    (3, "YE", "Pin 3", "Terminal 621", "CAN Low (Bus 1)"),
                    (4, "GN", "Pin 4", "Terminal 620", "CAN High (Bus 1)"),
                ],
            }
        ],
    },
    {
        "order": 3,
        "device_ref": "U207",
        "part_number": "EEA14709",
        "description": "Knuckleboom Angle Sensor",
        "classification": "Analogue Sensor",
        "designation": "Rotary encoder TBN25-MS16384 (CANopen Safety SIL2)",
        "type_function": "Absolute magnetic encoder for boom position feedback",
        "signal_form": "CANopen Safety SIL2 digital",
        "details": "(4-pole, A-coded), 7 m length",
        "classification_notes": "Feeds boom angle data to PALTRONIC system; redundant SIL2 outputs",
        "connector_type": "M16",
        "connector_part_number": "EEA3901",
        "cables": [
            {
                "cable_id": "W207",
                "cable_part_number": "EEA13797",
                "connection_details": "2 × 2 × 0.34 mm²",
                "junction_box_ref": "Junction Box (XX4)",
                "notes": (
                    "Routes via intermediate cable W25 (EEA5503) to CANBUS Junction Box (XX3).\n"
                    "W25 WH → CAN H Terminal 628; GN → CAN L Terminal 629."
                ),
                "wires": [
                    (1, "RD", "Pin 1", "Terminal 160", "Supply +Vs"),
                    (2, "BU", "Pin 2", "Terminal 800", "Ground 0 V"),
                    (3, "YE", "Pin 3", "Terminal 629 (via W25)", "CAN Low (Bus 0)"),
                    (4, "GN", "Pin 4", "Terminal 628 (via W25)", "CAN High (Bus 0)"),
                ],
            }
        ],
    },
    {
        "order": 4,
        "device_ref": "U409",
        "part_number": "EEA18779",
        "description": "Pressure Sensor — Piston Side",
        "classification": "Analogue Sensor",
        "designation": "Pressure transducer HPT 1746-CC (600 bar SIL2/PL d)",
        "type_function": "Dual-channel strain-gauge sensor for hydraulic monitoring",
        "signal_form": "Analogue 4–20 mA (+ inverse 20–4 mA)",
        "details": "[pins: 1 +Ub, 2 0 V, 3 Sig 1, 4 Sig 2]",
        "classification_notes": "Measures hydraulic pressure for LMI; dual outputs for redundant safety",
        "connector_type": "M20",
        "connector_part_number": "EEA3705",
        "cables": [
            {
                "cable_id": "W409",
                "cable_part_number": "EEA12759",
                "connection_details": "4 × 0.34 mm²",
                "junction_box_ref": "Junction Box (XX3) → location XX4",
                "notes": "Resistor R2 across terminals 628 and 629. Piston-side cylinder pressure.",
                "wires": [
                    (1, "BN",     "Pin 1", "Terminal 160", "Supply +Ub"),
                    (2, "WH",     "Pin 2", "Terminal 103", "Signal 1 — 4–20 mA (C70 Pin 26)"),
                    (3, "BU",     "Pin 3", "Terminal 800", "Ground 0 V"),
                    (4, "BK",     "Pin 4", "Terminal 104", "Signal 2 — 20–4 mA (C70 Pin 40)"),
                    (5, "Screen", "—",     "PE Terminal",  "Terminate screen on PE-Terminal"),
                ],
            }
        ],
    },
    {
        "order": 5,
        "device_ref": "U411",
        "part_number": "EEA18779",
        "description": "Pressure Sensor — Rod Side",
        "classification": "Analogue Sensor",
        "designation": "Pressure transducer HPT 1746-CC (600 bar SIL2/PL d)",
        "type_function": "Dual-channel strain-gauge sensor for hydraulic monitoring",
        "signal_form": "Analogue 4–20 mA (+ inverse 20–4 mA)",
        "details": "[pins: 1 +Ub, 2 0 V, 3 Sig 1, 4 Sig 2]",
        "classification_notes": "Measures hydraulic pressure for LMI; dual outputs for redundant safety",
        "connector_type": "M20",
        "connector_part_number": "EEA3705",
        "cables": [
            {
                "cable_id": "W411",
                "cable_part_number": "EEA12759",
                "connection_details": "4 × 0.34 mm²",
                "junction_box_ref": "Junction Box (XX3) → location XX4",
                "notes": "Rod-side cylinder pressure. Paired with W409 for differential load calculation.",
                "wires": [
                    (1, "BN",     "Pin 1", "Terminal 160", "Supply +Ub"),
                    (2, "WH",     "Pin 2", "Terminal 105", "Signal 1 — 4–20 mA (C70 Pin 25)"),
                    (3, "BU",     "Pin 3", "Terminal 800", "Ground 0 V"),
                    (4, "BK",     "Pin 4", "Terminal 106", "Signal 2 — 20–4 mA (C70 Pin 39)"),
                    (5, "Screen", "—",     "PE Terminal",  "Terminate screen on PE-Terminal"),
                ],
            }
        ],
    },
    {
        "order": 6,
        "device_ref": "B9",
        "part_number": "EEA12214",
        "description": "Winch Overload Switch",
        "classification": "Binary Sensor",
        "designation": "Inductive proximity XS1 sensor",
        "type_function": "Metal target detection for winch overload limit switch",
        "signal_form": "Digital ON/OFF",
        "details": "(4-pole, A-coded), 10 m length",
        "classification_notes": "Safety PL d rated binary switch for end-stop and overload monitoring",
        "connector_type": "M12",
        "connector_part_number": "EEA3900",
        "cables": [
            {
                "cable_id": "W9",
                "cable_part_number": "CPEE0400",
                "connection_details": "4 × 0.34 mm²",
                "junction_box_ref": "Junction Box (XX4)",
                "notes": "Screened cable. Screen connected to PE terminal.",
                "wires": [
                    (1, "BN",     "Pin 1", "Terminal 160", "Supply +Ub"),
                    (2, "WH",     "Pin 2", "Terminal 140", "Signal NC contact (C71 Pin 40)"),
                    (3, "BU",     "Pin 3", "Terminal 800", "Ground 0 V"),
                    (4, "BK",     "Pin 4", "Terminal 109", "Signal NO contact (C71 Pin 26)"),
                    (5, "Screen", "—",     "PE Terminal",  "Cable screen / earth"),
                ],
            }
        ],
    },
    {
        "order": 7,
        "device_ref": "Y190",
        "part_number": "EEA15740",
        "description": "Return Oil Utilization Valve",
        "classification": "Electromechanical Device",
        "designation": "Solenoid Coil Bosch Rexroth D36 — 24 VDC 17 W Class H",
        "type_function": "Hydraulic valve actuation coil",
        "signal_form": "Digital ON/OFF coil current 24 V DC",
        "details": "—",
        "classification_notes": "Activates return oil flow valve via electromagnetic control",
        "connector_type": "M12",
        "connector_part_number": "EEA3900",
        "cables": [
            {
                "cable_id": "W190",
                "cable_part_number": "EEA 169",
                "connection_details": "2 × 1.0 mm²",
                "junction_box_ref": "Junction Box (XX4)",
                "notes": "Coil supply from Terminal 190 (dedicated valve supply rail).",
                "wires": [
                    (1, "BN", "Pin 1", "Terminal 190", "Coil supply +24 V"),
                    (2, "BU", "Pin 2", "Terminal 800", "Coil ground 0 V"),
                ],
            }
        ],
    },
    {
        "order": 8,
        "device_ref": "H113",
        "part_number": "EEA17497",
        "description": "Flashlight (LED Strobe Beacon)",
        "classification": "Electrically Powered Equipment (Lighting)",
        "designation": "LED Strobe Beacon PDH-S23 (orange)",
        "type_function": "Visual warning light, 9–36 V DC",
        "signal_form": "Digital ON/OFF flashing signal",
        "details": "(5-pin), 10 m length\n[pins: 3 common, 4 +VDC]",
        "classification_notes": "Provides visual alert for warning and status; IP69 protection",
        "connector_type": "M12",
        "connector_part_number": "EEA3900",
        "cables": [
            {
                "cable_id": "W113",
                "cable_part_number": "CPEE0400",
                "connection_details": "4 × 0.34 mm²",
                "junction_box_ref": "Junction Box (XX3)",
                "notes": (
                    "Control signal routed via W71 (C71 Molex Grey):\n"
                    "  W71 BN → C71 Pin 17 (Warning beacon output).\n"
                    "Power pins (BN, WH) terminated with shrink sleeves at beacon end."
                ),
                "wires": [
                    (1, "BN",  "Pin 3 (common)", "Shrink sleeve", "Common/neutral"),
                    (2, "BU",  "Pin 2",           "Terminal 800",  "Ground 0 V"),
                    (3, "WH",  "—",               "Shrink sleeve", "Unused / power"),
                    (4, "BK",  "Pin 1",           "Terminal 111",  "Activated from PAL40 output"),
                ],
            }
        ],
    },
    {
        "order": 9,
        "device_ref": "H170",
        "part_number": "EEA13611",
        "description": "Floodlight 1",
        "classification": "Electrically Powered Equipment (Lighting)",
        "designation": "LED Floodlight RokLUME 380 N (24 V DC, 84 W)",
        "type_function": "High-power illumination for crane work area",
        "signal_form": "Constant 24 V DC supply",
        "details": "10 m each",
        "classification_notes": "Provides wide-area lighting; non-signal powered equipment",
        "connector_type": "M16",
        "connector_part_number": "EEA3901",
        "cables": [
            {
                "cable_id": "W170",
                "cable_part_number": "EEA 170",
                "connection_details": "2 × 1.5 mm²",
                "junction_box_ref": "Junction Box (XX4)",
                "notes": "Routed via intermediate cable W26 (EEA 192).",
                "wires": [
                    (1, "RD", "Pin 1", "Terminal 56",  "Supply +24 V"),
                    (2, "BU", "Pin 2", "Terminal 806", "Ground 0 V"),
                    (3, "PK", "—",     "Terminal 56",  "Additional supply connection"),
                ],
            }
        ],
    },
    {
        "order": 10,
        "device_ref": "H171",
        "part_number": "EEA13611",
        "description": "Floodlight 2",
        "classification": "Electrically Powered Equipment (Lighting)",
        "designation": "LED Floodlight RokLUME 380 N (24 V DC, 84 W)",
        "type_function": "High-power illumination for crane work area",
        "signal_form": "Constant 24 V DC supply",
        "details": "10 m each",
        "classification_notes": "Provides wide-area lighting; non-signal powered equipment",
        "connector_type": "M16",
        "connector_part_number": "EEA3901",
        "cables": [
            {
                "cable_id": "W171",
                "cable_part_number": "EEA 170",
                "connection_details": "2 × 1.5 mm²",
                "junction_box_ref": "Junction Box (XX4)",
                "notes": "Routed via intermediate cable W26 (EEA 192).",
                "wires": [
                    (1, "RD", "Pin 1", "Terminal 56",  "Supply +24 V"),
                    (2, "BU", "Pin 2", "Terminal 806", "Ground 0 V"),
                    (3, "BK", "—",     "Terminal 56",  "Additional supply connection"),
                ],
            }
        ],
    },
    {
        "order": 11,
        "device_ref": "H172",
        "part_number": "EEA11854",
        "description": "Working Light",
        "classification": "Electrically Powered Equipment (Lighting)",
        "designation": "LED Work Light Scorpius N4402 (9–32 V DC, 50 W)",
        "type_function": "Close-range illumination for control zones",
        "signal_form": "Constant DC supply (12–24 V)",
        "details": "15.4 m",
        "classification_notes": "Electrically powered lighting equipment for visibility in dark areas",
        "connector_type": "M16",
        "connector_part_number": "EEA3901",
        "cables": [
            {
                "cable_id": "W172",
                "cable_part_number": "EEA 170",
                "connection_details": "2 × 1.5 mm²",
                "junction_box_ref": "Junction Box (XX3)",
                "notes": (
                    "Switched via relay K56.\n"
                    "Control: C71 Pin 21 (working light output) → K56 relay coil (A1/A2) → relay contacts.\n"
                    "K56 A2 → Terminal 800. Relay contact pins: 11 → Terminal 163, 14 → Terminal 56.\n"
                    "24 → Terminal 56. Pin 21 → C71 Molex Grey."
                ),
                "wires": [
                    (1, "RD", "Pin 1",            "Terminal 56",   "Supply +24 V"),
                    (2, "BU", "Pin 2",            "Terminal 806",  "Ground 0 V"),
                    (3, "—",  "K56 Relay Coil A1","Terminal 163",  "Relay coil positive (from C71 Pin 21)"),
                    (4, "—",  "K56 Relay Coil A2","Terminal 800",  "Relay coil negative"),
                    (5, "—",  "K56 Contact 11",   "Terminal 163",  "Relay NC contact"),
                    (6, "—",  "K56 Contact 14",   "Terminal 56",   "Relay common"),
                    (7, "—",  "K56 Contact 24",   "Terminal 56",   "Relay NO contact"),
                ],
            }
        ],
    },
    {
        "order": 12,
        "device_ref": "U900",
        "part_number": "EEA15360",
        "description": "Telematic Unit CS100 IoT Gateway",
        "classification": "Communication Device / Analogue Processor",
        "designation": "Danfoss CS100 IoT Gateway",
        "type_function": "CAN data, GNSS telemetry connection for remote monitoring",
        "signal_form": "CAN bus / LTE / 2G data transfer digital",
        "details": "5 m length\n[pins: 1 GND, 2 V+, 3/4 CAN1 H/L, 7/8 CAN2 H/L]",
        "classification_notes": "Provides machine data transmission and fault logs via CAN and cellular",
        "connector_type": "M16",
        "connector_part_number": "EEA3901",
        "cables": [
            {
                "cable_id": "W900",
                "cable_part_number": "Part of U900",
                "connection_details": "4 × 0.34 mm²",
                "junction_box_ref": "Junction Box (XX3)",
                "notes": (
                    "Also connected via W71 (C71 Molex Grey):\n"
                    "  Terminal 621 → CAN1 High; Terminal 620 → CAN1 Low.\n"
                    "Slip ring W71: BN→Terminal 631, GN→Terminal 631, YE→Terminal 630, WH→Terminal 630."
                ),
                "wires": [
                    (1, "BU", "Pin 1", "Terminal 800",   "Ground 0 V"),
                    (2, "RD", "Pin 2", "Fuse 900",       "Supply +V (fused)"),
                    (3, "GN", "Pin 3", "Terminal 621",   "CAN1 High"),
                    (4, "YE", "Pin 4", "Terminal 620",   "CAN1 Low"),
                    (5, "—",  "Pin 5", "Blind",           "Unused — blind heat shrink"),
                    (6, "—",  "Pin 6", "Blind",           "Unused — blind heat shrink"),
                    (7, "—",  "Pin 7", "Blind",           "Unused — blind heat shrink"),
                    (8, "—",  "Pin 8", "Blind",           "Unused — blind heat shrink"),
                ],
            }
        ],
    },
    {
        "order": 13,
        "device_ref": "SRU1",
        "part_number": "CPEE0508A",
        "description": "Slip Ring Unit",
        "classification": "Auxiliary Device",
        "designation": "Slip ring unit for CAN and power transmission through rotating crane joint",
        "type_function": "Passive transfer, no signal change",
        "signal_form": "Ensures continuous data and power communication across slewing axis",
        "details": "—",
        "classification_notes": "—",
        "connector_type": "—",
        "connector_part_number": "—",
        "cables": [
            {
                "cable_id": "Integrated",
                "cable_part_number": "—",
                "connection_details": "5 × 2.5 mm² + 2 × 2 × 0.5 mm² (CAN Bus and Power Lines)",
                "junction_box_ref": "XX2, X106 via Cables 2.2, 3.2 and 4.2",
                "notes": "Passive slip ring. Continuously transfers CAN data and power across slewing axis with no signal conditioning.",
                "wires": [
                    (1, "BN",    "Terminal 631", "—",           "Power / CAN line"),
                    (2, "GN",    "Terminal 631", "—",           "Power / CAN line"),
                    (3, "YE",    "Terminal 630", "—",           "CAN Bus line"),
                    (4, "WH",    "Terminal 630", "—",           "CAN Bus line"),
                    (5, "3",     "Terminal 806", "—",           "Power line"),
                    (6, "1",     "Terminal 805", "—",           "Power line"),
                    (7, "2",     "Terminal 801", "—",           "Power line"),
                    (8, "4",     "Terminal 800", "—",           "Ground"),
                    (9, "GN/YE", "PE",           "—",           "Protective earth"),
                ],
            }
        ],
    },
    {
        "order": 14,
        "device_ref": "Y0",
        "part_number": "EEA 773",
        "description": "Emergency Stop Valve Plug (Y0)",
        "classification": "Safety Control Device",
        "designation": "Plug GAN-2000 PE2 LED 24 SD PAL (3 m)",
        "type_function": "Emergency stop valve connector with LED and suppression diode",
        "signal_form": "Digital ON/OFF signal (24 V DC)",
        "details": "PUR, shieldless, with Molding GAN-2000 plug 3 m",
        "classification_notes": "Provides safe valve shutdown and visual LED feedback for E-stop (Y0)",
        "connector_type": "—",
        "connector_part_number": "—",
        "cables": [
            {
                "cable_id": "W0",
                "cable_part_number": "EEA4379",
                "connection_details": "3 × 0.75 mm²",
                "junction_box_ref": "C70 Molex Blue",
                "notes": (
                    "Connects directly to PAL40 C70 connector.\n"
                    "Y0 is the main emergency stop hydraulic valve (normally closed).\n"
                    "BN pin (unused) terminated blind."
                ),
                "wires": [
                    (1, "GN", "Pin 14 (C70)", "Y0 Pin 2 — Support enable",      "E-stop support enable output"),
                    (2, "WH", "Pin 28 (C70)", "Y0 Pin 1 — Crane enable",         "Main crane enable solenoid output"),
                    (3, "YE", "Pin 27 (C70)", "Y0 Pin 3 — Coil ground return",   "Ground return for Y0 coil"),
                    (4, "BN", "—",            "Blind (unused)",                  "Spare / unused"),
                ],
            }
        ],
    },
    {
        "order": 15,
        "device_ref": "H5",
        "part_number": "EEA6193",
        "description": "Overload Horn (H5)",
        "classification": "Binary Device (Acoustic)",
        "designation": "Piezo Horn HU 90C10-100VB-05 B",
        "type_function": "Audible alert for load or fault conditions",
        "signal_form": "Digital ON/OFF (12/24 V DC)",
        "details": "1 m, 2-wire (red + / black –)",
        "classification_notes": "Activates under overload conditions; IP67; constant tone 90 dB",
        "connector_type": "—",
        "connector_part_number": "—",
        "cables": [
            {
                "cable_id": "W5",
                "cable_part_number": "Part of H5",
                "connection_details": "2 × 0.5 mm²",
                "junction_box_ref": "C70 Molex Blue",
                "notes": "Direct connection to PAL40 C70. Activated when load ≥ SWL threshold.",
                "wires": [
                    (1, "RD", "Pin 42 (C70)", "H5 supply terminal", "Horn drive output from PAL40"),
                    (2, "BK", "Pin 41 (C70)", "H5 ground terminal", "Ground return for H5 horn"),
                ],
            }
        ],
    },
    {
        "order": 16,
        "device_ref": "H6",
        "part_number": "EEA6194",
        "description": "Warning Horn (H6)",
        "classification": "Binary Device (Acoustic)",
        "designation": "Speaker-type alarm BUS 102C9-30VBW-02 B",
        "type_function": "General warning signal horn",
        "signal_form": "Digital ON/OFF (12/24 V DC)",
        "details": "2-wire (red + / black –)",
        "classification_notes": "Audible system warning activated by controller; IP67 rated",
        "connector_type": "—",
        "connector_part_number": "—",
        "cables": [
            {
                "cable_id": "W6",
                "cable_part_number": "Part of H6",
                "connection_details": "2 × 0.5 mm²",
                "junction_box_ref": "C71 Molex Grey",
                "notes": "Direct connection to PAL40 C71. General-purpose warning (RRC activation, zone entry).",
                "wires": [
                    (1, "RD", "Pin 18 (C71)", "H6 supply terminal", "Horn drive output from PAL40"),
                    (2, "BK", "Pin 4 (C71)",  "H6 ground terminal", "Ground return for H6 horn"),
                ],
            }
        ],
    },
    {
        "order": 17,
        "device_ref": "B310",
        "part_number": "—",
        "description": "Slewing Monitoring Switch",
        "classification": "Binary Sensor",
        "designation": "Slewing monitoring sensor",
        "type_function": "Detects slewing direction or end-position monitoring for crane rotation",
        "signal_form": "Digital ON/OFF",
        "details": "Integrated feedback signal from boom monitoring circuit",
        "classification_notes": "Provides operational feedback of slewing motion to controller",
        "connector_type": "M12",
        "connector_part_number": "EEA3900",
        "cables": [
            {
                "cable_id": "W10",
                "cable_part_number": "EEA4379",
                "connection_details": "4 × 0.75 mm² control cable",
                "junction_box_ref": "C70 Molex Blue",
                "notes": "4-wire sensor connection to PAL40 C70 (B310 slewing sensor pins).",
                "wires": [
                    (1, "BN", "Pin 48 (C70)", "Protected supply — B310",  "Sensor supply +V"),
                    (2, "WH", "Pin 20 (C70)", "Slewing left command",      "Slewing left / direction 1"),
                    (3, "YE", "Pin 6 (C70)",  "Slewing sensor ground",     "Sensor signal ground"),
                    (4, "GN", "Pin 34 (C70)", "Slewing right command",     "Slewing right / direction 2"),
                ],
            }
        ],
    },
    {
        "order": 18,
        "device_ref": "B312",
        "part_number": "—",
        "description": "Mainboom Monitoring Switch",
        "classification": "Binary Sensor",
        "designation": "Boom position / monitoring switch",
        "type_function": "Detects main boom operational state for PALTRONIC control",
        "signal_form": "Digital ON/OFF",
        "details": "Integrated feedback signal from boom monitoring circuit",
        "classification_notes": "Provides operational feedback of main boom motion to controller",
        "connector_type": "M12",
        "connector_part_number": "Not specified",
        "cables": [
            {
                "cable_id": "W312",
                "cable_part_number": "EEA4379",
                "connection_details": "4 × 0.75 mm² control cable",
                "junction_box_ref": "C70 Molex Blue",
                "notes": "4-wire connection to PAL40 C70 (B312 main boom sensor pins).",
                "wires": [
                    (1, "BN", "Pin 47 (C70)", "Protected supply — B312",  "Sensor supply +V"),
                    (2, "WH", "Pin 19 (C70)", "Main boom up command",      "Boom up / direction 1"),
                    (3, "YE", "Pin 5 (C70)",  "Main boom sensor ground",   "Sensor signal ground"),
                    (4, "GN", "Pin 33 (C70)", "Main boom down command",    "Boom down / direction 2"),
                ],
            }
        ],
    },
    {
        "order": 19,
        "device_ref": "B314",
        "part_number": "—",
        "description": "Knuckleboom Monitoring Switch",
        "classification": "Binary Sensor",
        "designation": "Boom position / monitoring switch",
        "type_function": "Detects knuckle boom position state",
        "signal_form": "Digital ON/OFF",
        "details": "Integrated feedback signal from boom monitoring circuit",
        "classification_notes": "Provides operational feedback of knuckle boom motion to controller",
        "connector_type": "M12",
        "connector_part_number": "Not specified",
        "cables": [
            {
                "cable_id": "W314",
                "cable_part_number": "EEA4379",
                "connection_details": "4 × 0.75 mm² control cable",
                "junction_box_ref": "C70 Molex Blue",
                "notes": "4-wire connection to PAL40 C70 (B314 knuckle boom sensor pins).",
                "wires": [
                    (1, "BN", "Pin 46 (C70)", "Protected supply — B314",   "Sensor supply +V"),
                    (2, "WH", "Pin 18 (C70)", "Knuckle boom up command",   "Boom up / direction 1"),
                    (3, "YE", "Pin 4 (C70)",  "Ground",                    "Sensor signal ground"),
                    (4, "GN", "Pin 32 (C70)", "Knuckle boom down command", "Boom down / direction 2"),
                ],
            }
        ],
    },
    {
        "order": 20,
        "device_ref": "B316",
        "part_number": "—",
        "description": "Extension Monitoring Switch",
        "classification": "Binary Sensor",
        "designation": "Extension position monitoring",
        "type_function": "Detects extension movement state",
        "signal_form": "Digital ON/OFF",
        "details": "Integrated feedback signal from extension monitoring",
        "classification_notes": "Provides extension position status for control logic",
        "connector_type": "M12",
        "connector_part_number": "Not specified",
        "cables": [
            {
                "cable_id": "W316",
                "cable_part_number": "EEA4379",
                "connection_details": "4 × 0.75 mm² control cable",
                "junction_box_ref": "C71 Molex Grey",
                "notes": "4-wire connection to PAL40 C71 (B316 extension sensor pins).",
                "wires": [
                    (1, "BN", "Pin 51 (C71)", "Protected supply — B316",   "Sensor supply +V"),
                    (2, "WH", "Pin 23 (C71)", "Extension retract command", "Retract / direction 1"),
                    (3, "YE", "Pin 9 (C71)",  "Extension sensor ground",   "Sensor signal ground"),
                    (4, "GN", "Pin 37 (C71)", "Extension out command",     "Extend / direction 2"),
                ],
            }
        ],
    },
    {
        "order": 21,
        "device_ref": "B318",
        "part_number": "—",
        "description": "Winch Monitoring Switch",
        "classification": "Binary Sensor",
        "designation": "Winch monitoring switch",
        "type_function": "Detects winch operational condition",
        "signal_form": "Digital ON/OFF",
        "details": "Integrated feedback signal from winch monitoring",
        "classification_notes": "Provides winch status monitoring signal",
        "connector_type": "M12",
        "connector_part_number": "Not specified",
        "cables": [
            {
                "cable_id": "W318",
                "cable_part_number": "EEA4379",
                "connection_details": "4 × 0.75 mm² control cable",
                "junction_box_ref": "C71 Molex Grey",
                "notes": "4-wire connection to PAL40 C71 (B318 winch control sensor pins).",
                "wires": [
                    (1, "BN", "Pin 52 (C71)", "Protected supply — B318",   "Sensor supply +V"),
                    (2, "WH", "Pin 38 (C71)", "Winch up command",          "Hoist / direction 1"),
                    (3, "YE", "Pin 10 (C71)", "Winch sensor ground",       "Sensor signal ground"),
                    (4, "GN", "Pin 24 (C71)", "Winch down command",        "Lower / direction 2"),
                ],
            }
        ],
    },
]


class Command(BaseCommand):
    help = "Load all PFM2100 device, cable, and wire data into the database"

    def add_arguments(self, parser):
        parser.add_argument("--flush", action="store_true", help="Delete existing data before loading")

    def handle(self, *args, **options):
        if options["flush"]:
            self.stdout.write("Flushing existing PFM2100 data...")
            PFM2100WireTerminal.objects.all().delete()
            PFM2100Cable.objects.all().delete()
            PFM2100Device.objects.all().delete()

        total_devices = 0
        total_cables = 0
        total_wires = 0

        for d in DEVICES:
            device, created = PFM2100Device.objects.update_or_create(
                order=d["order"],
                defaults={
                    "device_ref":            d.get("device_ref", ""),
                    "part_number":           d["part_number"] if d["part_number"] != "—" else "",
                    "description":           d["description"],
                    "classification":        d["classification"],
                    "designation":           d["designation"],
                    "type_function":         d["type_function"],
                    "signal_form":           d["signal_form"],
                    "details":               d["details"],
                    "classification_notes":  d["classification_notes"],
                    "connector_type":        d["connector_type"] if d["connector_type"] != "—" else "",
                    "connector_part_number": d["connector_part_number"] if d["connector_part_number"] != "—" else "",
                },
            )
            total_devices += 1

            for c in d["cables"]:
                cable, _ = PFM2100Cable.objects.update_or_create(
                    device=device,
                    cable_id=c["cable_id"],
                    defaults={
                        "cable_part_number": c["cable_part_number"],
                        "connection_details": c["connection_details"],
                        "junction_box_ref": c["junction_box_ref"],
                        "notes": c["notes"],
                    },
                )
                total_cables += 1

                PFM2100WireTerminal.objects.filter(cable=cable).delete()
                for wire in c["wires"]:
                    PFM2100WireTerminal.objects.create(
                        cable=cable,
                        order=wire[0],
                        wire_color=wire[1],
                        device_pin=wire[2],
                        terminal_ref=wire[3],
                        notes=wire[4],
                    )
                    total_wires += 1

            status = "Created" if created else "Updated"
            self.stdout.write(f"  {status:8s} [{d['order']:2d}] {d['description']}")

        self.stdout.write(self.style.SUCCESS(
            f"\nDone. {total_devices} devices, {total_cables} cables, {total_wires} wire terminals loaded."
        ))
