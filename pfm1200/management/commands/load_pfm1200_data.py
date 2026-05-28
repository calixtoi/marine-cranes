from django.core.management.base import BaseCommand
from pfm1200.models import PFM1200Device, PFM1200Cable, PFM1200WireTerminal

# ──────────────────────────────────────────────────────────────────────────────
# Source documents (cable lengths taken directly from drawing dimensions):
#   KEB01571B  — PFM1200 wiring, Junction Box XX3 (9 sheets, dated 21-Feb-2025)
#   KEB01572B XX4 — Junction Box XX4 crane arm (3 sheets, dated 31-Oct-2024)
#
# Cable lengths extracted per sheet:
#   Page 3 : W71=2400, W316=1400, W318=1450, W6=900
#   Page 4 : W70=2400, W310=1200, W312=1250, W314=1300, W0=1500
#   Page 5 : W25=850 (550+300), W172=2500
#   Page 6 : W409=2400, W411=2400
#   Page 7 : W24=1660, W50=2000, W52=2000, W54=2000
#   Page 8 : W56=2100, W58=2200, W60=1900, W62=1800
#   Page 9 : W17=tbd, W18=tbd
#   KEB01572B p3: W171=2300, W190=1240
#   W5 = 1000 mm (EEA6193 product spec: 1 m integral cable)
#   W205/W206/W113/W26/W170/W9/W900 = 0 (tbd in drawings)
# ──────────────────────────────────────────────────────────────────────────────

DEVICES = [
    # ── 1. Slewing Encoder — U205 ────────────────────────────────────────────
    {
        "order": 1,
        "device_ref": "U205",
        "part_number": "EEA18563",
        "description": "Slewing Encoder",
        "classification": "Analogue Sensor",
        "designation": "CAN encoder for slewing angle measurement (CANopen)",
        "type_function": "Absolute encoder providing crane slewing position via CAN Bus 0",
        "signal_form": "CANopen digital (2 × 2 × 0.34 mm² shielded pair)",
        "details": "CAN H → Terminal 628, CAN L → Terminal 629",
        "classification_notes": "Connected to XX3 Terminal 628/629 (CAN Bus 0). Cable EEA12216.",
        "connector_type": "M12",
        "connector_part_number": "EEA3900",
        "cables": [
            {
                "cable_id": "W205",
                "cable_part_number": "EEA12216",
                "connection_details": "2 × 2 × 0.34 mm²",
                "length_mm": 0,          # TBD — not dimensioned in KEB01571B
                "junction_box_ref": "Junction Box XX3",
                "notes": "Length TBD (not dimensioned in KEB01571B). CAN Bus 0: H → T.628, L → T.629.",
                "wires": [
                    (1, "RD", "Pin 1", "Terminal 160", "Supply +Vs"),
                    (2, "BU", "Pin 2", "Terminal 800", "Ground 0 V"),
                    (3, "YE", "Pin 3", "Terminal 629",  "CAN Low — Bus 0"),
                    (4, "GN", "Pin 4", "Terminal 628",  "CAN High — Bus 0"),
                ],
            }
        ],
    },
    # ── 2. Mainboom Angle Sensor — U206 ──────────────────────────────────────
    {
        "order": 2,
        "device_ref": "U206",
        "part_number": "EEA14709",
        "description": "Mainboom Angle Sensor",
        "classification": "Analogue Sensor",
        "designation": "CAN encoder for main boom angle measurement (CANopen)",
        "type_function": "Absolute encoder providing main boom position via CAN Bus 1",
        "signal_form": "CANopen digital (2 × 2 × 0.34 mm² shielded pair)",
        "details": "CAN H → Terminal 620, CAN L → Terminal 621",
        "classification_notes": "Connected to XX3 Terminal 620/621 (CAN Bus 1). Cable EEA13797.",
        "connector_type": "M16",
        "connector_part_number": "EEA3901",
        "cables": [
            {
                "cable_id": "W206",
                "cable_part_number": "EEA13797",
                "connection_details": "2 × 2 × 0.34 mm²",
                "length_mm": 0,          # TBD — not dimensioned in KEB01571B
                "junction_box_ref": "Junction Box XX3",
                "notes": "Length TBD (not dimensioned in KEB01571B). CAN Bus 1: H → T.620, L → T.621.",
                "wires": [
                    (1, "RD", "Pin 1", "Terminal 160", "Supply +Vs"),
                    (2, "BU", "Pin 2", "Terminal 800", "Ground 0 V"),
                    (3, "YE", "Pin 3", "Terminal 621",  "CAN Low — Bus 1"),
                    (4, "GN", "Pin 4", "Terminal 620",  "CAN High — Bus 1"),
                ],
            }
        ],
    },
    # ── 3. Pressure Sensor Piston Side — U409 ────────────────────────────────
    {
        "order": 3,
        "device_ref": "U409",
        "part_number": "EEA18779",
        "description": "Pressure Sensor — Piston Side",
        "classification": "Analogue Sensor",
        "designation": "Hydraulic pressure transducer — piston side cylinder",
        "type_function": "Measures hydraulic pressure in piston side of main cylinder",
        "signal_form": "Analogue 4–20 mA current loop",
        "details": "4 × 0.34 mm² screened. Screen on PE terminal.\n[BN supply, BU ground, WH → T.103, BK → T.104]",
        "classification_notes": "WH → Terminal 103 (C70 Pin 26), BK → Terminal 104 (C70 Pin 40).",
        "connector_type": "M12",
        "connector_part_number": "EEA3705",
        "cables": [
            {
                "cable_id": "W409",
                "cable_part_number": "EEA12759",
                "connection_details": "4 × 0.34 mm²",
                "length_mm": 2400,       # KEB01571B sheet 6: "2400 mm"
                "junction_box_ref": "Junction Box XX3",
                "notes": "Total length 2400 mm (KEB01571B sheet 6). Screen terminated on PE terminal.",
                "wires": [
                    (1, "BN",     "Pin 1", "Terminal 160", "Supply +Ub"),
                    (2, "WH",     "Pin 2", "Terminal 103", "Signal 1 — 4–20 mA (→ C70 Pin 26)"),
                    (3, "BU",     "Pin 3", "Terminal 800", "Ground 0 V"),
                    (4, "BK",     "Pin 4", "Terminal 104", "Signal 2 — 4–20 mA (→ C70 Pin 40)"),
                    (5, "Screen", "—",     "PE Terminal",  "Terminate screen on PE-Terminal"),
                ],
            }
        ],
    },
    # ── 4. Pressure Sensor Rod Side — U211 ───────────────────────────────────
    {
        "order": 4,
        "device_ref": "U211",
        "part_number": "EEA18779",
        "description": "Pressure Sensor — Rod Side",
        "classification": "Analogue Sensor",
        "designation": "Hydraulic pressure transducer — rod side cylinder",
        "type_function": "Measures hydraulic pressure in rod side of main cylinder",
        "signal_form": "Analogue 4–20 mA current loop",
        "details": "4 × 0.34 mm² screened. Screen on PE terminal.\n[BN supply, BU ground, WH → T.105, BK → T.106]",
        "classification_notes": "WH → Terminal 105 (C70 Pin 25), BK → Terminal 106 (C70 Pin 39).",
        "connector_type": "M12",
        "connector_part_number": "EEA3705",
        "cables": [
            {
                "cable_id": "W411",
                "cable_part_number": "EEA12759",
                "connection_details": "4 × 0.34 mm²",
                "length_mm": 2400,       # KEB01571B sheet 6: "2400 mm"
                "junction_box_ref": "Junction Box XX3",
                "notes": "Total length 2400 mm (KEB01571B sheet 6). Screen terminated on PE terminal.",
                "wires": [
                    (1, "BN",     "Pin 1", "Terminal 160", "Supply +Ub"),
                    (2, "WH",     "Pin 2", "Terminal 105", "Signal 1 — 4–20 mA (→ C70 Pin 25)"),
                    (3, "BU",     "Pin 3", "Terminal 800", "Ground 0 V"),
                    (4, "BK",     "Pin 4", "Terminal 106", "Signal 2 — 4–20 mA (→ C70 Pin 39)"),
                    (5, "Screen", "—",     "PE Terminal",  "Terminate screen on PE-Terminal"),
                ],
            }
        ],
    },
    # ── 5. Telematic Unit — U900 ──────────────────────────────────────────────
    {
        "order": 5,
        "device_ref": "U900",
        "part_number": "EEA15360",
        "description": "Telematic Unit CS100 IoT Gateway",
        "classification": "Communication Device / Analogue Processor",
        "designation": "Danfoss CS100 IoT Gateway — crane telemetry via CAN + cellular",
        "type_function": "CAN data, GNSS telemetry connection for remote monitoring",
        "signal_form": "CAN bus / LTE / 2G data transfer digital",
        "details": "Installed only if PCH = MOD1. Fuse F900 (1 A, EEA6090) in XX3. Part of assembly U900.",
        "classification_notes": "Cable part of U900 assembly. CAN1 H → T.621, CAN1 L → T.620.",
        "connector_type": "M16",
        "connector_part_number": "EEA3901",
        "cables": [
            {
                "cable_id": "W900",
                "cable_part_number": "Part of U900",
                "connection_details": "4 × 0.34 mm²",
                "length_mm": 0,          # TBD — not dimensioned in KEB01571B
                "junction_box_ref": "Junction Box XX3",
                "notes": (
                    "Length TBD. Only installed if PCH = MOD1 (Telematic Unit).\n"
                    "Supply via Fuse F900 (1 A) → Terminal 801."
                ),
                "wires": [
                    (1, "BU", "Pin 1", "Terminal 800",   "Ground 0 V"),
                    (2, "RD", "Pin 2", "Fuse F900",      "Supply +V (fused 1 A)"),
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
    # ── 6. Emergency Stop Valve Y0 ────────────────────────────────────────────
    {
        "order": 6,
        "device_ref": "Y0",
        "part_number": "—",
        "description": "Emergency Stop Valve Y0",
        "classification": "Safety Control Device",
        "designation": "Emergency stop hydraulic valve Y0 (normally closed)",
        "type_function": "Main crane enable valve — must be energized for crane operation",
        "signal_form": "Digital ON/OFF 24 V DC",
        "details": "Connector C0: AMP JPT grey plug (EEA5428, pins EEA5424, seal EEA5425, cap EEZ1731)",
        "classification_notes": "C0 → PAL40 C70 Molex Blue. De-energizes on E-stop, overload or CAN fault.",
        "connector_type": "AMP JPT",
        "connector_part_number": "EEA5428",
        "cables": [
            {
                "cable_id": "W0",
                "cable_part_number": "EEA4379",
                "connection_details": "4 × 0.75 mm²",
                "length_mm": 1500,       # KEB01571B sheet 4: "1500" (C0 to C70)
                "junction_box_ref": "C70 Molex Blue",
                "notes": "Length 1500 mm (KEB01571B sheet 4). C0 → C70. GN and BN blind at C70.",
                "wires": [
                    (1, "YE", "PIN 1 (C0)", "PIN 28 (C70)", "Crane enable output"),
                    (2, "WH", "PIN 3 (C0)", "PIN 27 (C70)", "Coil ground return"),
                    (3, "GN", "PIN 2 (C0)", "Blind",         "Unused — blind heat shrink"),
                    (4, "BN", "PIN 4 (C0)", "Blind",         "Unused — blind heat shrink"),
                ],
            }
        ],
    },
    # ── 7. Overload Horn H5 ───────────────────────────────────────────────────
    {
        "order": 7,
        "device_ref": "H5",
        "part_number": "EEA6193",
        "description": "Overload Horn H5",
        "classification": "Binary Device (Acoustic)",
        "designation": "Piezo overload horn H5 (EEA6193) — 90 dB IP67",
        "type_function": "Audible alarm for load overload condition",
        "signal_form": "Digital ON/OFF 24 V DC",
        "details": "2-wire cable (RD +, BK −). Part of EEA6193 assembly — 1 m integral cable.",
        "classification_notes": "Direct connection to PAL40 C70. RD → PIN 42, BK → PIN 41.",
        "connector_type": "—",
        "connector_part_number": "—",
        "cables": [
            {
                "cable_id": "W5",
                "cable_part_number": "Part of EEA6193",
                "connection_details": "2 × 0.5 mm²",
                "length_mm": 1000,       # EEA6193 product spec: 1 m integral cable
                "junction_box_ref": "C70 Molex Blue",
                "notes": "Length 1000 mm (EEA6193 product: 1 m integral cable). Direct connection to PAL40 C70.",
                "wires": [
                    (1, "RD", "H5 supply", "PIN 42 (C70)", "Horn drive output from PAL40"),
                    (2, "BK", "H5 ground", "PIN 41 (C70)", "Ground return for H5 horn"),
                ],
            }
        ],
    },
    # ── 8. Warning Horn H6 ────────────────────────────────────────────────────
    {
        "order": 8,
        "device_ref": "H6",
        "part_number": "EEA6194",
        "description": "Warning Horn H6",
        "classification": "Binary Device (Acoustic)",
        "designation": "Speaker alarm H6 (EEA6194) — IP67",
        "type_function": "General-purpose warning horn",
        "signal_form": "Digital ON/OFF 24 V DC",
        "details": "2-wire cable (RD +, BK −). Part of EEA6194 assembly.",
        "classification_notes": "Direct connection to PAL40 C71. RD → PIN 18, BK → PIN 4.",
        "connector_type": "—",
        "connector_part_number": "—",
        "cables": [
            {
                "cable_id": "W6",
                "cable_part_number": "Part of EEA6194",
                "connection_details": "2 × 0.5 mm²",
                "length_mm": 900,        # KEB01571B sheet 3: "900"
                "junction_box_ref": "C71 Molex Grey",
                "notes": "Length 900 mm (KEB01571B sheet 3). Direct connection to PAL40 C71.",
                "wires": [
                    (1, "RD", "H6 supply", "PIN 18 (C71)", "Horn drive output from PAL40"),
                    (2, "BK", "H6 ground", "PIN 4 (C71)",  "Ground return for H6 horn"),
                ],
            }
        ],
    },
    # ── 9. Orange Flashlight Beacon — H113 ────────────────────────────────────
    {
        "order": 9,
        "device_ref": "H113",
        "part_number": "EEA17497",
        "description": "Flashlight Beacon (Orange)",
        "classification": "Electrically Powered Equipment (Lighting)",
        "designation": "LED strobe / orange flashlight beacon H113 (EEA17497)",
        "type_function": "Visual warning beacon, flashing output, orange LED strobe",
        "signal_form": "Digital ON/OFF 24 V DC",
        "details": (
            "4 × 0.34 mm² cable CPEE0400. Connector M12 (EEA3900).\n"
            "Cable protection: Split Conduit D5.7-11.5 Polyamide (EZ7063).\n"
            "BN and WH terminated with shrink sleeves (unused)."
        ),
        "classification_notes": "BK → Terminal 111 (control). BU → Terminal 800 (ground). Cable gland M12.",
        "connector_type": "M12",
        "connector_part_number": "EEA3900",
        "cables": [
            {
                "cable_id": "W113",
                "cable_part_number": "CPEE0400",
                "connection_details": "4 × 0.34 mm²",
                "length_mm": 0,          # TBD — not dimensioned in KEB01571B
                "junction_box_ref": "Junction Box XX3",
                "notes": (
                    "Length TBD (not dimensioned in KEB01571B). Cable gland M12.\n"
                    "Split Conduit D5.7-11.5 Polyamide (EZ7063). BN and WH with shrink sleeves."
                ),
                "wires": [
                    (1, "BN",  "Pin 3 (common)", "Shrink sleeve", "Common/neutral — terminated blind"),
                    (2, "BU",  "Pin 2",           "Terminal 800",  "Ground 0 V"),
                    (3, "WH",  "—",               "Shrink sleeve", "Unused — terminated blind"),
                    (4, "BK",  "Pin 1",           "Terminal 111",  "Control signal from PAL40 C71"),
                ],
            }
        ],
    },
    # ── 10. Working Light — H172 ──────────────────────────────────────────────
    {
        "order": 10,
        "device_ref": "H172",
        "part_number": "EEA11854",
        "description": "Working Light",
        "classification": "Electrically Powered Equipment (Lighting)",
        "designation": (
            "Working light H172 (EEA11854) — relay-switched via K56.\n"
            "Deutsch DT 2-pin connector (EEA5044). Rubber cap EEA5696.\n"
            "Xenon lamp + socket. Cable protection EZ7063."
        ),
        "type_function": "Close-range illumination, switched via relay K56 (C71 Pin 21 → K56 coil)",
        "signal_form": "Constant 24 V DC supply (relay-switched)",
        "details": (
            "2 × 1.5 mm² cable EEA 170. Connector: Deutsch DT 2-pin (EEA5044), rubber cap EEA5696.\n"
            "Split Conduit D5.7-11.5 Polyamide (EZ7063). Xenon lamp + socket.\n"
            "Only installed if SCHEI = SCHEI03L."
        ),
        "classification_notes": "Optional (SCHEI03L only). Switched via K56. BN K56/A1 in W71.",
        "connector_type": "Deutsch DT 2P",
        "connector_part_number": "EEA5044",
        "cables": [
            {
                "cable_id": "W172",
                "cable_part_number": "EEA 170",
                "connection_details": "2 × 1.5 mm²",
                "length_mm": 2500,       # KEB01571B sheet 5: "2500 mm"
                "junction_box_ref": "Junction Box XX3",
                "notes": (
                    "Length 2500 mm (KEB01571B sheet 5). Only if SCHEI = SCHEI03L.\n"
                    "Split Conduit EZ7063. Deutsch DT 2P (EEA5044), rubber cap EEA5696.\n"
                    "Switched via K56: C71 Pin 21 → K56 A1/A2 → contacts → Terminal 56."
                ),
                "wires": [
                    (1, "RD", "PIN 1 (C172)", "Terminal 56",  "Supply +24 V (via K56 relay)"),
                    (2, "BU", "PIN 2 (C172)", "Terminal 806", "Ground 0 V"),
                ],
            },
            {
                "cable_id": "W172.2",
                "cable_part_number": "EEA 170",
                "connection_details": "2 × 1.5 mm²",
                "length_mm": 0,          # TBD — not dimensioned in KEB01571B
                "junction_box_ref": "Junction Box XX3",
                "notes": "Secondary cable — same type as W172 (EEA 170, 2 × 1.5 mm²). Split Conduit EZ7063. Length TBD.",
                "wires": [
                    (1, "RD", "PIN 1", "Terminal 56",  "Supply +24 V"),
                    (2, "BU", "PIN 2", "Terminal 806", "Ground 0 V"),
                ],
            },
        ],
    },
    # ── 11. PAL40 ECU C70 ─────────────────────────────────────────────────────
    {
        "order": 11,
        "device_ref": "C70",
        "part_number": "EEA12509",
        "description": "PAL40 ECU — Connector C70",
        "classification": "Communication Device / ECU Connector",
        "designation": "PAL40 ECU C70 — Molex Blue 56-pin connector",
        "type_function": "Main crane control ECU: CAN Bus 0, levers, pressure sensors, E-stop chain",
        "signal_form": "Mixed: CAN, analogue 4–20 mA, digital I/O",
        "details": "EEA12509 plug, EEA12512 pins, EEA12515 grommet seal, EEA12514 cap. 56-pin Molex Blue.",
        "classification_notes": "W70: XX3 → C70. 12 × 0.75 mm², 2400 mm. 550 mm to XX3, 70 mm pigtail at C70.",
        "connector_type": "Molex 56-pin",
        "connector_part_number": "EEA12509",
        "cables": [
            {
                "cable_id": "W70",
                "cable_part_number": "EEA4378",
                "connection_details": "12 × 0.75 mm²",
                "length_mm": 2400,       # KEB01571B sheet 4: "2400" (550 to XX3 + 70 pigtail)
                "junction_box_ref": "Junction Box XX3",
                "notes": "Length 2400 mm (KEB01571B sheet 4): 550 mm to XX3 + 70 mm pigtail at C70.",
                "wires": [
                    (1,  "RD",   "PIN 56 (C70)", "Terminal 160", "Supply +24 V"),
                    (2,  "BU",   "PIN 55 (C70)", "Terminal 800", "Ground 0 V"),
                    (3,  "BK",   "PIN 16 (C70)", "Terminal 101", "E-stop chain 1"),
                    (4,  "GY",   "PIN 17 (C70)", "Terminal 102", "E-stop chain 2"),
                    (5,  "GN",   "PIN 15 (C70)", "Terminal 628", "CAN Bus 0 High"),
                    (6,  "YE",   "PIN 29 (C70)", "Terminal 629", "CAN Bus 0 Low"),
                    (7,  "VT",   "PIN 26 (C70)", "Terminal 103", "Pressure sensor signal 1"),
                    (8,  "BN",   "PIN 40 (C70)", "Terminal 104", "Pressure sensor signal 2"),
                    (9,  "WH",   "PIN 25 (C70)", "Terminal 105", "Pressure sensor signal 3"),
                    (10, "GY/PK","PIN 39 (C70)", "Terminal 106", "Pressure sensor signal 4"),
                    (11, "PK",   "—",            "Blind",         "Unused — blind heat shrink"),
                    (12, "RD/BU","PIN 14 (C70)", "Terminal 121", "Y0 E-stop support enable"),
                ],
            }
        ],
    },
    # ── 12. PAL40 ECU C71 ─────────────────────────────────────────────────────
    {
        "order": 12,
        "device_ref": "C71",
        "part_number": "EEA12510",
        "description": "PAL40 ECU — Connector C71",
        "classification": "Communication Device / ECU Connector",
        "designation": "PAL40 ECU C71 — Molex Grey 56-pin connector",
        "type_function": "Main crane control ECU: CAN Bus 1, monitoring switches, warning outputs",
        "signal_form": "Mixed: CAN, digital I/O",
        "details": "EEA12510 plug, EEA12512 pins, EEA12515 grommet seal, EEA12514 cap. 56-pin Molex Grey.",
        "classification_notes": "W71: XX3 → C71. 12 × 0.75 mm², 2400 mm. 550 mm to XX3, 70 mm pigtail at C71.",
        "connector_type": "Molex 56-pin",
        "connector_part_number": "EEA12510",
        "cables": [
            {
                "cable_id": "W71",
                "cable_part_number": "EEA4378",
                "connection_details": "12 × 0.75 mm²",
                "length_mm": 2400,       # KEB01571B sheet 3: "2400" (550 to XX3 + 70 pigtail)
                "junction_box_ref": "Junction Box XX3",
                "notes": "Length 2400 mm (KEB01571B sheet 3): 550 mm to XX3 + 70 mm pigtail at C71.",
                "wires": [
                    (1,  "RD",   "PIN 16 (C71)", "Terminal 161", "Warning output supply"),
                    (2,  "GY/PK","—",            "Blind",         "Unused — blind heat shrink"),
                    (3,  "BU",   "PIN 2 (C71)",  "Terminal 800", "Ground 0 V"),
                    (4,  "GY",   "PIN 31 (C71)", "Terminal 15",  "CAN Bus signal"),
                    (5,  "GN",   "PIN 15 (C71)", "Terminal 620", "CAN Bus 1 High"),
                    (6,  "YE",   "PIN 29 (C71)", "Terminal 621", "CAN Bus 1 Low"),
                    (7,  "BU/RD","PIN 40 (C71)", "Terminal 140", "Winch overload NC signal"),
                    (8,  "WH",   "PIN 26 (C71)", "Terminal 109", "Winch overload NO signal"),
                    (9,  "VT",   "—",            "Blind",         "Unused — blind heat shrink"),
                    (10, "BK",   "PIN 17 (C71)", "Terminal 111", "Beacon control (if SCHEI=SCH03L)"),
                    (11, "BN",   "K56/A1",       "K56 Relay coil","Working light relay coil (if SCHEI=SCH03L)"),
                ],
            }
        ],
    },
    # ── 13. Main Controller C1 ────────────────────────────────────────────────
    {
        "order": 13,
        "device_ref": "C1",
        "part_number": "EEA4090",
        "description": "Remote Control — Connector C1",
        "classification": "Communication Device / ECU Connector",
        "designation": "C1 — DT 70-pin connector on Remote Control unit",
        "type_function": "Remote control interface: lever valve outputs, relay control, supply",
        "signal_form": "Mixed: digital valve signals, relay control",
        "details": (
            "EEA4090 plug, EEA4093 pins, EEA4092 pins, EEA4423 blind grommet, EEA4169 cap.\n"
            "DT 70-pin. Cable W24: EEA1268 12 × 1.5 mm², 1660 mm between XX3 and Remote Control."
        ),
        "classification_notes": "W24 links XX3 terminal strip to Remote Control C1. Levers Y310–Y322 connect directly to C1.",
        "connector_type": "DT 70-pin",
        "connector_part_number": "EEA4090",
        "cables": [
            {
                "cable_id": "W24",
                "cable_part_number": "EEA1268",
                "connection_details": "12 × 1.5 mm²",
                "length_mm": 1660,       # KEB01571B sheet 7: "1660" (550 mm to XX3 + 110 mm at C1)
                "junction_box_ref": "Junction Box XX3 → Remote Control",
                "notes": "Length 1660 mm (KEB01571B sheet 7): 550 mm to XX3, 110 mm pigtail at C1.",
                "wires": [
                    (1, "1",  "PIN 59 (C1)", "Terminal 801", "Supply +24 V (fused)"),
                    (2, "2",  "PIN 13 (C1)", "Terminal 800", "Ground 0 V"),
                    (3, "3",  "PIN 20 (C1)", "Terminal 15",  "Control supply rail"),
                    (4, "4",  "PIN 14 (C1)", "Terminal 620", "CAN Bus 1 High"),
                    (5, "5",  "PIN 12 (C1)", "Terminal 621", "CAN Bus 1 Low"),
                    (6, "BU", "PIN 57 (C1)", "Terminal 800", "Ground 0 V (additional)"),
                    (7, "6",  "PIN 19 (C1)", "K50/A1",       "Relay K50 coil positive"),
                    (8, "—",  "Blind",        "Blind",         "Unused — blind shrinking tube"),
                    (9, "—",  "Blind",        "Blind",         "Unused — blind shrinking tube"),
                    (10,"—",  "Blind",        "Blind",         "Unused — blind shrinking tube"),
                    (11,"—",  "Blind",        "Blind",         "Unused — blind shrinking tube"),
                    (12,"—",  "Blind",        "Blind",         "Unused — blind shrinking tube"),
                ],
            }
        ],
    },
    # ── 14–20. Hydraulic Valves Y310–Y322 ────────────────────────────────────
    {
        "order": 14, "device_ref": "Y310", "part_number": "EEA4379",
        "description": "Hydraulic Valve Y310",
        "classification": "Binary Sensor",
        "designation": "Hydraulic control valve Y310 — AMP JPT grey 4-pin (C50 connector)",
        "type_function": "Proportional lever / valve input — crane motion control",
        "signal_form": "Digital ON/OFF lever switch (4-wire)",
        "details": "4 × 0.75 mm². EEA5428 plug, EEA5424 pins, EEA5425 seal, EZ1731 cap.",
        "classification_notes": "EPLAN: Y310. Connector C50. YE/GN/WH/BN → C1 Pins 70/42/28/56.",
        "connector_type": "AMP JPT", "connector_part_number": "EEA5428",
        "cables": [{"cable_id": "W50","cable_part_number": "EEA4379","connection_details": "4 × 0.75 mm²","length_mm": 2000,"junction_box_ref": "C1 Controller","notes": "Length 2000 mm (KEB01571B sheet 7): 40 mm pigtail at C50 + 110 mm at C1.","wires": [(1,"YE","PIN 1 (C50)","PIN 70 (C1)","Dir 1"),(2,"GN","PIN 2 (C50)","PIN 42 (C1)","Dir 2"),(3,"WH","PIN 3 (C50)","PIN 28 (C1)","Ground"),(4,"BN","PIN 4 (C50)","PIN 56 (C1)","Supply")]}],
    },
    {
        "order": 15, "device_ref": "Y312", "part_number": "EEA4379",
        "description": "Hydraulic Valve Y312",
        "classification": "Binary Sensor",
        "designation": "Hydraulic control valve Y312 — AMP JPT grey 4-pin (C52 connector)",
        "type_function": "Proportional lever / valve input — crane motion control",
        "signal_form": "Digital ON/OFF lever switch (4-wire)",
        "details": "4 × 0.75 mm².",
        "classification_notes": "EPLAN: Y312. Connector C52. YE/GN/WH/BN → C1 Pins 69/41/27/55.",
        "connector_type": "AMP JPT", "connector_part_number": "EEA5428",
        "cables": [{"cable_id": "W52","cable_part_number": "EEA4379","connection_details": "4 × 0.75 mm²","length_mm": 2000,"junction_box_ref": "C1 Controller","notes": "Length 2000 mm (KEB01571B sheet 7).","wires": [(1,"YE","PIN 1 (C52)","PIN 69 (C1)","Dir 1"),(2,"GN","PIN 2 (C52)","PIN 41 (C1)","Dir 2"),(3,"WH","PIN 3 (C52)","PIN 27 (C1)","Ground"),(4,"BN","PIN 4 (C52)","PIN 55 (C1)","Supply")]}],
    },
    {
        "order": 16, "device_ref": "Y314", "part_number": "EEA4379",
        "description": "Hydraulic Valve Y314",
        "classification": "Binary Sensor",
        "designation": "Hydraulic control valve Y314 — AMP JPT grey 4-pin (C54 connector)",
        "type_function": "Proportional lever / valve input — crane motion control",
        "signal_form": "Digital ON/OFF lever switch (4-wire)",
        "details": "4 × 0.75 mm².",
        "classification_notes": "EPLAN: Y314. Connector C54. YE/GN/WH/BN → C1 Pins 68/40/26/54.",
        "connector_type": "AMP JPT", "connector_part_number": "EEA5428",
        "cables": [{"cable_id": "W54","cable_part_number": "EEA4379","connection_details": "4 × 0.75 mm²","length_mm": 2000,"junction_box_ref": "C1 Controller","notes": "Length 2000 mm (KEB01571B sheet 7).","wires": [(1,"YE","PIN 1 (C54)","PIN 68 (C1)","Dir 1"),(2,"GN","PIN 2 (C54)","PIN 40 (C1)","Dir 2"),(3,"WH","PIN 3 (C54)","PIN 26 (C1)","Ground"),(4,"BN","PIN 4 (C54)","PIN 54 (C1)","Supply")]}],
    },
    {
        "order": 17, "device_ref": "Y316", "part_number": "EEA4379",
        "description": "Hydraulic Valve Y316",
        "classification": "Binary Sensor",
        "designation": "Hydraulic control valve Y316 — AMP JPT grey 4-pin (C56 connector)",
        "type_function": "Proportional lever / valve input — crane motion control",
        "signal_form": "Digital ON/OFF lever switch (4-wire)",
        "details": "4 × 0.75 mm².",
        "classification_notes": "EPLAN: Y316. Connector C56. YE/GN/WH/BN → C1 Pins 67/39/25/53.",
        "connector_type": "AMP JPT", "connector_part_number": "EEA5428",
        "cables": [{"cable_id": "W56","cable_part_number": "EEA4379","connection_details": "4 × 0.75 mm²","length_mm": 2100,"junction_box_ref": "C1 Controller","notes": "Length 2100 mm (KEB01571B sheet 8).","wires": [(1,"YE","PIN 1 (C56)","PIN 67 (C1)","Dir 1"),(2,"GN","PIN 2 (C56)","PIN 39 (C1)","Dir 2"),(3,"WH","PIN 3 (C56)","PIN 25 (C1)","Ground"),(4,"BN","PIN 4 (C56)","PIN 53 (C1)","Supply")]}],
    },
    {
        "order": 18, "device_ref": "Y318", "part_number": "EEA4379",
        "description": "Hydraulic Valve Y318",
        "classification": "Binary Sensor",
        "designation": "Hydraulic control valve Y318 — AMP JPT grey 4-pin (C58 connector)",
        "type_function": "Proportional lever / valve input — crane motion control",
        "signal_form": "Digital ON/OFF lever switch (4-wire)",
        "details": "4 × 0.75 mm².",
        "classification_notes": "EPLAN: Y318. Connector C58. YE/GN/WH/BN → C1 Pins 66/38/24/52.",
        "connector_type": "AMP JPT", "connector_part_number": "EEA5428",
        "cables": [{"cable_id": "W58","cable_part_number": "EEA4379","connection_details": "4 × 0.75 mm²","length_mm": 2200,"junction_box_ref": "C1 Controller","notes": "Length 2200 mm (KEB01571B sheet 8).","wires": [(1,"YE","PIN 1 (C58)","PIN 66 (C1)","Dir 1"),(2,"GN","PIN 2 (C58)","PIN 38 (C1)","Dir 2"),(3,"WH","PIN 3 (C58)","PIN 24 (C1)","Ground"),(4,"BN","PIN 4 (C58)","PIN 52 (C1)","Supply")]}],
    },
    {
        "order": 19, "device_ref": "Y320", "part_number": "EEA4379",
        "description": "Hydraulic Valve Y320",
        "classification": "Binary Sensor",
        "designation": "Hydraulic control valve Y320 — AMP JPT grey 4-pin (C60 connector)",
        "type_function": "Proportional lever / valve input — crane motion control",
        "signal_form": "Digital ON/OFF lever switch (4-wire)",
        "details": "4 × 0.75 mm².",
        "classification_notes": "EPLAN: Y320. Connector C60. YE/GN/WH/BN → C1 Pins 65/37/23/51.",
        "connector_type": "AMP JPT", "connector_part_number": "EEA5428",
        "cables": [{"cable_id": "W60","cable_part_number": "EEA4379","connection_details": "4 × 0.75 mm²","length_mm": 1900,"junction_box_ref": "C1 Controller","notes": "Length 1900 mm (KEB01571B sheet 8).","wires": [(1,"YE","PIN 1 (C60)","PIN 65 (C1)","Dir 1"),(2,"GN","PIN 2 (C60)","PIN 37 (C1)","Dir 2"),(3,"WH","PIN 3 (C60)","PIN 23 (C1)","Ground"),(4,"BN","PIN 4 (C60)","PIN 51 (C1)","Supply")]}],
    },
    {
        "order": 20, "device_ref": "Y322", "part_number": "EEA4379",
        "description": "Hydraulic Valve Y322",
        "classification": "Binary Sensor",
        "designation": "Hydraulic control valve Y322 — AMP JPT grey 4-pin (C62 connector)",
        "type_function": "Proportional lever / valve input — crane motion control",
        "signal_form": "Digital ON/OFF lever switch (4-wire)",
        "details": "4 × 0.75 mm².",
        "classification_notes": "EPLAN: Y322. Connector C62. YE/GN/WH/BN → C1 Pins 64/36/22/50.",
        "connector_type": "AMP JPT", "connector_part_number": "EEA5428",
        "cables": [{"cable_id": "W62","cable_part_number": "EEA4379","connection_details": "4 × 0.75 mm²","length_mm": 1800,"junction_box_ref": "C1 Controller","notes": "Length 1800 mm (KEB01571B sheet 8).","wires": [(1,"YE","PIN 1 (C62)","PIN 64 (C1)","Dir 1"),(2,"GN","PIN 2 (C62)","PIN 36 (C1)","Dir 2"),(3,"WH","PIN 3 (C62)","PIN 22 (C1)","Ground"),(4,"BN","PIN 4 (C62)","PIN 50 (C1)","Supply")]}],
    },
    # ── 21–25. Monitoring Switches C310–C318 ─────────────────────────────────
    {
        "order": 21, "device_ref": "C310", "part_number": "—",
        "description": "Mainboom Monitoring Switch C310",
        "classification": "Binary Sensor",
        "designation": "Mainboom position / monitoring switch C310",
        "type_function": "Detects main boom operational state for PALTRONIC control",
        "signal_form": "Digital ON/OFF (4-wire sensor)",
        "details": "AMP JPT black plug (EEA5423). 4 × 0.75 mm².",
        "classification_notes": "C310 → C70 Pins 34/20/6/48. KEB01571B sheet 4.",
        "connector_type": "AMP JPT", "connector_part_number": "EEA5423",
        "cables": [{"cable_id": "W310","cable_part_number": "EEA4379","connection_details": "4 × 0.75 mm²","length_mm": 1200,"junction_box_ref": "C70 Molex Blue","notes": "Length 1200 mm (KEB01571B sheet 4): 40 mm pigtail at C310 + 70 mm at C70.","wires": [(1,"YE","PIN 1 (C310)","PIN 34 (C70)","Dir 1"),(2,"GN","PIN 2 (C310)","PIN 20 (C70)","Dir 2"),(3,"WH","PIN 3 (C310)","PIN 6 (C70)","Ground"),(4,"BN","PIN 4 (C310)","PIN 48 (C70)","Supply")]}],
    },
    {
        "order": 22, "device_ref": "C312", "part_number": "—",
        "description": "Knuckleboom Monitoring Switch C312",
        "classification": "Binary Sensor",
        "designation": "Knuckle boom position / monitoring switch C312",
        "type_function": "Detects knuckle boom operational state for PALTRONIC control",
        "signal_form": "Digital ON/OFF (4-wire sensor)",
        "details": "AMP JPT black plug (EEA5423). 4 × 0.75 mm².",
        "classification_notes": "C312 → C70 Pins 33/19/5/47. KEB01571B sheet 4.",
        "connector_type": "AMP JPT", "connector_part_number": "EEA5423",
        "cables": [{"cable_id": "W312","cable_part_number": "EEA4379","connection_details": "4 × 0.75 mm²","length_mm": 1250,"junction_box_ref": "C70 Molex Blue","notes": "Length 1250 mm (KEB01571B sheet 4).","wires": [(1,"YE","PIN 1 (C312)","PIN 33 (C70)","Dir 1"),(2,"GN","PIN 2 (C312)","PIN 19 (C70)","Dir 2"),(3,"WH","PIN 3 (C312)","PIN 5 (C70)","Ground"),(4,"BN","PIN 4 (C312)","PIN 47 (C70)","Supply")]}],
    },
    {
        "order": 23, "device_ref": "C314", "part_number": "—",
        "description": "Slewing Monitoring Switch C314",
        "classification": "Binary Sensor",
        "designation": "Slewing position / monitoring switch C314",
        "type_function": "Detects slewing operational state for PALTRONIC control",
        "signal_form": "Digital ON/OFF (4-wire sensor)",
        "details": "AMP JPT black plug (EEA5423). 4 × 0.75 mm².",
        "classification_notes": "C314 → C70 Pins 32/18/4/46. KEB01571B sheet 4.",
        "connector_type": "AMP JPT", "connector_part_number": "EEA5423",
        "cables": [{"cable_id": "W314","cable_part_number": "EEA4379","connection_details": "4 × 0.75 mm²","length_mm": 1300,"junction_box_ref": "C70 Molex Blue","notes": "Length 1300 mm (KEB01571B sheet 4).","wires": [(1,"YE","PIN 1 (C314)","PIN 32 (C70)","Dir 1"),(2,"GN","PIN 2 (C314)","PIN 18 (C70)","Dir 2"),(3,"WH","PIN 3 (C314)","PIN 4 (C70)","Ground"),(4,"BN","PIN 4 (C314)","PIN 46 (C70)","Supply")]}],
    },
    {
        "order": 24, "device_ref": "C316", "part_number": "—",
        "description": "Extension Monitoring Switch C316",
        "classification": "Binary Sensor",
        "designation": "Extension position / monitoring switch C316",
        "type_function": "Detects extension operational state for PALTRONIC control",
        "signal_form": "Digital ON/OFF (4-wire sensor)",
        "details": "AMP JPT black plug (EEA5423). 4 × 0.75 mm².",
        "classification_notes": "C316 → C71 Pins 37/23/9/51. KEB01571B sheet 3.",
        "connector_type": "AMP JPT", "connector_part_number": "EEA5423",
        "cables": [{"cable_id": "W316","cable_part_number": "EEA4379","connection_details": "4 × 0.75 mm²","length_mm": 1400,"junction_box_ref": "C71 Molex Grey","notes": "Length 1400 mm (KEB01571B sheet 3).","wires": [(1,"YE","PIN 1 (C316)","PIN 37 (C71)","Dir 1"),(2,"GN","PIN 2 (C316)","PIN 23 (C71)","Dir 2"),(3,"WH","PIN 3 (C316)","PIN 9 (C71)","Ground"),(4,"BN","PIN 4 (C316)","PIN 51 (C71)","Supply")]}],
    },
    {
        "order": 25, "device_ref": "C318", "part_number": "—",
        "description": "Winch Monitoring Switch C318",
        "classification": "Binary Sensor",
        "designation": "Winch position / monitoring switch C318",
        "type_function": "Detects winch operational state for PALTRONIC control",
        "signal_form": "Digital ON/OFF (4-wire sensor)",
        "details": "AMP JPT black plug (EEA5423). 4 × 0.75 mm².",
        "classification_notes": "C318 → C71 Pins 38/24/10/52. KEB01571B sheet 3.",
        "connector_type": "AMP JPT", "connector_part_number": "EEA5423",
        "cables": [{"cable_id": "W318","cable_part_number": "EEA4379","connection_details": "4 × 0.75 mm²","length_mm": 1450,"junction_box_ref": "C71 Molex Grey","notes": "Length 1450 mm (KEB01571B sheet 3).","wires": [(1,"YE","PIN 1 (C318)","PIN 38 (C71)","Dir 1"),(2,"GN","PIN 2 (C318)","PIN 24 (C71)","Dir 2"),(3,"WH","PIN 3 (C318)","PIN 10 (C71)","Ground"),(4,"BN","PIN 4 (C318)","PIN 52 (C71)","Supply")]}],
    },
    # ── 26. XX3-to-XX4 Link Cable — W25 ──────────────────────────────────────
    {
        "order": 26,
        "device_ref": "W25",
        "part_number": "EEA5503",
        "description": "XX3–XX4 Link Cable",
        "classification": "Auxiliary Device",
        "designation": "Inter-junction-box cable XX3 → XX4 (KEB01571B to KEB01572B)",
        "type_function": "Carries CAN, supply and control signals from XX3 to XX4",
        "signal_form": "Mixed: CAN, digital, 24 V supply",
        "details": "15 × 1 mm² + 3 × 0.34 mm².",
        "classification_notes": "WH → T.628 (CAN Bus 0 H), GN → T.629 (CAN Bus 0 L). KEB01571B sheet 5.",
        "connector_type": "—", "connector_part_number": "—",
        "cables": [
            {
                "cable_id": "W25",
                "cable_part_number": "EEA5503",
                "connection_details": "15 × 1 mm² + 3 × 0.34 mm²",
                "length_mm": 850,        # KEB01571B sheet 5: 550 mm (XX3 side) + 300 mm (XX4 side)
                "junction_box_ref": "Junction Box XX3 → XX4",
                "notes": "Length 850 mm (KEB01571B sheet 5): 550 mm to XX3 + 300 mm to XX4. Wires 7–14 spare. BU → PE.",
                "wires": [
                    (1,  "WH", "Open/crane", "Terminal 628", "CAN Bus 0 High"),
                    (2,  "GN", "Open/crane", "Terminal 629", "CAN Bus 0 Low"),
                    (3,  "BN", "Open/crane", "Blind",         "Spare — blind"),
                    (4,  "1",  "Open/crane", "Terminal 160", "Supply +24 V"),
                    (5,  "2",  "Open/crane", "Terminal 800", "Ground 0 V"),
                    (6,  "3",  "Open/crane", "Terminal 109", "Winch overload NO"),
                    (7,  "4",  "Open/crane", "Terminal 140", "Winch overload NC"),
                    (8,  "5",  "K50/14",     "K50 relay",    "Relay K50 contact 14"),
                    (9,  "6",  "Open/crane", "Terminal 800", "Ground 0 V (additional)"),
                    (10, "7",  "Open/crane", "Blind",         "Spare"),
                    (11, "8",  "Open/crane", "Blind",         "Spare"),
                    (12, "9",  "Open/crane", "Blind",         "Spare"),
                    (13, "10", "Open/crane", "Blind",         "Spare"),
                    (14, "11", "Open/crane", "Blind",         "Spare"),
                    (15, "12", "Open/crane", "Blind",         "Spare"),
                    (16, "BU", "PE",          "Terminal PE",  "Protective earth"),
                ],
            }
        ],
    },
    # ── 27. Working Light Supply W26 (optional SCHEI03L) ─────────────────────
    {
        "order": 27,
        "device_ref": "W26",
        "part_number": "EEA 192",
        "description": "Working Light Supply — W26",
        "classification": "Electrically Powered Equipment (Lighting)",
        "designation": "Supply cable W26 for working light (optional — SCHEI = SCHEI03L only)",
        "type_function": "Carries 24 V supply for working light from XX3 to XX4",
        "signal_form": "24 V DC supply (relay-switched)",
        "details": "7 × 1.5 mm². Only installed if SCHEI = SCHEI03L.",
        "classification_notes": "PK/BK → T.56 (supply). WH/GN → T.806 (ground).",
        "connector_type": "—", "connector_part_number": "—",
        "cables": [
            {
                "cable_id": "W26",
                "cable_part_number": "EEA 192",
                "connection_details": "7 × 1.5 mm²",
                "length_mm": 0,          # TBD — not dimensioned in KEB01571B
                "junction_box_ref": "Junction Box XX3 → XX4",
                "notes": "Length TBD (not dimensioned in KEB01571B). Only if SCHEI = SCHEI03L.",
                "wires": [
                    (1, "PK", "Open/crane", "Terminal 56",  "Supply +24 V"),
                    (2, "WH", "Open/crane", "Terminal 806", "Ground 0 V"),
                    (3, "BK", "Open/crane", "Terminal 56",  "Supply +24 V (additional)"),
                    (4, "GN", "Open/crane", "Terminal 806", "Ground 0 V (additional)"),
                ],
            }
        ],
    },
    # ── 28. Floodlight 1 — H170 (XX4, optional SCHEI03L) ─────────────────────
    {
        "order": 28,
        "device_ref": "H170",
        "part_number": "EEA 170",
        "description": "Floodlight 1",
        "classification": "Electrically Powered Equipment (Lighting)",
        "designation": "LED floodlight 1 at crane arm — optional if SCHEI = SCHEI03L",
        "type_function": "High-power work area illumination on crane arm",
        "signal_form": "Constant 24 V DC supply",
        "details": "2 × 1.5 mm². Connector C170: DT 2P (EEA5044 plug, EEA14722 cap).",
        "classification_notes": "Optional — SCHEI03L only. XX4 T.56 (supply), T.806 (ground). KEB01572B sheet 3.",
        "connector_type": "DT 2P", "connector_part_number": "EEA5044",
        "cables": [
            {
                "cable_id": "W170",
                "cable_part_number": "EEA 170",
                "connection_details": "2 × 1.5 mm²",
                "length_mm": 0,          # TBD — not dimensioned in KEB01572B
                "junction_box_ref": "Junction Box XX4",
                "notes": "Length TBD (not dimensioned in KEB01572B). Only if SCHEI = SCHEI03L.",
                "wires": [
                    (1, "RD", "PIN 1 (C170)", "Terminal 56 (XX4)",  "Supply +24 V"),
                    (2, "BU", "PIN 2 (C170)", "Terminal 806 (XX4)", "Ground 0 V"),
                ],
            }
        ],
    },
    # ── 29. Floodlight 2 — H171 (XX4) ────────────────────────────────────────
    {
        "order": 29,
        "device_ref": "H171",
        "part_number": "EEA 170",
        "description": "Floodlight 2",
        "classification": "Electrically Powered Equipment (Lighting)",
        "designation": "LED floodlight 2 at crane arm",
        "type_function": "High-power work area illumination on crane arm",
        "signal_form": "Constant 24 V DC supply",
        "details": "2 × 1.5 mm². Connector C171: DT 2P (EEA5044 plug, EEA14722 cap). 2300 mm.",
        "classification_notes": "XX4 T.56 (supply), T.806 (ground). KEB01572B sheet 3.",
        "connector_type": "DT 2P", "connector_part_number": "EEA5044",
        "cables": [
            {
                "cable_id": "W171",
                "cable_part_number": "EEA 170",
                "connection_details": "2 × 1.5 mm²",
                "length_mm": 2300,       # KEB01572B sheet 3: "2300 mm"
                "junction_box_ref": "Junction Box XX4",
                "notes": "Length 2300 mm (KEB01572B sheet 3): 150 mm at XX4 + 30 mm at C171.",
                "wires": [
                    (1, "RD", "PIN 1 (C171)", "Terminal 56 (XX4)",  "Supply +24 V"),
                    (2, "BU", "PIN 2 (C171)", "Terminal 806 (XX4)", "Ground 0 V"),
                ],
            }
        ],
    },
    # ── 30. Return Oil Utilization Valve — Y190 (XX4) ────────────────────────
    {
        "order": 30,
        "device_ref": "Y190",
        "part_number": "EEA 169",
        "description": "Return Oil Utilization Valve",
        "classification": "Electromechanical Device",
        "designation": "Solenoid coil for return oil utilization valve — C190 GDM3009 (EEA13793)",
        "type_function": "Hydraulic valve coil actuation for return oil circuit",
        "signal_form": "Digital ON/OFF 24 V DC coil",
        "details": "2 × 1 mm². Connector C190: GDM3009 (EEA13793 plug). 1240 mm.",
        "classification_notes": "BN → T.190 (XX4), BU → T.800 (XX4). KEB01572B sheet 3.",
        "connector_type": "GDM3009", "connector_part_number": "EEA13793",
        "cables": [
            {
                "cable_id": "W190",
                "cable_part_number": "EEA 169",
                "connection_details": "2 × 1.0 mm²",
                "length_mm": 1240,       # KEB01572B sheet 3: "1240 mm"
                "junction_box_ref": "Junction Box XX4",
                "notes": "Length 1240 mm (KEB01572B sheet 3): 150 mm at XX4 + 50 mm at C190.",
                "wires": [
                    (1, "BN", "PIN 1 (C190)", "Terminal 190 (XX4)", "Coil supply +24 V"),
                    (2, "BU", "PIN 2 (C190)", "Terminal 800 (XX4)", "Coil ground 0 V"),
                ],
            }
        ],
    },
    # ── 31. Winch Overload Switch — B9 (XX4) ─────────────────────────────────
    {
        "order": 31,
        "device_ref": "B9",
        "part_number": "CPEE0400",
        "description": "Winch Overload Switch",
        "classification": "Binary Sensor",
        "designation": "Winch overload / limit switch at crane arm (XX4)",
        "type_function": "Detects winch overload or end-position condition",
        "signal_form": "Digital ON/OFF (4 × 0.34 mm² screened)",
        "details": "4 × 0.34 mm². Also routed to XX2 via W503.",
        "classification_notes": "BN → T.190, BU → T.800, WH → T.140, BK → T.109 (XX4). KEB01572B sheet 3.",
        "connector_type": "M12", "connector_part_number": "EEA3900",
        "cables": [
            {
                "cable_id": "W9",
                "cable_part_number": "CPEE0400",
                "connection_details": "4 × 0.34 mm²",
                "length_mm": 0,          # TBD — shown as "xxx mm" in KEB01572B
                "junction_box_ref": "Junction Box XX4",
                "notes": "Length TBD (shown as 'xxx mm' in KEB01572B sheet 3). WH terminated blind at device side.",
                "wires": [
                    (1, "BN", "Pin 1", "Terminal 190 (XX4)", "Sensor supply / signal"),
                    (2, "WH", "Pin 2", "Terminal 140 (XX4)", "Signal NC — blind at device end"),
                    (3, "BU", "Pin 3", "Terminal 800 (XX4)", "Ground 0 V"),
                    (4, "BK", "Pin 4", "Terminal 109 (XX4)", "Signal NO contact"),
                ],
            }
        ],
    },
    # ── 32. Lubrication Pump Motor 1 — C17 (optional ZS002) ──────────────────
    {
        "order": 32,
        "device_ref": "C17",
        "part_number": "EEA4379",
        "description": "Lubrication Pump Motor 1",
        "classification": "Electromechanical Device",
        "designation": "Electric lubrication pump motor 1 — C17 GDM3009 (EEA13793) — optional ZS002",
        "type_function": "Drives automatic grease lubrication pump — only if ZSCHM = ZS002",
        "signal_form": "Digital ON/OFF 24 V DC motor drive",
        "details": "4 × 0.75 mm². Connector C17: GDM3009 (EEA13793). Only installed if ZSCHM = ZS002.",
        "classification_notes": "Optional. YE → T.17, BN → T.800, GN → PE, WH blind. KEB01571B sheet 9.",
        "connector_type": "GDM3009", "connector_part_number": "EEA13793",
        "cables": [
            {
                "cable_id": "W17",
                "cable_part_number": "EEA4379",
                "connection_details": "4 × 0.75 mm²",
                "length_mm": 0,          # TBD — not dimensioned in KEB01571B
                "junction_box_ref": "Junction Box XX3",
                "notes": "Length TBD (KEB01571B sheet 9). Only if ZSCHM = ZS002.",
                "wires": [
                    (1, "YE", "PIN 1 (C17)", "Terminal 17",  "Motor supply"),
                    (2, "BN", "PIN 2 (C17)", "Terminal 800", "Motor ground 0 V"),
                    (3, "GN", "PIN 3 (C17)", "Terminal PE",  "Protective earth"),
                    (4, "WH", "—",            "Blind",         "Unused — blind heat shrink"),
                ],
            }
        ],
    },
    # ── 33. Lubrication Pump Motor 2 — C18 (optional ZS002) ──────────────────
    {
        "order": 33,
        "device_ref": "C18",
        "part_number": "EEA4379",
        "description": "Lubrication Pump Motor 2",
        "classification": "Electromechanical Device",
        "designation": "Electric lubrication pump motor 2 — C18 GDM3009 (EEA13793) — optional ZS002",
        "type_function": "Drives automatic grease lubrication pump — only if ZSCHM = ZS002",
        "signal_form": "Digital ON/OFF 24 V DC motor drive",
        "details": "4 × 0.75 mm². Connector C18: GDM3009 (EEA13793). Only installed if ZSCHM = ZS002.",
        "classification_notes": "Optional. YE → T.17, BN → T.800, GN → PE, WH blind. KEB01571B sheet 9.",
        "connector_type": "GDM3009", "connector_part_number": "EEA13793",
        "cables": [
            {
                "cable_id": "W18",
                "cable_part_number": "EEA4379",
                "connection_details": "4 × 0.75 mm²",
                "length_mm": 0,          # TBD — not dimensioned in KEB01571B
                "junction_box_ref": "Junction Box XX3",
                "notes": "Length TBD (KEB01571B sheet 9). Only if ZSCHM = ZS002.",
                "wires": [
                    (1, "YE", "PIN 1 (C18)", "Terminal 17",  "Motor supply"),
                    (2, "BN", "PIN 2 (C18)", "Terminal 800", "Motor ground 0 V"),
                    (3, "GN", "PIN 3 (C18)", "Terminal PE",  "Protective earth"),
                    (4, "WH", "—",            "Blind",         "Unused — blind heat shrink"),
                ],
            }
        ],
    },
]


class Command(BaseCommand):
    help = "Load PFM1200 device/cable/wire data (KEB01571B + KEB01572B)"

    def add_arguments(self, parser):
        parser.add_argument("--flush", action="store_true", help="Delete existing data before loading")

    def handle(self, *args, **options):
        if options["flush"]:
            self.stdout.write("Flushing existing PFM1200 data...")
            PFM1200WireTerminal.objects.all().delete()
            PFM1200Cable.objects.all().delete()
            PFM1200Device.objects.all().delete()

        total_devices = total_cables = total_wires = 0

        for d in DEVICES:
            device, created = PFM1200Device.objects.update_or_create(
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
                cable, _ = PFM1200Cable.objects.update_or_create(
                    device=device,
                    cable_id=c["cable_id"],
                    defaults={
                        "cable_part_number":  c["cable_part_number"],
                        "connection_details": c["connection_details"],
                        "length_mm":          c.get("length_mm", 0),
                        "junction_box_ref":   c["junction_box_ref"],
                        "notes":              c["notes"],
                    },
                )
                total_cables += 1

                PFM1200WireTerminal.objects.filter(cable=cable).delete()
                for wire in c["wires"]:
                    PFM1200WireTerminal.objects.create(
                        cable=cable,
                        order=wire[0],
                        wire_color=wire[1],
                        device_pin=wire[2],
                        terminal_ref=wire[3],
                        notes=wire[4],
                    )
                    total_wires += 1

            status = "Created" if created else "Updated"
            ref = d.get("device_ref", "")
            self.stdout.write(f"  {status:8s} [{d['order']:2d}] {ref:5s} {d['description']}")

        self.stdout.write(self.style.SUCCESS(
            f"\nDone. {total_devices} devices, {total_cables} cables, {total_wires} wire terminals loaded."
        ))
