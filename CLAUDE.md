# Marine Crane Documentation — Project Overview

Django-based engineering documentation website for PALFINGER marine crane electrical systems.
Targets engineers and technicians who need pin-level electrical reference for the PAL40 ECU and the PFM2100 crane.

---

## Stack

| Layer | Technology |
|-------|-----------|
| Framework | Django 6.0.3 |
| Language | Python 3.13 |
| Database | SQLite (dev) |
| Frontend | Server-rendered HTML/CSS — dark GitHub-style theme |
| Dev server | `py manage.py runserver 8002` |

---

## Project Structure

```
marine-cranes-1/
├── manage.py
├── marine_cranes/          # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── context_processors.py   # Injects sidebar nav into all templates
├── pal40/                  # App: PALTRONIC 40 ECU connector documentation
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── templates/pal40/
│   │   ├── base.html           # Site-wide base with left sidebar
│   │   ├── index.html
│   │   ├── connector_detail.html
│   │   └── pin_detail.html
│   └── management/commands/
│       └── load_pal40_data.py
├── pfm2100/                # App: PFM2100 crane device registry
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py                # WireTerminalForm / CableMetaForm / make_wire_formset
│   ├── admin.py
│   ├── templates/pfm2100/
│   │   ├── device_list.html
│   │   ├── device_detail.html
│   │   ├── edit_cable_wiring.html  # Inline formset editor for wire terminals
│   │   └── schematic.html          # Interactive JS topology diagram
│   └── management/commands/
│       └── load_pfm2100_data.py
├── datasheet/              # Source PDFs (not in git LFS — add manually)
│   ├── Pal40Upgrade_IO.pdf
│   └── inf_eea-12238m_-.pdf
├── sheets/                 # Source Excel files
│   └── PFM2100 System.xlsx
└── PAL40_System_Documentation.md   # Full markdown reference document
```

---

## Apps

### `pal40` — PAL40 ECU Connector Documentation

Covers the PALTRONIC 40 control unit — PALFINGER's main ECU for crane overload protection and motion control.

**Models:**

| Model | Purpose |
|-------|---------|
| `Crane` | Top-level crane asset |
| `ControlSystem` | PAL40 ECU record (supply voltage, safety level) |
| `Connector` | C70 (Molex Blue) or C71 (Molex Grey) |
| `Device` | Sensor, valve, horn, relay, fuse connected to a pin |
| `Pin` | Individual pin — signal type, direction, cable, wire color, terminal, device FK |
| `SignalGroup` | M2M grouping of related pins (e.g. pressure loop pair) |
| `SafetyFunction` | Named safety function with IEC 13849 level and reaction time |
| `TroubleshootingNote` | Symptom / cause / diagnostic per pin |

**Pin signal types:** `DI` `DO` `AI` `AO` `CAN` `PWR` `GND`

**Load data:**
```
py manage.py load_pal40_data
py manage.py load_pal40_data --flush   # wipe and reload
```

**What is loaded:**
- 13 devices (B310, B312, B314, B316, B318, Y0, H5, H6, H113, K56, F160, F161, DV1)
- C70 — 56 pins (main boom, knuckle boom, slewing levers, pressure sensors 4–20 mA, CAN Bus 0, E-stop chain, Y0 valve, H5 horn)
- C71 — 56 pins (extension, winch levers, CAN Bus 1 RRC/telematics, load indicators FPO1/FPO2, H6 horn, H113 beacon, working light, winch safety switches)

**URLs:**

| URL | View |
|-----|------|
| `/` | PAL40 system overview + connector cards |
| `/connector/<pk>/` | Full 56-pin table with 8 columns matching source document |
| `/connector/<pk>/pin/<n>/` | Pin detail: device, safety functions, troubleshooting |

---

### `pfm2100` — PFM2100 Crane Device Registry

Documents all electrical devices fitted to the PFM2100 marine crane.

**Models:**

| Model | Purpose |
|-------|---------|
| `PFM2100Device` | Device with part number, classification, designation, signal form, connector type |
| `PFM2100Cable` | Cable connecting a device — ID (W205…), part number, cross-section, junction box ref |
| `PFM2100WireTerminal` | Individual wire row — color, device pin, terminal/connection reference |

**Load data:**
```
py manage.py load_pfm2100_data
py manage.py load_pfm2100_data --flush
```

**What is loaded — 21 devices:**

| # | Part Number | Description | Cable |
|---|------------|-------------|-------|
| 1 | EEA18563 | Slewing Encoder (CANopen SIL2) | W205 |
| 2 | EEA14709 | Mainboom Angle Sensor (CANopen SIL2) | W206 |
| 3 | EEA14709 | Knuckleboom Angle Sensor (CANopen SIL2) | W207 |
| 4 | EEA18779 | Pressure Sensor — Piston Side (600 bar SIL2) | W409 |
| 5 | EEA18779 | Pressure Sensor — Rod Side (600 bar SIL2) | W411 |
| 6 | EEA12214 | Winch Overload Switch (Inductive, PL d) | W9 |
| 7 | EEA15740 | Return Oil Utilization Valve (Bosch Rexroth D36) | W190 |
| 8 | EEA17497 | Flashlight — LED Strobe Beacon PDH-S23 | W113 |
| 9 | EEA13611 | Floodlight 1 — RokLUME 380N 84 W | W170 |
| 10 | EEA13611 | Floodlight 2 — RokLUME 380N 84 W | W171 |
| 11 | EEA11854 | Working Light — Scorpius N4402 50 W | W172 |
| 12 | EEA15360 | Telematic Unit — Danfoss CS100 IoT Gateway | W900 |
| 13 | CPEE0508A | Slip Ring Unit (CAN + power through slewing joint) | Integrated |
| 14 | EEA 773 | Emergency Stop Valve Plug Y0 (GAN-2000 PE2 LED) | W0 |
| 15 | EEA6193 | Overload Horn H5 — Piezo 90 dB IP67 | W5 |
| 16 | EEA6194 | Warning Horn H6 — Speaker alarm IP67 | W6 |
| 17 | — | Slewing Monitoring Switch | W10 |
| 18 | — | Mainboom Monitoring Switch | W312 |
| 19 | — | Knuckleboom Monitoring Switch | W314 |
| 20 | — | Extension Monitoring Switch | W316 |
| 21 | — | Winch Monitoring Switch | W318 |

Total: 85 wire terminals across 21 cables.

**Forms (`pfm2100/forms.py`):**

| Form / Factory | Purpose |
|---------------|---------|
| `WireTerminalForm` | ModelForm for a single `PFM2100WireTerminal` row (color dropdown, pin, terminal ref, notes) |
| `make_wire_formset(extra=1)` | Returns a `modelformset_factory` for wire terminals with delete support |
| `CableMetaForm` | ModelForm for `PFM2100Cable` header fields (cable ID, part number, junction box, etc.) |

**URLs:**

| URL | View |
|-----|------|
| `/pfm2100/` | Device registry table |
| `/pfm2100/device/<pk>/` | Full device detail: specs + cable table + wire/pin/terminal rows |
| `/pfm2100/cable/<pk>/edit/` | Inline edit — cable metadata + wire terminal formset, saves & redirects to device detail |
| `/pfm2100/schematic/` | Interactive topology diagram — draggable nodes, click to inspect cable wiring |

---

## Navigation

All pages share a persistent left sidebar (defined in `pal40/templates/pal40/base.html`) powered by the `marine_cranes.context_processors.sidebar_nav` context processor.

Sidebar sections:
- **PAL40** — System Overview, C70, C71
- **PFM2100** — Connector Map, System Schematic, All Devices + each device by name/part number

Active page is highlighted.

---

## Admin

Django admin at `/admin/` — username `admin`, password set via:
```
py manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
u = User.objects.get(username='admin')
u.set_password('YOUR_PASSWORD')
u.save()
"
```

---

## Reference Documents

| File | Content |
|------|---------|
| `PAL40_System_Documentation.md` | Full engineering reference — all 112 pins, device explanations, signal flows, safety logic, troubleshooting, Django model suggestions |
| `datasheet/Pal40Upgrade_IO.pdf` | PAL40 I/O pinout source |
| `datasheet/inf_eea-12238m_-.pdf` | PAL40 system specification EEA12238M |
| `sheets/PFM2100 System.xlsx` | PFM2100 device/cable source data |

---

## Key Electrical Concepts

- **PAL40** operates at 8–32 V DC, max 10 A, IEC 13849 PL c
- **C70** (Molex Blue): CAN Bus 0, main boom/knuckle/slewing levers, pressure sensors (4–20 mA), emergency stop chain Y0, overload horn H5
- **C71** (Molex Grey): CAN Bus 1 (RRC, telematics), extension/winch levers, load indicators, warning horn H6, flashing beacon H113
- **4-wire sensor convention**: BN = supply, YE = ground, WH = direction 1, GN = direction 2
- **Pressure sensors**: 4–20 mA current loop — 4 mA = 0 bar, 20 mA = 600 bar
- **Y0 Emergency Stop Valve**: normally closed — must be actively energized for crane to operate; de-energizes on overload, E-stop, or CAN fault
- **Dual-channel E-stop** (C70 pins 16 + 17): IEC 13849 Category 3 architecture

---

## Next Steps (suggested)

- Add `SignalGroup` and `SafetyFunction` fixtures for PAL40 pins
- Add PAL40 ↔ PFM2100 device cross-reference (e.g. link B310 Device to Slewing Monitoring Switch W10)
- Add a junction box view (Terminal 160, 800, 628, 629 … group all pins by terminal)
- Add search across pins and devices
- Improve schematic topology (persist node positions, add PAL40 ECU node, cable routing lines)
- PostgreSQL for production
