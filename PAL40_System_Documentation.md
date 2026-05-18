# PALTRONIC 40 (PAL40) — Technical Electrical Documentation
## Marine Crane Control System — Connector-Level Engineering Reference

**Document scope:** Connector C70 (Molex Blue) and C71 (Molex Grey)  
**System:** PALTRONIC 40 ECU — Crane overload protection and motion control  
**Reference standards:** IEC 13849 PL c, EN 13852  
**Prepared for:** Django-based engineering documentation system

---

# SYSTEM OVERVIEW

## What is the PALTRONIC 40?

The PALTRONIC 40 (PAL40) is PALFINGER's main electronic control unit for marine crane overload protection (OLP) and motion control. It serves as the central ECU that:

- Monitors all hydraulic boom angles and extension positions via analog sensors
- Reads hydraulic pressure on both piston and rod sides of the main cylinder
- Controls crane motions through hydraulic directional valves via digital outputs
- Enforces the Safe Working Load (SWL) envelope by cutting power to the emergency stop valve when overload is detected
- Communicates with remote control receivers, telematics modules, and peripheral I/O modules over two independent CAN bus networks
- Drives indicator lights, horns, beacons, and load meters to provide operator feedback

## Physical Architecture

The PAL40 uses two 56-pin Molex connectors:

| Connector | Color  | Primary Role |
|-----------|--------|--------------|
| C70       | Blue   | Main motion commands, pressure sensing, CAN Bus 0, emergency stop, battery feed |
| C71       | Grey   | Remote control, auxiliary functions, CAN Bus 1, load indicators, winch safety |

## Electrical Characteristics

| Parameter | Value |
|-----------|-------|
| Supply voltage | 8–32 V DC |
| Max total load current | 10 A |
| Operating temperature | −40 °C to +60 °C |
| Safety level | IEC 13849 PL c |
| CAN networks | 2 independent buses |
| Analog inputs | 4–20 mA current loop |
| Digital I/O | Active-high/Active-low logic |

## Signal Category Summary

| Category | C70 Pins | C71 Pins |
|----------|----------|----------|
| Ground (GND) | 1–13, 27, 41, 55 | 1–14 |
| Protected battery supply (UIN) | 43–54 | 43–56 |
| Battery positive (main) | 56 | 16 |
| CAN Bus 0 (H/L) | 15, 29 | — |
| CAN Bus 1 (H/L) | — | 15, 29 |
| Emergency stop chain | 14, 16, 17, 28 | — |
| Lever digital inputs | 18–20, 32–34 | 23–24, 33–38 |
| Limit switch inputs | 21–23, 35–38 | 25–28, 39–42 |
| Analog pressure inputs | 25–26, 39–40 | — |
| Digital outputs (actuators/indicators) | 42 | 17–22, 31 |

---

# CONNECTOR C70 — MOLEX BLUE

## 1. Connector Overview

**Connector designation:** C70  
**Connector type:** 56-pin Molex connector, blue housing  
**Role in PAL40 architecture:** Primary motion control and safety interface  

C70 is the primary ECU connector. It carries:

- All main boom axis lever command inputs (main boom, knuckle boom, slewing)
- Analog hydraulic pressure sensor signals (piston side and rod side, 4–20 mA current loop)
- The complete emergency stop valve control chain (Y0)
- CAN Bus 0 — the main internal machine bus connecting slewing sensors, outer boom sensors, and I/O modules
- External emergency stop chain inputs from safety relays
- The overload horn output (H5)
- Main battery supply (56) and the protected sensor supply outputs (pins 43–54)
- Sensor ground returns for B310, B312, B314, and Y0

**Connected subsystems:**
- Hydraulic boom control valves (via emergency stop valve Y0)
- Boom angle sensors B310, B312, B314 (slewing, main boom, knuckle boom)
- Hydraulic pressure sensors (piston and rod)
- CAN Bus 0 network (slewing controller, outer boom controller, IO modules)
- Overload horn H5
- Emergency stop chain

---

## 2. Pin-by-Pin Description — C70

### Ground Pins (1–13, 27, 41, 55)

| Pin | Cable | Wire Color | Terminal / Device | Notes |
|-----|-------|------------|-------------------|-------|
| 1   | —     | —          | —                 | chassis ground |
| 2   | —     | —          | —                 | chassis ground |
| 3   | —     | —          | —                 | chassis ground |
| 4   | —     | —          | —                 | chassis ground |
| 5   | W312  | YE         | B312 Pin 5        | sensor signal ground — Main Boom sensor |
| 6   | W310  | YE         | B310 Pin 3        | sensor signal ground — Slewing sensor |
| 7   | —     | —          | —                 | chassis ground |
| 8   | —     | —          | —                 | chassis ground |
| 9   | —     | —          | —                 | chassis ground |
| 10  | —     | —          | —                 | chassis ground |
| 11  | —     | —          | —                 | chassis ground |
| 12  | —     | —          | —                 | chassis ground |
| 13  | —     | —          | —                 | chassis ground |
| 27  | W0    | YE         | Y0 Pin 3          | ground return for emergency stop valve coil |
| 41  | W5    | BK         | H5 (Overload Horn) | ground return for overload horn |
| 55  | W70   | BU         | Terminal 800      | CAN/signal common ground — harness W70 |

**Signal type:** Ground (GND)  
**Direction:** Reference / Return  

Ground pins provide the 0 V reference for all sensors, actuators, and logic circuits connected to C70. Sensor-specific ground pins (5, 6, 27, 41) are routed through the sensor harnesses rather than directly to chassis to keep signal returns clean and reduce noise on analog sensor lines.

---

### Pin 14 — Emergency Stop: Support Enable

| Field | Value |
|-------|-------|
| Signal type | Digital Output |
| Cable | W0 |
| Wire color | GN (Green) |
| Terminal | Y0 Pin 2 |
| Device | Y0 — Emergency Stop Valve |
| Direction | Output |

**Function:** This output drives the support-enable coil of the emergency stop valve Y0. In the PAL40 safety architecture, Y0 is a normally-closed hydraulic solenoid valve positioned in the main hydraulic feed to the crane circuit. The PAL40 must actively energize Y0 to allow any crane motion.

Pin 14 controls the "support" or "pilot" energization — it enables the valve only when all pre-conditions (no overload, no external E-stop, boom within envelope) are satisfied.

**Safety logic:** If the PAL40 detects overload via pressure sensors or boom angle, pin 14 de-energizes. Y0 closes, cutting hydraulic flow to all crane functions. The crane halts regardless of any operator lever input.

---

### Pin 15 — CAN Bus 0 Low

| Field | Value |
|-------|-------|
| Signal type | CAN Bus (differential pair, Low wire) |
| Cable | W70 |
| Wire color | YE (Yellow) |
| Terminal | 628 |
| Direction | Bidirectional |

**Function:** CAN Bus 0 Low signal wire. Together with Pin 29 (CAN High), these form the differential CAN bus pair for Bus 0.

CAN Bus 0 connects the PAL40 to:
- Slewing angle/position sensor node
- Outer boom angle sensor node
- Peripheral I/O expansion modules

The PAL40 reads boom geometry data from CAN sensors to compute the current load radius and compare against the rated capacity chart.

**Electrical:** ISO 11898, 250 kbit/s or 500 kbit/s, 120 Ω termination at each bus end.

---

### Pin 16 — External Emergency Stop Chain 2

| Field | Value |
|-------|-------|
| Signal type | Digital Input |
| Cable | W70 |
| Wire color | BK (Black) |
| Terminal | 101 |
| Direction | Input |

**Function:** Input from the second channel of the external emergency stop safety relay chain. This is part of the dual-channel E-stop monitoring architecture required by IEC 13849 PL c.

When this input goes low (circuit opened by E-stop button or safety relay drop-out), the PAL40 immediately de-energizes Y0, halting all crane motions.

**Safety logic:** Pins 16 and 17 (Chain 1 and Chain 2) are monitored independently. If either channel opens, the crane stops. The PAL40 also cross-checks both channels; a discrepancy between them (one open, one closed for extended period) is flagged as a safety fault.

---

### Pin 17 — External Emergency Stop Chain 1

| Field | Value |
|-------|-------|
| Signal type | Digital Input |
| Cable | W70 |
| Wire color | GY (Grey) |
| Terminal | 102 |
| Direction | Input |

**Function:** First channel of the external emergency stop safety chain. Operates in parallel with Pin 16 for dual-channel redundancy. See Pin 16 for safety logic.

---

### Pin 18 — Knuckle Boom Up (Lever)

| Field | Value |
|-------|-------|
| Signal type | Digital Input |
| Cable | W314 |
| Wire color | WH (White) |
| Terminal | B314 Pin 1 |
| Device | B314 — Knuckle Boom Sensor |
| Direction | Input |

**Function:** Lever command input for knuckle boom (inner boom / jib) upward motion. The signal originates from the proportional lever transducer assembly B314. When the operator moves the knuckle boom lever to the "up" direction, B314 Pin 1 goes active, commanding the PAL40 to enable the corresponding hydraulic directional control valve.

**Note:** The lever sensor B314 provides both the up (Pin 1, WH) and down (Pin 2, GN) commands. The PAL40 processes these as discrete directional commands, not as a continuous analog position signal.

---

### Pin 19 — Main Boom Up (Lever)

| Field | Value |
|-------|-------|
| Signal type | Digital Input |
| Cable | W312 |
| Wire color | WH (White) |
| Terminal | B312 Pin 1 |
| Device | B312 — Main Boom Sensor |
| Direction | Input |

**Function:** Lever command input for main boom raise motion. Active signal from B312 Pin 1 requests the PAL40 to enable main boom-up hydraulic valve output. The PAL40 validates this command against the load moment envelope before passing the output to the valve.

---

### Pin 20 — Slewing Left (Lever)

| Field | Value |
|-------|-------|
| Signal type | Digital Input |
| Cable | W310 |
| Wire color | WH (White) |
| Terminal | B310 Pin 1 |
| Device | B310 — Slewing Sensor |
| Direction | Input |

**Function:** Lever command for crane rotation to the left (counter-clockwise when viewed from above). B310 Pin 1 goes active when the slewing lever is deflected left. The PAL40 enables the slewing hydraulic valve only when:
- No overload condition exists
- Emergency stop chain is intact
- Slewing is not blocked by a zone restriction

---

### Pin 21 — Top Stop Stabilizer B (NC Contact)

| Field | Value |
|-------|-------|
| Signal type | Digital Input |
| Cable | — (not specified) |
| Wire color | — |
| Terminal | — |
| Direction | Input |

**Function:** Normally-closed limit switch input for Stabilizer B top-stop position. The NC contact is used for fail-safe detection — a broken wire or disconnected sensor will open the NC circuit, which the PAL40 interprets as "limit reached," preventing further movement in that direction. This is a standard safety practice for physical end-stop protection.

---

### Pin 22 — FPI2: Stabilizer A (NC Contact)

| Field | Value |
|-------|-------|
| Signal type | Digital Input |
| Cable | — |
| Wire color | — |
| Terminal | — |
| Direction | Input |

**Function:** FPI2 (Free Position Indicator 2) — Normally-closed interlock input for Stabilizer A. Used as a pre-condition check: the PAL40 monitors whether stabilizers are deployed before allowing crane operation. An open NC contact here indicates the stabilizer is not in its required locked position, and the PAL40 may inhibit crane lifting operations accordingly.

---

### Pins 23–24 — End Layer / Overload Winch 2 (NC Contacts)

| Pin | Function | Signal type | Direction |
|-----|----------|-------------|-----------|
| 23  | End Layer Winch 2 — Boom A (NC) | Digital Input | Input |
| 24  | Overload Winch 2 — Boom B (NC) | Digital Input | Input |

**Function:** Normally-closed safety input contacts for the second winch assembly. Pin 23 signals that the winch rope has reached the end layer (minimum drum wraps) and further lowering is dangerous. Pin 24 signals an overload condition on the second winch (excess rope tension). Both use NC contacts for fail-safe behavior.

---

### Pin 25 — Pressure Rod Sensor (4–20 mA) — Signal Wire A

| Field | Value |
|-------|-------|
| Signal type | Analog Input (4–20 mA current loop) |
| Cable | W70 |
| Wire color | WH (White) |
| Terminal | 105 |
| Direction | Input |

**Function:** One conductor of the 4–20 mA current loop for the hydraulic rod-side pressure sensor (600 bar range). The rod-side sensor measures the hydraulic pressure acting on the annular area (rod side) of the main boom hydraulic cylinder. See Pin 39 for the second conductor of this loop.

**Signal characteristics:** 4 mA = 0 bar, 20 mA = 600 bar. The PAL40 ADC converts the current signal to a pressure value used in the load moment calculation.

---

### Pin 26 — Pressure Piston Sensor (4–20 mA) — Signal Wire A

| Field | Value |
|-------|-------|
| Signal type | Analog Input (4–20 mA current loop) |
| Cable | W70 |
| Wire color | VT (Violet) |
| Terminal | 103 |
| Direction | Input |

**Function:** One conductor of the 4–20 mA current loop for the hydraulic piston-side pressure sensor (600 bar range). The piston-side pressure acts over the full bore area of the main boom cylinder and is the primary load-bearing pressure. See Pin 40 for the second conductor.

**Signal characteristics:** 4 mA = 0 bar, 20 mA = 600 bar.

---

### Pin 28 — Emergency Stop Solenoid: Crane Enable

| Field | Value |
|-------|-------|
| Signal type | Digital Output |
| Cable | W0 |
| Wire color | WH (White) |
| Terminal | Y0 Pin 1 |
| Device | Y0 — Emergency Stop Valve |
| Direction | Output |

**Function:** Main solenoid drive output to Y0 emergency stop valve. This output, combined with Pin 14, provides the dual coil energization of the Y0 valve. Pin 28 carries the primary energization current for the crane-enable solenoid.

**Safety logic:** De-energizing Pin 28 closes Y0, which immediately blocks hydraulic supply to all crane functions. This is the final-stage actuator in the overload protection chain. The PAL40 de-energizes this output upon any of the following:
- Overload detected (load > 100% SWL)
- Emergency stop input activated (Pins 16/17)
- CAN bus communication failure with critical nodes
- Internal PAL40 self-test failure

---

### Pin 29 — CAN Bus 0 High

| Field | Value |
|-------|-------|
| Signal type | CAN Bus (differential pair, High wire) |
| Cable | W70 |
| Wire color | GN (Green) |
| Terminal | 629 |
| Direction | Bidirectional |

**Function:** CAN Bus 0 High signal wire. Together with Pin 15 (CAN Low), forms the ISO 11898 differential pair for Bus 0. See Pin 15 for full bus description.

---

### Pin 30 — Overload Protection (OLP) Input

| Field | Value |
|-------|-------|
| Signal type | Digital Input |
| Cable | — |
| Wire color | — |
| Terminal | — |
| Direction | Input |

**Function:** External overload protection signal input. This pin receives an override or interlock signal related to the overload protection function. In some crane configurations this is connected to an external OLP relay or a remote interlock that can trigger crane halt independent of the internal PAL40 calculation.

---

### Pin 31 — Pendulum Input

| Field | Value |
|-------|-------|
| Signal type | Analog / Digital Input |
| Cable | — |
| Wire color | — |
| Terminal | — |
| Direction | Input |

**Function:** Pendulum (inclinometer / heel angle) sensor input. Marine cranes installed on vessels must compensate for vessel motion. The pendulum sensor measures the inclination of the crane base relative to true vertical, allowing the PAL40 to adjust the effective load radius calculation when the vessel is heeled.

---

### Pins 32–34 — Boom Down / Slewing Right (Lever Inputs)

| Pin | Function | Cable | Wire | Terminal | Device |
|-----|----------|-------|------|----------|--------|
| 32  | Knuckle boom down | W314 | GN   | B314 Pin 2 | B314 Knuckleboom |
| 33  | Main boom down    | W312 | GN   | B312 Pin 2 | B312 Mainboom |
| 34  | Slewing right     | W310 | GN   | B310 Pin 2 | B310 Slewing |

**Signal type:** Digital Input  
**Direction:** Input  

**Function:** Lever command inputs for the reverse direction of each axis:
- Pin 32: Knuckle boom lower motion command
- Pin 33: Main boom lower motion command
- Pin 34: Crane rotation to the right (clockwise viewed from above)

The convention for B310/B312/B314 is: **Pin 1 (WH) = positive direction (up/left), Pin 2 (GN) = negative direction (down/right)**. This wiring convention is consistent across all boom lever sensors.

---

### Pins 35–38 — Limit Switch Inputs (NO Contacts)

| Pin | Function |
|-----|----------|
| 35  | Top Stop — Stabilizer B (NO contact) |
| 36  | FPI2 — Stabilizer A (NO contact) |
| 37  | End layer Winch 2 — Boom B (NO contact) |
| 38  | Overload Winch 2 — Boom A (NO contact) |

**Signal type:** Digital Input  
**Direction:** Input  

**Function:** Normally-open companion contacts to Pins 21–24. The PAL40 monitors both the NC and NO contacts of each limit switch simultaneously. This dual-contact monitoring provides:
- Fail-safe detection (NC opens = limit triggered, even if NO fails)
- Contact weld detection (if both contacts show the same state when they should differ, a stuck contact is flagged)

---

### Pin 39 — Pressure Rod Sensor (4–20 mA) — Signal Wire B

| Field | Value |
|-------|-------|
| Signal type | Analog Input (4–20 mA current loop) |
| Cable | W70 |
| Wire color | GY/PK (Grey/Pink) |
| Terminal | 106 |
| Direction | Input |

**Function:** Second conductor (return path) of the rod-side pressure sensor current loop. Together with Pin 25, completes the 4–20 mA loop for the rod-side pressure sensor. Terminal 106 is the current loop return referenced to Terminal 105.

---

### Pin 40 — Pressure Piston Sensor (4–20 mA) — Signal Wire B

| Field | Value |
|-------|-------|
| Signal type | Analog Input (4–20 mA current loop) |
| Cable | W70 |
| Wire color | BN (Brown) |
| Terminal | 104 |
| Direction | Input |

**Function:** Second conductor (return path) of the piston-side pressure sensor current loop. Together with Pin 26, completes the 4–20 mA loop for the piston-side pressure sensor. Terminal 104 is the current loop return referenced to Terminal 103.

---

### Pin 42 — Horn H5 (Overload Horn)

| Field | Value |
|-------|-------|
| Signal type | Digital Output |
| Cable | W5 |
| Wire color | RD (Red) |
| Terminal | H5 (supply terminal) |
| Device | H5 — Overload Horn |
| Direction | Output |

**Function:** Drives the overload warning horn H5. The PAL40 activates this output when the computed load exceeds a programmable threshold (typically 90–100% SWL). The horn alerts the operator and slinging crew that the crane is approaching or has exceeded the safe working load.

**Ground return:** Pin 41 (W5, BK wire) provides the ground return for H5. Both supply and ground are routed through the PAL40 connector to allow the ECU to fully control the horn circuit.

---

### Protected Battery Supply Pins (43–54)

| Pin | Cable | Wire Color | Terminal / Device |
|-----|-------|------------|-------------------|
| 43  | —     | —          | — |
| 44  | —     | —          | — |
| 45  | —     | —          | — |
| 46  | W314  | BN         | B314 Pin 4 — Knuckleboom sensor supply |
| 47  | W312  | BN         | B312 Pin 4 — Mainboom sensor supply |
| 48  | W310  | BN         | B310 Pin 4 — Slewing sensor supply |
| 49  | —     | —          | — |
| 50  | —     | —          | — |
| 51  | —     | —          | — |
| 52  | —     | —          | — |
| 53  | —     | —          | — |
| 54  | —     | —          | — |

**Signal type:** Power Output (Protected Supply, UIN1)  
**Direction:** Output  

**Function:** The PAL40 provides a regulated, short-circuit-protected battery supply to connected sensors and peripheral devices. "Protected" means the supply is internally current-limited and monitored — a short circuit on a sensor cable will not damage the ECU but will be flagged as a wiring fault.

Pins 46, 47, 48 supply the sensor excitation voltage to B314 (knuckle boom), B312 (main boom), and B310 (slewing) respectively via the brown wire on Pin 4 of each sensor connector. This is a standard 4-wire sensor wiring arrangement: supply (BN), ground (YE), command up (WH), command down (GN).

---

### Pin 56 — Battery Positive (Main Supply)

| Field | Value |
|-------|-------|
| Signal type | Power Input |
| Cable | W70 |
| Wire color | RD (Red) |
| Terminal | 160 — via fuse F160 |
| Direction | Input |

**Function:** Main battery supply input to the PAL40 ECU. Protected by fuse F160 in the power distribution panel. This is the primary 12 V or 24 V DC supply that powers all PAL40 internal logic, output drivers, and sensor supply regulators.

---

## 3. Device Explanations — C70

### Y0 — Emergency Stop Valve

| Field | Value |
|-------|-------|
| Device type | Hydraulic solenoid valve (normally closed) |
| Pins used | C70: 14 (support enable), 27 (ground), 28 (crane enable) |
| Cable | W0 |

**Mechanical/hydraulic function:** Y0 is a two-coil, normally-closed electrohydraulic valve positioned in the main hydraulic supply circuit of the crane. When de-energized, its spring returns to the closed position, blocking all hydraulic flow to crane functions. The crane is hydraulically locked in a fail-safe state.

**Why PAL40 requires this:** The PAL40 overload protection system must be able to instantly stop all crane motions when an overload is detected, an emergency stop is pressed, or a system fault occurs. Y0 is the final actuating element — de-energize it and the crane stops regardless of operator inputs.

**Three-wire control (Pins 14, 27, 28):**
- Pin 27 (YE, Y0 Pin 3): Valve coil ground return
- Pin 28 (WH, Y0 Pin 1): Primary crane-enable coil
- Pin 14 (GN, Y0 Pin 2): Support-enable coil

**Typical signal:** 12 V or 24 V DC at the solenoid coil; current draw typically 0.5–1.5 A depending on coil specification.

---

### B310 — Slewing Sensor

| Field | Value |
|-------|-------|
| Device type | Angle / position transducer with integral lever microswitch |
| C70 Pins | 6 (GND), 20 (left cmd), 34 (right cmd), 48 (supply) |
| Cable | W310 |

**Mechanical function:** B310 is mounted on the slewing mechanism and detects rotation angle and lever commands. The sensor provides directional lever switch outputs (left/right) used by the PAL40 to determine the operator's requested slewing direction.

**4-wire connection (W310 harness):**
- Pin 4 (BN) → C70 Pin 48: Protected supply
- Pin 3 (YE) → C70 Pin 6: Signal ground
- Pin 1 (WH) → C70 Pin 20: Slewing left active
- Pin 2 (GN) → C70 Pin 34: Slewing right active

**Why PAL40 requires this:** The PAL40 must know the current slewing direction command to apply zone-dependent load restrictions and to correctly execute the control logic. In zones where the load radius is larger (crane slewing outboard on a vessel), tighter SWL limits apply.

---

### B312 — Main Boom Sensor

| Field | Value |
|-------|-------|
| Device type | Angle / position transducer with integral lever microswitch |
| C70 Pins | 5 (GND), 19 (up cmd), 33 (down cmd), 47 (supply) |
| Cable | W312 |

**Mechanical function:** B312 measures the main boom (outer boom) elevation angle. The boom angle is a critical input for load radius calculation: as the boom lowers, load radius increases, and SWL decreases. B312 also contains the lever switch that sends up/down commands to the PAL40.

**Why PAL40 requires this:** The PAL40's overload protection algorithm uses boom angle to determine the current load radius. Without this signal, the crane cannot compute whether the current load is within the rated capacity chart. Loss of B312 signal causes an immediate crane halt.

---

### B314 — Knuckle Boom Sensor

| Field | Value |
|-------|-------|
| Device type | Angle / position transducer with integral lever microswitch |
| C70 Pins | 18 (up cmd), 32 (down cmd), 46 (supply) |
| Cable | W314 |
| C71 Pins | — |

**Mechanical function:** B314 measures the knuckle boom (inner boom / jib) angle. On a knuckle-boom crane, both the main boom and knuckle boom angles together determine the crane's horizontal reach (load radius). The PAL40 uses both B312 and B314 readings simultaneously in its geometric load radius calculation.

---

### H5 — Overload Horn

| Field | Value |
|-------|-------|
| Device type | Acoustic warning indicator |
| C70 Pins | 41 (GND), 42 (drive) |
| Cable | W5 |

**Function:** Electric horn that sounds when the crane load approaches or exceeds the SWL. Provides audible warning to operator and ground crew.

**Why PAL40 drives this directly:** The PAL40 monitors load as a percentage of SWL and activates H5 at a programmable threshold (commonly 90% or 100%). The horn is wired directly to PAL40 outputs so the ECU has full control over the alarm timing and pattern.

---

### Pressure Sensors — Piston Side and Rod Side (600 bar, 4–20 mA)

| Field | Value |
|-------|-------|
| Device type | Hydraulic pressure transducer |
| Range | 0–600 bar |
| Signal | 4–20 mA current loop |
| C70 Piston pins | 26 (Wire A) + 40 (Wire B) |
| C70 Rod pins | 25 (Wire A) + 39 (Wire B) |

**Mechanical/hydraulic function:**

The main boom is raised and lowered by a double-acting hydraulic cylinder. The PAL40 measures pressure on both sides:

- **Piston side:** Pressure acting over the full bore area (driving force for lifting)
- **Rod side:** Counter-pressure acting over the annular area (back-pressure during lifting)

The net force on the cylinder — and therefore the actual load — is calculated from the differential pressure:

```
F = (P_piston × A_bore) − (P_rod × A_annular)
```

Combined with the boom geometry (angle and extension), this force gives the load moment from which the actual hook load is derived and compared to the SWL chart.

**Why two wires per sensor (terminals 103+104, 105+106):** 4–20 mA current loop sensors require two conductors: one carrying the loop current from the transmitter, one returning it. Terminals 103/104 form the piston loop; 105/106 form the rod loop.

**Signal characteristics:**
- 4 mA = 0 bar (sensor powered, zero pressure)
- 20 mA = 600 bar (full scale)
- < 3.5 mA = broken wire / sensor fault

---

## 4. Signal Flow — C70

### Main Boom Lift Operation

```
Operator deflects main boom lever UP
  → B312 Pin 1 (WH) goes HIGH
    → C70 Pin 19 reads HIGH (main boom up command)
      → PAL40 checks: load moment OK? E-stop chain intact? CAN Bus 0 healthy?
        → If OK: PAL40 energizes Y0 (Pins 14 + 28)
          → Hydraulic valve opens → main boom rises
            → B312 CAN node or angle change updates load radius
              → PAL40 recalculates load vs. SWL continuously
                → If load > 100% SWL: Pin 14/28 de-energize → Y0 closes → crane halts
```

### Overload Pressure Detection

```
Hook load increases
  → Hydraulic cylinder piston pressure rises
    → Piston sensor (4–20 mA) → C70 Pins 26 + 40 (current increases)
      → PAL40 ADC reads current, calculates pressure
        → Net force = (P_piston × A_bore) − (P_rod × A_annular)
          → Load moment = Force × Load_radius
            → If Load_moment > Rated_moment:
              → Pin 42 HIGH → H5 horn sounds
              → Pins 14/28 LOW → Y0 de-energizes → crane stopped
```

### Emergency Stop Chain

```
Emergency stop button pressed
  → Safety relay opens both channels
    → C70 Pin 16 (chain 2) goes LOW
    → C70 Pin 17 (chain 1) goes LOW
      → PAL40 detects E-stop condition
        → Pin 28 immediately de-energized (within < 20 ms)
          → Y0 valve closes
            → All crane motion stops
              → PAL40 holds E-stop status until reset condition met
```

### CAN Bus 0 Data Flow

```
Slewing sensor node (CAN Bus 0)
  → Broadcasts angle data frame every 10–20 ms
    → C70 Pin 15 (CAN Low) + Pin 29 (CAN High) carry differential signal
      → PAL40 CAN controller receives angle data
        → Updates load radius calculation
          → Adjusts SWL limits based on slewing zone
```

---

## 5. Safety Functions — C70

### Emergency Stop System

**Pins involved:** 14, 16, 17, 28, 27  
**Safety level:** IEC 13849 PL c (Category 3 architecture)  

The dual-channel emergency stop chain (Pins 16 + 17) implements a Category 3 safety architecture. Both channels are monitored independently. The PAL40 performs cross-channel plausibility checking at startup and periodically during operation.

Reaction time from E-stop activation to Y0 de-energization: typically < 20 ms.

### Overload Protection (OLP)

**Pins involved:** 25, 26, 39, 40 (pressure inputs), 14, 28 (Y0 outputs)  
**Algorithm:** Continuous load moment calculation  

The PAL40 calculates load moment 10–100 times per second. The load chart (SWL vs. radius) is stored internally. When actual load moment exceeds rated, Y0 is de-energized and H5 sounds. The crane is only allowed to move in the direction that reduces load moment (lowering, retracting).

### Stabilizer Interlock (FPI)

**Pins involved:** 21, 22, 35, 36  
**Logic:** NC + NO dual contact monitoring  

The PAL40 inhibits crane lifts above a configured low SWL (typically 10% of maximum) until both stabilizers (A and B) are confirmed deployed. The FPI (Free Position Indicator) contacts confirm stabilizer extension. Dual-contact monitoring (NC + NO) detects stuck or missing contacts.

### Winch Safety

**Pins involved:** 23, 24, 37, 38  
**Logic:** Dual-contact (NC + NO)  

End-layer detection prevents the winch from paying out rope until fewer than the minimum safe wraps remain on the drum. Winch overload detection prevents lifting loads that would cause rope or sheave damage.

---

## 6. Troubleshooting — C70

### Pressure Sensor Fault

| Symptom | Likely Cause | Diagnostic |
|---------|-------------|------------|
| PAL40 shows error: pressure sensor open circuit | Broken wire in W70 (Pins 25/39 or 26/40 loop) | Measure loop current: <3.5 mA = open circuit |
| PAL40 overload trips at low load | Piston sensor stuck at high value, or rod sensor stuck low | Disconnect sensor, measure signal current with calibrated source |
| Erratic load readings | Poor connection at terminals 103–106 | Inspect terminal crimps, check for corrosion at C70 pins |

**Diagnostic procedure — pressure loop:**
1. With crane powered and at rest (no load), measure current between Pin 25 and Pin 39: expect 4 mA (0 bar).
2. Apply known hydraulic pressure (test gauge); expect proportional current increase.
3. Current > 20.5 mA or < 3.5 mA = sensor fault.

---

### Emergency Stop Fault

| Symptom | Likely Cause | Diagnostic |
|---------|-------------|------------|
| Crane will not start, E-stop fault displayed | One or both E-stop chains open | Check continuity of W70 from C70 Pins 16/17 to terminal block 101/102 |
| E-stop fault clears but crane still won't move | Y0 coil open or driver fault | Measure voltage at C70 Pin 28 with E-stop reset: expect supply voltage |
| E-stop discrepancy fault | Pins 16 and 17 in different states for >100 ms | Inspect safety relay contacts for welding or sticking |

---

### CAN Bus 0 Fault

| Symptom | Likely Cause | Diagnostic |
|---------|-------------|------------|
| CAN Bus 0 timeout, angle sensor lost | Cable break in W70 differential pair | Measure bus voltage: Pin 29 (CAN H) should be 2.5–3.5 V; Pin 15 (CAN L) 1.5–2.5 V |
| CAN Bus 0 off bus, no communications | Missing termination or bus short | Measure Pin 29 to Pin 15 resistance with all nodes disconnected: expect 60 Ω (two 120 Ω terminators in parallel) |

---

### Sensor Supply Fault (Protected Battery Supply)

| Symptom | Likely Cause | Diagnostic |
|---------|-------------|------------|
| Multiple sensor signals lost simultaneously | Protected supply short circuit | Measure voltage at C70 Pin 46/47/48: expect battery voltage minus 0.5 V |
| One sensor supply lost | Wire break in BN wire of that sensor harness | Disconnect sensor, measure voltage at the harness connector Pin 4: expect supply voltage |

---

### Horn H5 Fault

| Symptom | Likely Cause | Diagnostic |
|---------|-------------|------------|
| No horn sound during overload | H5 driver output fault or broken circuit | Measure C70 Pin 42 voltage during overload: expect supply voltage |
| Horn sounds continuously | Driver stuck on, or short to supply | Disconnect Pin 42 from H5: if horn stops, fault is in ECU output; if continues, check for wiring short |

---

## 7. Django Data Model — C70

```python
# Suggested Django models for PAL40 C70 documentation

class Crane(models.Model):
    name = models.CharField(max_length=100)
    model_number = models.CharField(max_length=50)
    serial_number = models.CharField(max_length=50)

class ControlSystem(models.Model):
    crane = models.ForeignKey(Crane, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)        # "PALTRONIC 40"
    model = models.CharField(max_length=50)        # "PAL40"
    supply_voltage_min = models.FloatField()       # 8.0 V
    supply_voltage_max = models.FloatField()       # 32.0 V
    safety_level = models.CharField(max_length=20) # "PL c"
    max_current_a = models.FloatField()            # 10.0

class Connector(models.Model):
    control_system = models.ForeignKey(ControlSystem, on_delete=models.CASCADE)
    designation = models.CharField(max_length=10)  # "C70"
    color = models.CharField(max_length=20)        # "Blue"
    connector_type = models.CharField(max_length=50) # "Molex 56-pin"
    primary_role = models.TextField()

class Device(models.Model):
    DEVICE_TYPES = [
        ('sensor', 'Sensor'),
        ('actuator', 'Actuator'),
        ('switch', 'Switch / Limit Switch'),
        ('valve', 'Hydraulic Valve'),
        ('indicator', 'Indicator / Horn / Light'),
        ('relay', 'Relay'),
        ('other', 'Other'),
    ]
    identification = models.CharField(max_length=20)  # "B312", "Y0", "H5"
    name = models.CharField(max_length=100)            # "Main Boom Sensor"
    device_type = models.CharField(max_length=20, choices=DEVICE_TYPES)
    description = models.TextField()
    cable = models.CharField(max_length=20, blank=True)  # "W312"

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
    device = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True, blank=True)
    safety_related = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ('connector', 'pin_number')
        ordering = ['pin_number']

# Sample fixture data for C70 key pins
C70_PIN_DATA = [
    {
        "pin_number": 14,
        "function": "Emergency stop – support enable",
        "signal_type": "DO",
        "direction": "OUT",
        "cable": "W0",
        "wire_color": "GN",
        "terminal": "Y0 Pin 2",
        "device_id": "Y0",
        "safety_related": True,
        "description": "Drives support-enable coil of emergency stop valve Y0. De-energizing halts all crane motion."
    },
    {
        "pin_number": 15,
        "function": "CAN Bus 0 Low (slewing / outer boom / IO)",
        "signal_type": "CAN",
        "direction": "BIDI",
        "cable": "W70",
        "wire_color": "YE",
        "terminal": "628",
        "device_id": None,
        "safety_related": True,
        "description": "CAN Bus 0 differential Low wire. Carries sensor data from slewing, outer boom, and IO modules."
    },
    {
        "pin_number": 25,
        "function": "Pressure rod sensor (600 bar) – 4–20 mA wire A",
        "signal_type": "AI",
        "direction": "IN",
        "cable": "W70",
        "wire_color": "WH",
        "terminal": "105",
        "device_id": None,
        "safety_related": True,
        "description": "One conductor of the rod-side hydraulic pressure sensor current loop. 4 mA = 0 bar, 20 mA = 600 bar."
    },
    {
        "pin_number": 28,
        "function": "Emergency stop solenoid – crane enable",
        "signal_type": "DO",
        "direction": "OUT",
        "cable": "W0",
        "wire_color": "WH",
        "terminal": "Y0 Pin 1",
        "device_id": "Y0",
        "safety_related": True,
        "description": "Main solenoid drive for Y0 crane-enable coil. De-energized on overload, E-stop, or system fault."
    },
]
```

---

---

# CONNECTOR C71 — MOLEX GREY

## 1. Connector Overview

**Connector designation:** C71  
**Connector type:** 56-pin Molex connector, grey housing  
**Role in PAL40 architecture:** Auxiliary functions, remote control, and load indication interface  

C71 handles:

- CAN Bus 1 — the remote control and telematics bus (RRC receiver, telematics module, main boom CAN node)
- Warning and indicator outputs (flashing beacon H113, warning horn H6, working lights, load percentage LEDs)
- Winch safety inputs (end-layer and overload detection for winch 1)
- Extension boom and winch lever commands (B316 extensions, B318 winch)
- Auxiliary hydraulic functions (rotator, grapple, DV1 valve)
- Override and second-hand control inputs
- Secondary battery supply input (UIN2) for PAL40 output drivers
- FPI1 interlock inputs (stabilizer pre-conditions)
- Load limit selection inputs

**Connected subsystems:**
- CAN Bus 1 network (remote control receiver, telematics, main boom CAN sensor)
- Extension sensor B316 and winch control B318
- Flashing beacon H113
- Warning horn H6
- Working light relay K56
- DV1 hydraulic valve driver
- Winch 1 safety switches (end-layer, overload)

---

## 2. Pin-by-Pin Description — C71

### Ground Pins (1–14)

| Pin | Cable | Wire Color | Terminal / Device | Notes |
|-----|-------|------------|-------------------|-------|
| 1   | —     | —          | —                 | chassis ground |
| 2   | W71   | BU         | Terminal 800      | CAN/signal common ground — harness W71 |
| 3   | —     | —          | —                 | chassis ground |
| 4   | W6    | BK         | H6 (Warning Horn) | ground return for warning horn H6 |
| 5   | —     | —          | —                 | chassis ground |
| 6   | —     | —          | —                 | chassis ground |
| 7   | —     | —          | —                 | chassis ground |
| 8   | —     | —          | —                 | chassis ground |
| 9   | W316  | YE         | B316 Pin 3        | sensor signal ground — Extensions sensor |
| 10  | W318  | YE         | B318 Pin 3        | sensor signal ground — Winch/Extensions sensor |
| 11  | —     | —          | —                 | chassis ground |
| 12  | —     | —          | —                 | chassis ground |
| 13  | —     | —          | —                 | chassis ground |
| 14  | —     | —          | —                 | chassis ground |

**Signal type:** Ground (GND)  
**Direction:** Reference / Return  

Pin 2 provides the common W71 harness ground referenced to Terminal 800 — the same bus bar structure used by C70's Pin 55 (W70 ground). Pins 9 and 10 are dedicated sensor ground returns for B316 and B318, routed through the sensor cables to maintain clean signal returns.

---

### Pin 15 — CAN Bus 1 Low

| Field | Value |
|-------|-------|
| Signal type | CAN Bus (differential pair, Low wire) |
| Cable | W71 |
| Wire color | YE (Yellow) |
| Terminal | 620 |
| Direction | Bidirectional |

**Function:** CAN Bus 1 Low signal wire. Together with Pin 29 (CAN High), forms the ISO 11898 differential pair for Bus 1.

CAN Bus 1 connects the PAL40 to:
- RRC (Radio Remote Control) receiver
- Telematics module (fleet management, data logging)
- Main boom angle sensor CAN node

This bus is typically isolated from Bus 0 to prevent remote control CAN faults from affecting the primary safety-critical Bus 0 network.

---

### Pin 16 — Battery Positive Supply (UIN2)

| Field | Value |
|-------|-------|
| Signal type | Power Input |
| Cable | W71 |
| Wire color | RD (Red) |
| Terminal | 161 — via fuse F161 |
| Device | F161 — Paltronic outputs fuse |
| Direction | Input |

**Function:** Secondary battery supply for PAL40 output drivers. The PAL40 architecture uses two separate supply inputs:
- UIN1 (C70, Pin 56 via F160): Powers ECU logic and sensor supplies
- UIN2 (C71, Pin 16 via F161): Powers the output load drivers (horn, lights, valve solenoids)

Separating these supplies allows the logic to remain powered (for fault logging and diagnostics) even if the output driver supply trips on overload.

---

### Pin 17 — Warning Beacon (Flashing Light)

| Field | Value |
|-------|-------|
| Signal type | Digital Output |
| Cable | W71 |
| Wire color | BN (Brown) |
| Terminal | 111 |
| Device | H113 — Orange Flashlight (Flashing Beacon) |
| Direction | Output |

**Function:** Drives the orange flashing beacon H113. This beacon is activated by the PAL40 during:
- Active crane operation (as a visual warning to surrounding personnel)
- Overload condition
- RRC remote control operation (to indicate the crane is remotely controlled)

The beacon complies with marine crane safety requirements for visual warning signals.

---

### Pin 18 — Warning Horn H6

| Field | Value |
|-------|-------|
| Signal type | Digital Output |
| Cable | W6 |
| Wire color | RD (Red) |
| Terminal | H6 (supply terminal) |
| Device | H6 — Warning Horn |
| Direction | Output |

**Function:** Drives the warning horn H6. H6 is a general-purpose audible warning distinct from the overload horn H5 (on C70). H6 may be activated for:
- Remote control activation confirmation
- Operation zone entry warning
- General operator alert signals

**Ground return:** C71 Pin 4 (W6, BK) provides the H6 ground return.

---

### Pin 19 — 100% Load Indicator (FPO1)

| Field | Value |
|-------|-------|
| Signal type | Digital / Analog Output |
| Cable | — |
| Wire color | — |
| Terminal | — |
| Direction | Output |

**Function:** Output signal driving the 100% load indicator (full-scale overload warning). FPO1 (Free Programmable Output 1) drives a load indicator display or lamp that illuminates when the crane reaches 100% SWL. This is the maximum load warning — any further load increase will trigger the overload protection and crane halt.

---

### Pin 20 — 90% Load Indicator (FPO2)

| Field | Value |
|-------|-------|
| Signal type | Digital / Analog Output |
| Cable | — |
| Wire color | — |
| Terminal | — |
| Direction | Output |

**Function:** Output signal driving the 90% load indicator. FPO2 (Free Programmable Output 2) activates when the load reaches 90% SWL, providing an early warning to the operator before reaching the hard overload limit. The operator can then slow down or reposition before triggering automatic protection.

---

### Pin 21 — Working Light

| Field | Value |
|-------|-------|
| Signal type | Digital Output |
| Cable | W71 |
| Wire color | BK (Black) |
| Terminal | K56 / A1 |
| Device | K56 — Working Light Relay |
| Direction | Output |

**Function:** Drives the coil of relay K56, which in turn switches the working light power circuit. The working light illuminates the crane working area during night operations or poor visibility conditions. The PAL40 controls this as a switched output through a relay (K56) to handle the high current required by the work light.

---

### Pin 22 — Load Limit C Out

| Field | Value |
|-------|-------|
| Signal type | Digital Output |
| Cable | — |
| Wire color | — |
| Terminal | — |
| Direction | Output |

**Function:** Output signal for Load Limit C — one of the selectable load limit configurations. Some PALFINGER cranes support multiple predefined load limit profiles (A, B, C) corresponding to different rigging configurations or operational modes. This output signals to external equipment which profile is currently active.

---

### Pin 23 — Extension Boom Retract (Lever)

| Field | Value |
|-------|-------|
| Signal type | Digital Input |
| Cable | W316 |
| Wire color | GN (Green) |
| Terminal | B316 Pin 1 |
| Device | B316 — Extensions Sensor |
| Direction | Input |

**Function:** Lever command input for extension boom retraction (telescoping in). B316 Pin 1 (GN wire) goes active when the operator commands extension retract. The PAL40 uses this to enable the retract hydraulic valve on the extension cylinder.

**4-wire connection (W316 harness):**
- Pin 4 (BN) → C71 Pin 51: Protected supply
- Pin 3 (YE) → C71 Pin 9: Signal ground
- Pin 1 (GN) → C71 Pin 23: Extension retract active
- Pin 2 (WH) → C71 Pin 37: Extension out active

---

### Pin 24 — Winch Down (Lever)

| Field | Value |
|-------|-------|
| Signal type | Digital Input |
| Cable | W318 |
| Wire color | WH (White) |
| Terminal | B318 Pin 2 |
| Device | B318 — Winch / Extensions Control |
| Direction | Input |

**Function:** Lever command input for winch lowering (paying out rope). B318 Pin 2 (WH wire) goes active when the operator commands winch down. The PAL40 enables the winch lower hydraulic valve only when the winch safety conditions are satisfied (no end-layer, no overload).

---

### Pin 25 — SE End Position (NO) — End Layer Winch 1

| Field | Value |
|-------|-------|
| Signal type | Digital Input |
| Cable | — |
| Wire color | — |
| Terminal | — |
| Direction | Input |

**Function:** Normally-open contact of the end-layer limit switch for winch 1. Indicates the winch drum has reached the minimum number of safe rope wraps. See Pin 39 for the NC companion contact.

---

### Pin 26 — SE Overload (NO) — Winch 1

| Field | Value |
|-------|-------|
| Signal type | Digital Input |
| Cable | W71 |
| Wire color | WH (White) |
| Terminal | 109 |
| Direction | Input |

**Function:** Normally-open contact of the winch 1 overload switch. Activates when winch rope tension exceeds the safe working load of the winch. The PAL40 halts winch hoisting when this contact closes, preventing rope breakage or sheave damage.

---

### Pin 27 — Load Limit C Select (NO)

| Field | Value |
|-------|-------|
| Signal type | Digital Input |
| Cable | — |
| Wire color | — |
| Terminal | — |
| Direction | Input |

**Function:** Normally-open contact of the Load Limit C selection input. When closed, the PAL40 switches to the Load Limit C configuration — a predefined reduced SWL profile for specific rigging conditions. See Pin 41 for the NC companion contact.

---

### Pin 28 — FPI1 (NO Contact)

| Field | Value |
|-------|-------|
| Signal type | Digital Input |
| Cable | — |
| Wire color | — |
| Terminal | — |
| Direction | Input |

**Function:** Normally-open contact of FPI1 (Free Position Indicator 1) — the first stabilizer interlock input. Operates in a dual-contact configuration with Pin 42 (NC). FPI1 monitors whether stabilizer set A is correctly deployed before the PAL40 allows full crane capacity lifting.

---

### Pin 29 — CAN Bus 1 High

| Field | Value |
|-------|-------|
| Signal type | CAN Bus (differential pair, High wire) |
| Cable | W71 |
| Wire color | GN (Green) |
| Terminal | 621 |
| Direction | Bidirectional |

**Function:** CAN Bus 1 High signal wire. Together with Pin 15 (CAN Low), forms the ISO 11898 differential pair for Bus 1. See Pin 15 for full bus description.

---

### Pin 30 — CAN Termination

| Field | Value |
|-------|-------|
| Signal type | CAN Bus Termination |
| Cable | — |
| Wire color | — (Stirrup/jumper) |
| Terminal | Stirrup |
| Direction | — |

**Function:** CAN Bus 1 termination point. A 120 Ω termination resistor (or stirrup/jumper that connects to an internal terminator) is installed here to properly terminate Bus 1 at the PAL40 end. Every CAN bus segment must have exactly two 120 Ω termination resistors — one at each physical end of the cable run.

**Note:** "Stirrup" in PALFINGER wiring terminology refers to a short jumper wire creating a loop or termination at this point. This is equivalent to selecting the internal terminator.

---

### Pin 31 — DV1 Valve Driver

| Field | Value |
|-------|-------|
| Signal type | Digital Output |
| Cable | W71 |
| Wire color | GY (Grey) |
| Terminal | 15 |
| Direction | Output |

**Function:** Output driver for DV1 — an auxiliary directional control valve. DV1 is a supplementary hydraulic valve used for auxiliary crane functions (e.g., a circuit selector, secondary function valve, or mode-switching valve). The PAL40 activates DV1 via this output in response to specific operator commands or automatic control logic.

---

### Pin 32 — Override Button / 2nd Hand

| Field | Value |
|-------|-------|
| Signal type | Digital Input |
| Cable | — |
| Wire color | — |
| Terminal | — |
| Direction | Input |

**Function:** Override / second operator enable button input. When activated, this allows limited crane motion beyond normal restrictions — used in specific maintenance or recovery procedures. This is a controlled override requiring deliberate operator action (typically a momentary pushbutton held during the overriding motion).

**Safety note:** Override functions are logged by the PAL40 and in some configurations require a key-switch or PIN code in addition to this button.

---

### Pins 33–36 — Rotator and Grapple (Lever Inputs)

| Pin | Function | Direction |
|-----|----------|-----------|
| 33  | Rotator left (LEVER) | Input |
| 34  | Rotator right (LEVER) | Input |
| 35  | Open grapple (LEVER) | Input |
| 36  | Close grapple (LEVER) | Input |

**Signal type:** Digital Input  
**Cable / Terminal:** Not specified (optional equipment)  

**Function:** These inputs receive lever commands for optional end-of-line accessories:
- **Rotator:** Hydraulic rotator for rotating suspended loads (left/right)
- **Grapple:** Hydraulic grapple / grab for handling bulk cargo or loose materials (open/close)

These functions are only active when the corresponding equipment is fitted and the PAL40 is configured to include these options.

---

### Pin 37 — Extension Boom Out (Lever)

| Field | Value |
|-------|-------|
| Signal type | Digital Input |
| Cable | W316 |
| Wire color | WH (White) |
| Terminal | B316 Pin 2 |
| Device | B316 — Extensions Sensor |
| Direction | Input |

**Function:** Lever command for extension boom extension (telescoping out). B316 Pin 2 (WH wire) goes active when the operator extends the boom. The PAL40 validates this command — extending the boom increases load radius and reduces allowable SWL, so the PAL40 continuously checks the load against the new radius as extension proceeds.

---

### Pin 38 — Winch Up (Lever)

| Field | Value |
|-------|-------|
| Signal type | Digital Input |
| Cable | W318 |
| Wire color | GN (Green) |
| Terminal | B318 Pin 1 |
| Device | B318 — Winch Control |
| Direction | Input |

**Function:** Lever command for winch hoisting (pulling in rope). B318 Pin 1 (GN wire) goes active for winch up. The PAL40 enables winch hoisting only when overload and end-layer conditions are clear.

**4-wire connection (W318 harness):**
- Pin 4 (BN) → C71 Pin 52: Protected supply
- Pin 3 (YE) → C71 Pin 10: Signal ground
- Pin 1 (GN) → C71 Pin 38: Winch up active
- Pin 2 (WH) → C71 Pin 24: Winch down active

---

### Pin 39 — End Layer Winch 1 (NC)

| Field | Value |
|-------|-------|
| Signal type | Digital Input |
| Cable | — |
| Wire color | — |
| Terminal | — |
| Direction | Input |

**Function:** Normally-closed contact of the winch 1 end-layer limit switch. The NC contact opens when the end-layer position is reached, providing fail-safe protection (broken wire = limit triggered). See Pin 25 (NO companion) for dual-contact monitoring.

---

### Pin 40 — Overload Winch 1 (NC)

| Field | Value |
|-------|-------|
| Signal type | Digital Input |
| Cable | W71 |
| Wire color | BU/RD (Blue/Red) |
| Terminal | 140 |
| Direction | Input |

**Function:** Normally-closed contact of the winch 1 overload switch. The NC contact opens when winch rope tension is excessive. Fail-safe behavior: broken wire or disconnected switch → contact appears open → PAL40 halts winch hoisting. See Pin 26 (NO companion) for dual-contact monitoring.

---

### Pin 41 — Load Limit C Select (NC)

| Field | Value |
|-------|-------|
| Signal type | Digital Input |
| Cable | — |
| Wire color | — |
| Terminal | — |
| Direction | Input |

**Function:** Normally-closed contact of the Load Limit C selector. Dual-contact companion to Pin 27 (NO). The PAL40 uses both contacts to confirm a clean contact operation and detect failures.

---

### Pin 42 — FPI1 (NC Contact)

| Field | Value |
|-------|-------|
| Signal type | Digital Input |
| Cable | — |
| Wire color | — |
| Terminal | — |
| Direction | Input |

**Function:** Normally-closed contact of FPI1 (stabilizer A interlock). NC companion to Pin 28 (NO). Dual-contact architecture confirms stabilizer deployment reliably and detects stuck contacts.

---

### Protected Battery Supply Pins (43–56)

| Pin | Cable | Wire Color | Terminal / Device |
|-----|-------|------------|-------------------|
| 43  | —     | —          | — |
| 44  | —     | —          | CAN termination point (internal) |
| 45  | —     | —          | — |
| 46  | —     | —          | — |
| 47  | —     | —          | — |
| 48  | —     | —          | — |
| 49  | —     | —          | — |
| 50  | —     | —          | — |
| 51  | W316  | BN         | B316 Pin 4 — Extensions sensor supply |
| 52  | W318  | BN         | B318 Pin 4 — Winch sensor supply |
| 53  | —     | —          | — |
| 54  | —     | —          | — |
| 55  | —     | —          | — |
| 56  | —     | —          | — |

**Signal type:** Power Output (Protected Supply)  
**Direction:** Output  

Pins 51 and 52 supply the excitation voltage to the extension (B316) and winch (B318) sensors respectively. Pin 44 coincides with the CAN termination function as noted for the C71 connector architecture.

---

## 3. Device Explanations — C71

### H113 — Orange Flashing Beacon

| Field | Value |
|-------|-------|
| Device type | Visual indicator (rotating or strobe beacon) |
| C71 Pin | 17 (drive output) |
| Cable | W71 |

**Function:** Safety beacon that visually signals crane operation status. Activated automatically by PAL40 during crane motion, overload, or remote control mode. Marine cranes are typically required by classification society rules to have an active warning light visible from 360° around the crane when it is in operation.

---

### H6 — Warning Horn

| Field | Value |
|-------|-------|
| Device type | Acoustic warning indicator |
| C71 Pins | 4 (GND), 18 (drive output) |
| Cable | W6 |

**Function:** General-purpose warning horn distinct from the overload-specific horn H5. H6 is used for non-overload warning conditions such as remote control activation, zone boundary warnings, or operator alerts.

---

### B316 — Extension Sensor

| Field | Value |
|-------|-------|
| Device type | Position transducer / lever switch assembly |
| C71 Pins | 9 (GND), 23 (retract cmd), 37 (out cmd), 51 (supply) |
| Cable | W316 |

**Mechanical function:** B316 measures the extension boom position (how far the telescoping section is extended). This measurement is critical because extension directly affects load radius. As the boom extends, the horizontal distance from the crane centerline to the hook increases, reducing the allowable SWL.

**PAL40 use:** Continuous extension position data is used in the geometric load radius calculation alongside main boom and knuckle boom angles.

---

### B318 — Winch Control

| Field | Value |
|-------|-------|
| Device type | Lever switch assembly (winch motion commands) |
| C71 Pins | 10 (GND), 24 (down cmd), 38 (up cmd), 52 (supply) |
| Cable | W318 |

**Mechanical function:** B318 provides the operator's winch control commands (hoist up / lower down). It is a lever-type switch rather than a position sensor — it generates discrete on/off commands that the PAL40 routes to the winch hydraulic valve, subject to safety checks.

**Why PAL40 monitors this:** The PAL40 must validate winch commands against the winch overload and end-layer safety switches before enabling the hydraulic valve.

---

### K56 — Working Light Relay

| Field | Value |
|-------|-------|
| Device type | Electromechanical relay |
| C71 Pin | 21 (coil drive) |
| Terminal | K56 / A1 |

**Function:** Power relay that switches the working light circuit. The PAL40 drives the relay coil (Pin 21), and the relay contacts switch the higher-current working light load. This protects the PAL40 output drivers from the lamp's inrush current.

---

### DV1 — Auxiliary Directional Valve

| Field | Value |
|-------|-------|
| Device type | Hydraulic solenoid directional control valve |
| C71 Pin | 31 |
| Cable | W71 |

**Function:** An auxiliary hydraulic valve for supplementary crane functions. DV1 is controlled directly by PAL40 Pin 31 for functions such as circuit mode selection, a secondary hydraulic function, or a pilot valve in a more complex hydraulic circuit.

---

### RRC Receiver (via CAN Bus 1)

| Field | Value |
|-------|-------|
| Device type | Radio Remote Control receiver |
| C71 Pins | 15 (CAN1 Low), 29 (CAN1 High), 30 (termination) |
| Bus | CAN Bus 1 |

**Function:** The RRC (Radio Remote Control) receiver translates radio signals from the portable remote control handset into CAN bus messages on Bus 1. The PAL40 reads these CAN messages and treats them as operator commands, subject to the same safety validation as local lever commands. CAN Bus 1 isolation ensures that RRC communication faults cannot affect the primary safety Bus 0.

---

## 4. Signal Flow — C71

### Remote Control Operation

```
Operator presses winch-up on RRC handset
  → RRC receiver decodes radio signal
    → RRC sends CAN message on Bus 1: "Winch UP commanded"
      → C71 Pins 15/29 carry CAN1 differential signal
        → PAL40 CAN1 controller receives winch-up command
          → PAL40 checks: winch overload OK (Pin 26/40)? End layer OK (Pin 25/39)?
            → If OK: PAL40 energizes winch valve (via Y0, already enabled via C70)
              → Winch hoists → load increases
                → If winch overload switch opens: Pin 40 (NC) goes HIGH
                  → PAL40 halts winch motion
```

### Extension Boom Operation with Load Check

```
Operator commands extension boom out
  → B316 Pin 2 (WH) → C71 Pin 37 goes HIGH
    → PAL40 reads extension out command
      → PAL40 checks current load moment at current radius
        → Extension increases radius → new load moment calculated
          → If new load moment < SWL: extension valve enabled
            → Boom extends → radius increases → SWL decreases
              → If load moment approaches SWL during extension:
                → PAL40 blocks further extension
                → Horn H5 (C70 Pin 42) activates
```

### Warning Beacon Activation

```
Crane enters operation mode
  → PAL40 activates working output
    → C71 Pin 17 drives H113 beacon (orange flashing light)
      → Beacon flashes at programmed rate
        → Personnel in crane area alerted to active crane operation
```

### Load Percentage Indication

```
PAL40 continuously calculates load as % of SWL
  → At 90% SWL:
    → C71 Pin 20 (FPO2) activates → 90% indicator illuminates
    → Warning Horn H6 (Pin 18) may pulse
  → At 100% SWL:
    → C71 Pin 19 (FPO1) activates → 100% indicator illuminates
    → H5 overload horn (C70 Pin 42) activates
    → Y0 valve (C70 Pins 14/28) de-energizes → crane halts
```

---

## 5. Safety Functions — C71

### Winch Overload Protection

**Pins involved:** 25, 26 (NO contacts), 39, 40 (NC contacts)  
**Logic:** Dual-contact (NC + NO) monitoring  

The PAL40 monitors both NC and NO contacts of the winch 1 overload and end-layer switches. Discrepancy detection (both contacts same state) flags a switch fault. In any fault condition, the PAL40 defaults to the safe state (winch stopped).

### FPI1 Stabilizer Interlock

**Pins involved:** 28 (NO), 42 (NC)  
**Logic:** Crane operations restricted to reduced SWL until FPI1 confirms stabilizer deployment  

The FPI1 dual-contact pair provides confirmation of stabilizer A deployment. Combined with FPI2 on C70 Pins 22/36 (stabilizer B), the PAL40 allows full crane capacity only when both stabilizers are confirmed deployed and locked.

### Load Limit C Selection (Safety Override Reduction)

**Pins involved:** 27 (NO), 41 (NC)  
**Logic:** Operator-selectable reduced SWL profile  

Load Limit C reduces the crane's permitted SWL to a predefined lower value — used when operating with specific rigging configurations (e.g., multi-leg slings, reduced hook block) that require a derated capacity.

### Override / 2nd Hand Control

**Pin involved:** 32  
**Logic:** Momentary override, requires deliberate operator action  

The override button allows limited motion beyond normal protective restrictions. This is a logged, controlled bypass — not an emergency defeat switch. The PAL40 enforces time limits and logging on all override activations.

---

## 6. Troubleshooting — C71

### CAN Bus 1 (Remote Control) Fault

| Symptom | Likely Cause | Diagnostic |
|---------|-------------|------------|
| Remote control unresponsive | CAN Bus 1 open circuit | Measure Pin 29 (CAN H) to Pin 15 (CAN L): expect 60 Ω (powered off, both ends terminated) |
| Intermittent remote control commands | Loose connector at C71 Pins 15 or 29 | Inspect W71 connector crimps and backshell, wiggle test while monitoring CAN traffic |
| CAN Bus 1 off-bus error | Missing or double termination | Check Pin 30 stirrup/terminator, verify only one external termination on Bus 1 |

---

### Winch Safety Switch Fault

| Symptom | Likely Cause | Diagnostic |
|---------|-------------|------------|
| Winch will not hoist, no operator error | NC contact open (Pin 40 or 39) | With powered system, measure C71 Pin 39 and 40: NC contact = high voltage when switch closed |
| PAL40 shows winch switch discrepancy fault | NC and NO contacts both same state | Disconnect winch switch, measure contact resistance directly: NC = < 1 Ω closed, NO = >10 MΩ open |

---

### Warning Beacon / Horn Fault

| Symptom | Likely Cause | Diagnostic |
|---------|-------------|------------|
| Beacon H113 not flashing | Open circuit in W71 BN wire or H113 lamp/LED failed | Measure C71 Pin 17 voltage during operation: expect supply voltage when active |
| Warning horn H6 continuous | PAL40 output stuck, or short to supply on W6 RD | Disconnect Pin 18 from H6: if horn stops, PAL40 output fault; if continues, wiring short |

---

### Working Light Fault

| Symptom | Likely Cause | Diagnostic |
|---------|-------------|------------|
| Working light does not come on | Relay K56 coil not energized, or contacts failed | Measure C71 Pin 21 voltage during light ON command: expect supply voltage to relay coil |
| Working light always on | K56 contacts welded | De-energize Pin 21 (remove command): light should go off; if it stays on, K56 contacts are welded |

---

### Extension Sensor Fault (B316)

| Symptom | Likely Cause | Diagnostic |
|---------|-------------|------------|
| Extension commands not responding | No supply to B316 (Pin 51), or broken signal wire | Measure C71 Pin 51 to Pin 9 (GND): expect supply voltage |
| Extension moves only one direction | One lever switch contact open | Measure C71 Pin 23 (retract) and Pin 37 (out) when commanding each direction |

---

## 7. Django Data Model — C71

```python
# Sample fixture data for C71 key pins — extends the same model classes defined for C70

C71_PIN_DATA = [
    {
        "pin_number": 15,
        "function": "CAN Bus 1 Low – Remote control / telemetry / Main Boom",
        "signal_type": "CAN",
        "direction": "BIDI",
        "cable": "W71",
        "wire_color": "YE",
        "terminal": "620",
        "device_id": None,
        "safety_related": True,
        "description": "CAN Bus 1 Low differential wire. Connects RRC receiver, telematics, and main boom sensor to PAL40."
    },
    {
        "pin_number": 16,
        "function": "Battery positive supply – UIN2 (Paltronic outputs)",
        "signal_type": "PWR",
        "direction": "IN",
        "cable": "W71",
        "wire_color": "RD",
        "terminal": "161 (F161)",
        "device_id": "F161",
        "safety_related": False,
        "description": "Secondary battery supply for PAL40 output drivers. Protected by fuse F161."
    },
    {
        "pin_number": 17,
        "function": "Warning beacon (flashing light) – H113",
        "signal_type": "DO",
        "direction": "OUT",
        "cable": "W71",
        "wire_color": "BN",
        "terminal": "111",
        "device_id": "H113",
        "safety_related": False,
        "description": "Drives orange flashing beacon H113 during crane operation and overload conditions."
    },
    {
        "pin_number": 29,
        "function": "CAN Bus 1 High – Remote control / telemetry / Main Boom",
        "signal_type": "CAN",
        "direction": "BIDI",
        "cable": "W71",
        "wire_color": "GN",
        "terminal": "621",
        "device_id": None,
        "safety_related": True,
        "description": "CAN Bus 1 High differential wire. Paired with Pin 15 for ISO 11898 Bus 1 communication."
    },
    {
        "pin_number": 40,
        "function": "Overload winch 1 (NC contact)",
        "signal_type": "DI",
        "direction": "IN",
        "cable": "W71",
        "wire_color": "BU/RD",
        "terminal": "140",
        "device_id": None,
        "safety_related": True,
        "description": "NC winch overload switch. Opens on excess rope tension. Fail-safe: broken wire = halts winch hoisting."
    },
]

# Signal type and direction choices are shared across both connectors
# Relational structure for Django admin and API

class SignalGroup(models.Model):
    """Logical grouping of related pins (e.g., pressure sensor loop, CAN pair, E-stop chain)"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    pins = models.ManyToManyField(Pin, related_name='signal_groups')

class TroubleshootingNote(models.Model):
    pin = models.ForeignKey(Pin, on_delete=models.CASCADE, related_name='troubleshooting')
    symptom = models.CharField(max_length=200)
    likely_cause = models.CharField(max_length=200)
    diagnostic_procedure = models.TextField()

class SafetyFunction(models.Model):
    SAFETY_LEVELS = [
        ('PL_c', 'PL c (IEC 13849)'),
        ('PL_d', 'PL d (IEC 13849)'),
        ('SIL_1', 'SIL 1'),
        ('SIL_2', 'SIL 2'),
    ]
    name = models.CharField(max_length=100)   # "Emergency Stop", "Overload Protection"
    safety_level = models.CharField(max_length=10, choices=SAFETY_LEVELS)
    description = models.TextField()
    pins = models.ManyToManyField(Pin, related_name='safety_functions')
    reaction_time_ms = models.IntegerField(null=True, blank=True)
```

---

---

# COMPLETE PIN REFERENCE TABLES

## C70 — Molex Blue: All 56 Pins

| Pin | Signal Type | Direction | Function | Cable | Wire Color | Terminal | Device | Safety |
|-----|-------------|-----------|----------|-------|------------|----------|--------|--------|
| 1   | GND | REF | Chassis ground | — | — | — | — | — |
| 2   | GND | REF | Chassis ground | — | — | — | — | — |
| 3   | GND | REF | Chassis ground | — | — | — | — | — |
| 4   | GND | REF | Chassis ground | — | — | — | — | — |
| 5   | GND | REF | Sensor ground — B312 | W312 | YE | B312 Pin 5 | B312 | — |
| 6   | GND | REF | Sensor ground — B310 | W310 | YE | B310 Pin 3 | B310 | — |
| 7   | GND | REF | Chassis ground | — | — | — | — | — |
| 8   | GND | REF | Chassis ground | — | — | — | — | — |
| 9   | GND | REF | Chassis ground | — | — | — | — | — |
| 10  | GND | REF | Chassis ground | — | — | — | — | — |
| 11  | GND | REF | Chassis ground | — | — | — | — | — |
| 12  | GND | REF | Chassis ground | — | — | — | — | — |
| 13  | GND | REF | Chassis ground | — | — | — | — | — |
| 14  | DO  | OUT | Emergency stop – support enable | W0 | GN | Y0 Pin 2 | Y0 | YES |
| 15  | CAN | BIDI | CAN Bus 0 Low | W70 | YE | Term. 628 | — | YES |
| 16  | DI  | IN  | External E-stop chain 2 | W70 | BK | Term. 101 | — | YES |
| 17  | DI  | IN  | External E-stop chain 1 | W70 | GY | Term. 102 | — | YES |
| 18  | DI  | IN  | Knuckle boom up (LEVER) | W314 | WH | B314 Pin 1 | B314 | — |
| 19  | DI  | IN  | Main boom up (LEVER) | W312 | WH | B312 Pin 1 | B312 | — |
| 20  | DI  | IN  | Slewing left (LEVER) | W310 | WH | B310 Pin 1 | B310 | — |
| 21  | DI  | IN  | Top Stop Stabilizer B (NC) | — | — | — | — | YES |
| 22  | DI  | IN  | FPI2 – Stabilizer A (NC) | — | — | — | — | YES |
| 23  | DI  | IN  | End Layer Winch 2 – Boom A (NC) | — | — | — | — | YES |
| 24  | DI  | IN  | Overload Winch 2 – Boom B (NC) | — | — | — | — | YES |
| 25  | AI  | IN  | Pressure rod sensor 4–20 mA (Wire A) | W70 | WH | Term. 105 | — | YES |
| 26  | AI  | IN  | Pressure piston sensor 4–20 mA (Wire A) | W70 | VT | Term. 103 | — | YES |
| 27  | GND | REF | Ground – Y0 valve coil return | W0 | YE | Y0 Pin 3 | Y0 | YES |
| 28  | DO  | OUT | Emergency stop solenoid – crane enable | W0 | WH | Y0 Pin 1 | Y0 | YES |
| 29  | CAN | BIDI | CAN Bus 0 High | W70 | GN | Term. 629 | — | YES |
| 30  | DI  | IN  | Overload protection (OLP) input | — | — | — | — | YES |
| 31  | AI  | IN  | Pendulum (inclinometer) | — | — | — | — | YES |
| 32  | DI  | IN  | Knuckle boom down (LEVER) | W314 | GN | B314 Pin 2 | B314 | — |
| 33  | DI  | IN  | Main boom down (LEVER) | W312 | GN | B312 Pin 2 | B312 | — |
| 34  | DI  | IN  | Slewing right (LEVER) | W310 | GN | B310 Pin 2 | B310 | — |
| 35  | DI  | IN  | Top Stop Stabilizer B (NO) | — | — | — | — | YES |
| 36  | DI  | IN  | FPI2 – Stabilizer A (NO) | — | — | — | — | YES |
| 37  | DI  | IN  | End layer Winch 2 – Boom B (NO) | — | — | — | — | YES |
| 38  | DI  | IN  | Overload Winch 2 – Boom A (NO) | — | — | — | — | YES |
| 39  | AI  | IN  | Pressure rod sensor 4–20 mA (Wire B) | W70 | GY/PK | Term. 106 | — | YES |
| 40  | AI  | IN  | Pressure piston sensor 4–20 mA (Wire B) | W70 | BN | Term. 104 | — | YES |
| 41  | GND | REF | Ground – H5 horn return | W5 | BK | H5 | H5 | — |
| 42  | DO  | OUT | Horn H5 – overload horn drive | W5 | RD | H5 | H5 | — |
| 43  | PWR | OUT | Protected battery supply (UIN1) | — | — | — | — | — |
| 44  | PWR | OUT | Protected battery supply | — | — | — | — | — |
| 45  | PWR | OUT | Protected battery supply | — | — | — | — | — |
| 46  | PWR | OUT | Protected supply – B314 sensor (BN) | W314 | BN | B314 Pin 4 | B314 | — |
| 47  | PWR | OUT | Protected supply – B312 sensor (BN) | W312 | BN | B312 Pin 4 | B312 | — |
| 48  | PWR | OUT | Protected supply – B310 sensor (BN) | W310 | BN | B310 Pin 4 | B310 | — |
| 49  | PWR | OUT | Protected battery supply | — | — | — | — | — |
| 50  | PWR | OUT | Protected battery supply | — | — | — | — | — |
| 51  | PWR | OUT | Protected battery supply | — | — | — | — | — |
| 52  | PWR | OUT | Protected battery supply | — | — | — | — | — |
| 53  | PWR | OUT | Protected battery supply | — | — | — | — | — |
| 54  | PWR | OUT | Protected battery supply | — | — | — | — | — |
| 55  | GND | REF | W70 common ground (Terminal 800) | W70 | BU | Term. 800 | — | — |
| 56  | PWR | IN  | Battery positive – main supply (F160) | W70 | RD | Term. 160 | F160 | — |

---

## C71 — Molex Grey: All 56 Pins

| Pin | Signal Type | Direction | Function | Cable | Wire Color | Terminal | Device | Safety |
|-----|-------------|-----------|----------|-------|------------|----------|--------|--------|
| 1   | GND | REF | Chassis ground | — | — | — | — | — |
| 2   | GND | REF | W71 common ground (Terminal 800) | W71 | BU | Term. 800 | — | — |
| 3   | GND | REF | Chassis ground | — | — | — | — | — |
| 4   | GND | REF | Ground – H6 horn return | W6 | BK | H6 | H6 | — |
| 5   | GND | REF | Chassis ground | — | — | — | — | — |
| 6   | GND | REF | Chassis ground | — | — | — | — | — |
| 7   | GND | REF | Chassis ground | — | — | — | — | — |
| 8   | GND | REF | Chassis ground | — | — | — | — | — |
| 9   | GND | REF | Sensor ground – B316 | W316 | YE | B316 Pin 3 | B316 | — |
| 10  | GND | REF | Sensor ground – B318 | W318 | YE | B318 Pin 3 | B318 | — |
| 11  | GND | REF | Chassis ground | — | — | — | — | — |
| 12  | GND | REF | Chassis ground | — | — | — | — | — |
| 13  | GND | REF | Chassis ground | — | — | — | — | — |
| 14  | GND | REF | Chassis ground | — | — | — | — | — |
| 15  | CAN | BIDI | CAN Bus 1 Low (RRC / telemetry / Main Boom) | W71 | YE | Term. 620 | — | YES |
| 16  | PWR | IN  | Battery positive – UIN2 (F161) | W71 | RD | Term. 161 | F161 | — |
| 17  | DO  | OUT | Warning beacon – H113 flashing light | W71 | BN | Term. 111 | H113 | — |
| 18  | DO  | OUT | Warning Horn H6 | W6 | RD | H6 | H6 | — |
| 19  | DO  | OUT | 100% load indicator – FPO1 | — | — | — | — | — |
| 20  | DO  | OUT | 90% load indicator – FPO2 | — | — | — | — | — |
| 21  | DO  | OUT | Working light – K56 relay coil | W71 | BK | K56/A1 | K56 | — |
| 22  | DO  | OUT | Load Limit C out | — | — | — | — | — |
| 23  | DI  | IN  | Extension boom retract (LEVER) | W316 | GN | B316 Pin 1 | B316 | — |
| 24  | DI  | IN  | Winch down (LEVER) | W318 | WH | B318 Pin 2 | B318 | — |
| 25  | DI  | IN  | SE end position (NO) – End layer winch 1 | — | — | — | — | YES |
| 26  | DI  | IN  | SE overload (NO) – Winch 1 | W71 | WH | Term. 109 | — | YES |
| 27  | DI  | IN  | Load Limit C select (NO) | — | — | — | — | — |
| 28  | DI  | IN  | FPI1 (NO) | — | — | — | — | YES |
| 29  | CAN | BIDI | CAN Bus 1 High (RRC / telemetry / Main Boom) | W71 | GN | Term. 621 | — | YES |
| 30  | CAN | — | CAN termination (stirrup) | — | Stirrup | — | — | — |
| 31  | DO  | OUT | DV1 auxiliary valve drive | W71 | GY | Term. 15 | DV1 | — |
| 32  | DI  | IN  | Override button / 2nd Hand | — | — | — | — | — |
| 33  | DI  | IN  | Rotator left (LEVER) | — | — | — | — | — |
| 34  | DI  | IN  | Rotator right (LEVER) | — | — | — | — | — |
| 35  | DI  | IN  | Open grapple (LEVER) | — | — | — | — | — |
| 36  | DI  | IN  | Close grapple (LEVER) | — | — | — | — | — |
| 37  | DI  | IN  | Extension boom out (LEVER) | W316 | WH | B316 Pin 2 | B316 | — |
| 38  | DI  | IN  | Winch up (LEVER) | W318 | GN | B318 Pin 1 | B318 | — |
| 39  | DI  | IN  | End layer winch 1 (NC) | — | — | — | — | YES |
| 40  | DI  | IN  | Overload winch 1 (NC) | W71 | BU/RD | Term. 140 | — | YES |
| 41  | DI  | IN  | Load Limit C select (NC) | — | — | — | — | — |
| 42  | DI  | IN  | FPI1 (NC) | — | — | — | — | YES |
| 43  | PWR | OUT | Protected battery supply | — | — | — | — | — |
| 44  | PWR | OUT | Protected battery supply / CAN termination | — | — | — | — | — |
| 45  | PWR | OUT | Protected battery supply | — | — | — | — | — |
| 46  | PWR | OUT | Protected battery supply | — | — | — | — | — |
| 47  | PWR | OUT | Protected battery supply | — | — | — | — | — |
| 48  | PWR | OUT | Protected battery supply | — | — | — | — | — |
| 49  | PWR | OUT | Protected battery supply | — | — | — | — | — |
| 50  | PWR | OUT | Protected battery supply | — | — | — | — | — |
| 51  | PWR | OUT | Protected supply – B316 sensor (BN) | W316 | BN | B316 Pin 4 | B316 | — |
| 52  | PWR | OUT | Protected supply – B318 sensor (BN) | W318 | BN | B318 Pin 4 | B318 | — |
| 53  | PWR | OUT | Protected battery supply | — | — | — | — | — |
| 54  | PWR | OUT | Protected battery supply | — | — | — | — | — |
| 55  | PWR | OUT | Protected battery supply | — | — | — | — | — |
| 56  | PWR | OUT | Protected battery supply | — | — | — | — | — |

---

# CROSS-REFERENCE: DEVICES TO PINS

| Device ID | Device Name | Type | C70 Pins | C71 Pins | Cable |
|-----------|-------------|------|----------|----------|-------|
| Y0 | Emergency Stop Valve | Hydraulic valve (NC solenoid) | 14, 27, 28 | — | W0 |
| B310 | Slewing Sensor | Position transducer + lever switch | 6 (GND), 20, 34, 48 | — | W310 |
| B312 | Main Boom Sensor | Position transducer + lever switch | 5 (GND), 19, 33, 47 | — | W312 |
| B314 | Knuckle Boom Sensor | Position transducer + lever switch | 18, 32, 46 | — | W314 |
| B316 | Extension Sensor | Position transducer + lever switch | — | 9 (GND), 23, 37, 51 | W316 |
| B318 | Winch Control | Lever switch assembly | — | 10 (GND), 24, 38, 52 | W318 |
| H5 | Overload Horn | Acoustic indicator | 41 (GND), 42 | — | W5 |
| H6 | Warning Horn | Acoustic indicator | — | 4 (GND), 18 | W6 |
| H113 | Orange Flashing Beacon | Visual indicator | — | 17 | W71 |
| K56 | Working Light Relay | Electromechanical relay | — | 21 | W71 |
| F160 | Main Supply Fuse | Fuse | 56 | — | W70 |
| F161 | Output Supply Fuse | Fuse | — | 16 | W71 |
| DV1 | Auxiliary Hydraulic Valve | Solenoid valve | — | 31 | W71 |

---

# WIRE COLOR CODE REFERENCE

| Code | Color | Typical use in this system |
|------|-------|---------------------------|
| WH   | White | Lever command positive direction / current loop signal |
| GN   | Green | Lever command negative direction / E-stop enable / CAN High |
| YE   | Yellow | Sensor signal ground / CAN Low |
| BK   | Black | Ground return for indicators |
| RD   | Red | Battery positive / horn drive supply |
| BN   | Brown | Sensor protected supply (Pin 4) / beacon |
| BU   | Blue | Common ground bus (Terminal 800) |
| GY   | Grey | E-stop chain 1 / auxiliary valve drive |
| VT   | Violet | Pressure sensor current loop |
| GY/PK | Grey-Pink | Pressure sensor return |
| BU/RD | Blue-Red | Winch overload switch |

---

# GLOSSARY

| Term | Definition |
|------|-----------|
| SWL | Safe Working Load — maximum rated load for a given boom configuration |
| OLP | Overload Protection — system that prevents operation beyond SWL |
| FPI | Free Position Indicator — switch confirming a stabilizer or outrigger is deployed |
| RRC | Radio Remote Control — wireless control system for the crane |
| CAN | Controller Area Network — ISO 11898 serial bus used between ECU and sensors |
| UIN1 | First battery supply input (logic and sensors) — fuse F160 |
| UIN2 | Second battery supply input (output drivers) — fuse F161 |
| NC | Normally Closed — switch contact closed at rest, opens when actuated |
| NO | Normally Open — switch contact open at rest, closes when actuated |
| FPO | Free Programmable Output — configurable output for indicators / external signals |
| DV1 | Directional Valve 1 — auxiliary hydraulic control valve |
| ECU | Electronic Control Unit |
| ADC | Analog-to-Digital Converter (within PAL40) |
| PL c | Performance Level c per IEC 13849 — safety integrity level |
| End Layer | Minimum safe number of rope wraps remaining on winch drum |
| Load Radius | Horizontal distance from crane rotation centerline to hook |
| Load Moment | Product of hook load × load radius, compared against rated chart |
