---
title: 'Self-Powered and Self-Regulating GPU Chips'
date: '2026-11-25'
weight: 10
slug: self-powered-gpu-chips
description: 'A feasibility program for recovering GPU waste heat as electricity: which conversion
  technologies could work at chip temperatures, what the thermodynamics allows, and where in the
  system the idea is strongest.'
tags:
  - research
  - energy
  - GPU
math: true
---
**A feasibility program for recovering GPU waste heat as electricity**

**Author:** Bhash Ganti (aka Bachi)

**(c) 2026 Bhash Ganti. Released under the Apache-2.0 License.**

bachipeachy@gmail.com · ORCID [0009-0007-3810-6520](https://orcid.org/0009-0007-3810-6520)

**Type:** Open research proposal. It reports no measurement yet, and invites contributors.

---

## Abstract

A modern GPU turns nearly all of the electricity it draws into heat. The industry treats that heat
as a problem to remove: heat spreaders, vapor chambers, liquid cooling and throttling all exist to
carry it away. This proposal asks a complementary question. Can a computing package convert a
measurable part of its own waste heat back into useful electricity, without hurting its cooling or
its computation?

We compare three conversion technologies: thermoelectric generators (TEG), thermophotovoltaics (TPV)
and thermoradiative devices (TR). A first-order estimate frames the problem honestly. At a GPU's
temperatures, far-field radiative conversion is bounded at a few milliwatts per square centimetre,
so TPV and TR matter only in near-field geometries. A thermoelectric layer in the main heat path
could recover about 1–2% of the heat flowing through it. It pays for that with tens of kelvin of
thermal headroom, which the cooler would otherwise use. Whether the trade is positive depends on
what that headroom costs, and that is the central measurement the program must make.

The idea is strongest in two places. The first is small, steady loads, such as sensors, telemetry and
fan control, where the harvester also measures the heat it converts. The second is the rack or
facility coolant loop, where heat from many GPUs gathers outside the chip's own thermal path. We
propose a staged program with explicit decision gates: a simulator first, then bench experiments,
then a real GPU. Package integration comes only after a measured positive net benefit.

The proposal does not claim that a GPU can power itself. It asks whether energy recovery can reduce
the net electricity computing needs, and it treats a well-measured negative result as a result.

## 1. Introduction: the energy we throw away

Computing hardware has changed beyond recognition. GPUs perform trillions of operations a second,
train and serve large AI models, and carry some of the world's most demanding workloads. That
progress costs energy. Electricity enters the processor, does computational work, and leaves almost
entirely as heat.

The industry has built an impressive toolkit to remove that heat:

- heat spreaders and heat sinks;
- vapor chambers and heat pipes;
- liquid and microchannel cooling;
- advanced thermal interface materials;
- thermal throttling.

These tools improve cooling and reliability. None of them tries to recover the energy the heat
carries. This proposal asks whether some of it can come back as electricity, and whether recovery
can become part of the computing package rather than a separate generation plant.

## 2. What this proposal claims, and what it does not

**The hypothesis.** A GPU package, or the cooling system around it, can carry a harvesting subsystem
that converts part of the heat into electricity. Dedicated circuitry conditions that electricity and
delivers it to selected loads, with a positive net benefit at some operating points.

The energy cycle is:

**Electrical input → computation → waste heat → conversion → recovered electricity → electrical loads**

Traditional GPU architecture balances four concerns: computation, memory and data movement, power
delivery and thermal management. The proposal adds a fifth: thermal energy recovery.

**What the title means.** "Self-powered" names the direction of travel, not a destination. A GPU
cannot run on its own heat (§6). The research asks how far toward that direction a real package can
move. "Self-regulating" names a feedback property. The harvested power tracks the heat flow, so the
harvester can also serve as a thermal sensor that needs no supply of its own (§5).

**What counts as success.** The program succeeds if it measures the net benefit honestly, whatever
its sign, under a stated system boundary (§8).

## 3. Candidate conversion technologies

A central task is to find which mechanism suits a GPU's temperatures and physical constraints. Three
deserve investigation.

### 3.1 Thermophotovoltaic conversion (TPV)

A TPV system heats an emitter, which radiates infrared light. A photovoltaic cell tuned to that light
converts it into current. TPV has reached high efficiencies at high emitter temperatures:

- Burger et al. (2022), from Lenert's group, reported 32.5% TPV efficiency at an emitter
  temperature of 1,036 °C, using a semitransparent cell that absorbs less than 1% of below-bandgap
  radiation.
- LaPotin et al. (2022) reported 41.1% at an emitter temperature of 2,400 °C.

**The research challenge.** These results do not transfer to a GPU. A GPU runs at roughly 60–95 °C,
more than a thousand kelvin below these emitters. The radiation a body emits falls with the fourth
power of its absolute temperature, and its spectrum shifts deep into the infrared. Section 7 shows
what that means in watts.

Two directions could change the picture:

- **Near-field TPV.** When emitter and cell sit closer than the thermal wavelength, of the order of
  micrometres, evanescent coupling can raise the radiative exchange above the blackbody limit
  (Mittapally et al. 2023). Zero-vacuum-gap designs pursue the same goal with an
  infrared-transparent spacer (Habibi et al. 2025).
- **Low-bandgap cells and selective emitters,** matched to the spectrum of a body near 350 K.

### 3.2 Thermoelectric conversion (TEG)

A thermoelectric generator turns a temperature difference directly into a voltage, through the
Seebeck effect. It needs a hot side, a cold side, a thermoelectric material and a load. It needs no
emitter and no optics.

A GPU package already has a gradient between the die and the cooler, which makes a TEG the natural
first experiment. It also exposes the hardest trade in this proposal. A TEG needs a temperature
difference across itself, so placing it in the heat path adds thermal resistance. If that raises the
junction temperature, or makes the cooler work harder, the recovered power may not pay for it.

Research directions:

- thin-film and micro-scale thermoelectric generators;
- lateral gradients and package-edge harvesting, away from the main heat path;
- thermoelectric structures inside heat spreaders.

### 3.3 Thermoradiative conversion (TR)

A thermoradiative device runs a semiconductor junction in reverse of a photovoltaic cell. A warm
diode radiates to a colder environment, and under the right non-equilibrium conditions the net
emission drives a current (Nielsen et al. 2024). Its appeal for this proposal is that it converts
heat leaving a warm body, rather than light arriving from a hot one. That suits sources near room
temperature, at least in principle. The related thermophotonic approach adds an electroluminescent
stage, and Sadi et al. (2022) assess its requirements for waste-heat harvesting.

### 3.4 Comparison

| Technology | Mechanism | Main challenge at GPU temperatures |
|---|---|---|
| TPV | Thermal photons into electricity | Far-field power density is tiny; near-field gaps are hard to build at scale |
| TEG | Temperature difference into electricity | It competes with the cooler for the same temperature difference |
| TR | Radiative emission into electricity | Practical power density and device integration |

The program picks no winner before it compares them in measurement.

## 4. Proposed architecture

The architecture has four cooperating subsystems.

### 4.1 The computational subsystem

This is the conventional GPU: processing cores, memory controllers, on-package memory, interconnects
and power delivery. Its job is still computation, and the first phases change nothing in it.

### 4.2 The harvesting subsystem

This is the addition. It captures heat from selected regions and converts it, using a thermoelectric
structure, a TPV emitter-cell pair, a thermoradiative structure, or a hybrid.

Where to place it is an open question. Candidates are the package perimeter, regions of the heat
spreader, the cold plate, and, at rack scale, the coolant loop (§7.3). The rule throughout is that
the harvester must not obstruct the primary cooling path.

### 4.3 Power conditioning and storage

A harvester's output has its own voltage, current and impedance, so it cannot feed the GPU's power
rails directly. A conditioning stage converts voltage, regulates current, tracks the maximum power
point, isolates where needed, measures the energy and may buffer it in a small capacitor.

The first implementations feed auxiliary loads only, never the high-current core rails.

### 4.4 Power management

A controller watches junction temperature, the thermal gradient, the harvested power, the conversion
efficiency, the cooler's operating point and the loads available. It decides whether to use, store or
discard the harvested energy. Thermal safety and electrical stability always come before recovery.

## 5. The self-regulating principle

A GPU's heat output follows its workload, and a harvester's output follows the heat. That gives a
feedback chain:

**GPU workload → heat → harvested power → measurement → allocation**

The chain carries two kinds of value, and they should be kept apart.

**Energy.** The harvested power is small (§7), so its energy value lies in loads that need little and
need it steadily.

**Information.** The harvested power is a direct, self-powered measure of local heat flow. A
thermoelectric element that powers its own readout can report a hot spot without drawing on the
GPU's supply. This may be the earliest practical payoff. A distributed array of self-powered
heat-flux sensors would feed the power manager real data at no electrical cost.

Two cautions apply. More heat does not always mean more useful power, because conversion depends on
the temperature difference, the coupling and the materials. Recovering more power does not lower the
GPU's temperature either. The controller therefore keeps thermal limits that do not depend on the
harvester.

A control policy:

1. Measure the thermal state.
2. Estimate the power available to harvest.
3. Measure the power actually recovered.
4. Work out the net benefit after conversion and conditioning losses.
5. Deliver it to permitted loads.
6. Reduce or disable harvesting whenever it compromises cooling or electrical stability.

The goal is not to generate electricity. It is to raise the whole system's energy efficiency.

## 6. Thermodynamic limits

A GPU cannot run on its own heat. That would mean recovering all the energy it consumes, with no
loss, which thermodynamics forbids.

For any heat engine working between a hot and a cold reservoir, the Carnot efficiency bounds the work
it can extract:

\(\displaystyle \eta_{\max} = 1 - \frac{T_c}{T_h}\)

Take a hot side at 80 °C (\(T_h = 353.15\) K) and a cold side at 25 °C (\(T_c = 298.15\) K). Then
\(\eta_{\max} \approx 15.6\%\). This is an ideal bound for the whole temperature difference
between die and room. Real devices reach a fraction of it, and the cooler needs part of that
difference to move the heat at all.

The practical lesson is that temperature differences are the scarce resource. The die-to-room
difference is small, and the cooler already spends it. That is why the program compares mechanisms
and placements rather than assuming one layer will solve the problem.

## 7. A first-order feasibility estimate

Before any experiment, simple physics bounds what each approach can deliver. The numbers below use a
GPU dissipating 700 W, typical of a current data-centre accelerator. The die is about 8 cm², under a
lid of about 25 cm².

### 7.1 Far-field radiation is bounded at milliwatts

A black body at 80 °C facing surroundings at 25 °C exchanges, at most,

\(\displaystyle q = \sigma\,(T_h^4 - T_c^4) \approx 5.67\times10^{-8}\,(353.15^4 - 298.15^4) \approx 434\ \text{W/m}^2 \approx 43\ \text{mW/cm}^2\)

Even a perfect Carnot converter could turn at most 15.6% of that into work, about 6.8 mW/cm². Over
the whole 25 cm² lid, that is under 0.2 W, against 700 W of heat. Far-field TPV and TR therefore
cannot matter for the GPU's power budget. Near-field coupling can raise the exchange by one or two
orders of magnitude, which brings the bound to watts. But it needs sub-micrometre gaps held over large
areas, and the surface it uses is the one the cooler needs. Radiative approaches are worth pursuing
for sensing and for the basic science, not as a power source at GPU temperatures.

### 7.2 A thermoelectric layer in the heat path recovers about 1–2%

A thermoelectric generator's best efficiency depends on its material's figure of merit \(ZT\):

\(\displaystyle \eta_{TEG} = \frac{T_h - T_c}{T_h}\cdot\frac{\sqrt{1+ZT}-1}{\sqrt{1+ZT}+T_c/T_h}\)

Place a TEG with \(ZT = 1\), typical of bismuth telluride, so that 30 K falls across it: hot face at
80 °C, cold face at 50 °C. The Carnot term is 8.5%, the material term 0.18, and the efficiency about
1.5%. With all 700 W passing through it, the TEG produces roughly 10 W.

Those 30 K must come from somewhere. Either the junction runs 30 K hotter, which costs reliability
and invites throttling, or the cooler holds the cold face 30 K lower, which costs fan, pump or
chiller power. The harvest is worth having only when that headroom is cheaper than about 1.5% of
the GPU's power. Where the cooler must run a refrigeration cycle to supply the headroom, the
thermodynamic minimum cost of that refrigeration is of the same order as the TEG's output. Real
chillers cost more. **The decisive measurement of the program is therefore the cooling cost of the
headroom, not the TEG's output.**

### 7.3 Where the numbers improve

The estimate points to three places where the idea is stronger.

- **Small, steady loads.** A few milliwatts to a few watts suits sensors, telemetry, fan and pump
  control, and power-management circuitry. It cannot help the core rails. Here the harvester's
  measuring role (§5) adds value on top of the energy.
- **Unused gradients.** Gradients outside the main heat path cost the cooler nothing: package edges,
  board regions near voltage regulators, and memory stacks that run at a different temperature from
  the die.
- **The coolant loop.** Warm-water liquid cooling gathers the heat of many GPUs into one fluid
  stream, outside any chip's thermal path. A converter on the loop can be large, serviced and
  optimised at one temperature, and it adds no junction penalty. It does compete with a strong
  alternative: using the heat as heat, for buildings or district heating, which delivers most of its
  energy rather than a few percent. A credible program compares against heat reuse, not only against
  doing nothing.

The program should therefore define its system boundary at several levels (die, package, board, rack
loop and facility) and report the net benefit at each.

## 8. Energy accounting

Let:

- \(P_g\) be the gross electrical power the harvester produces;
- \(P_c\) be the power the conversion and conditioning circuits consume;
- \(P_a\) be the extra cooling power that harvesting causes;
- \(P_s\) be any other extra system overhead.

The net recovered power is

\(\displaystyle P_{\text{net}} = P_g - P_c - P_a - P_s\)

For a GPU drawing \(P_{\text{GPU}}\), the effective external power becomes
\(P_{\text{eff}} = P_{\text{GPU}} - P_{\text{net}}\), and the recovery ratio is
\(R = P_{\text{net}} / P_{\text{GPU}} \times 100\%\).

A positive \(P_{\text{net}}\) means harvesting lowers the electricity the system needs, within the
stated boundary. A negative value means it costs more than it returns. That result is important too:
a good converter is not necessarily a good GPU energy-recovery system. Section 7.2 shows that
\(P_a\) is the term most likely to decide the sign. Every measurement states its boundary and uses
an identical computational workload.

## 9. Research program

The program grows in steps, and each step ends at a decision gate. Nobody needs to make a GPU or
open an expensive package in the early phases.

### Phase 1: a feasibility model

A Python simulator of thermal energy recovery. It takes GPU power, die, case and coolant
temperatures, thermal resistances, conversion efficiency and overheads. It reports the recoverable
energy, the net benefit, its sensitivity to temperature and cooling, and the three technologies side
by side, at each system boundary of §7.3.

**Gate:** continue to hardware only for the configurations the model shows with \(P_{\text{net}} >
0\) at a realistic operating point. Publish the rest as negative results.

### Phase 2: technology models

Detailed models of each candidate:

- **TEG:** gradient, Seebeck coefficient, electrical resistance, thermal conductivity, load matching
  and geometry.
- **TPV:** emitter spectrum, cell bandgap, spectral selectivity, optical coupling, gap and losses.
- **TR:** band structure, radiative and non-radiative recombination, temperature dependence and
  radiative exchange.

**Gate:** pick at most two device configurations for the bench.

### Phase 3: a bench proof of concept

A controlled heat source, without a GPU. Measure the hot and cold temperatures, open-circuit and
loaded voltage and current, electrical output, conversion efficiency and the added thermal resistance.

**Gate:** a reproducible measurement within a stated margin of the model.

### Phase 4: a real GPU, unmodified

A commercial GPU serves as a controlled heat and workload source. Its silicon and power connections
stay untouched, and the harvesters sit beside the package or on the coolant loop. Compare three
setups under identical workloads:

1. no harvester;
2. harvester installed and electrically unloaded;
3. harvester enabled.

Measure GPU power and temperature, cooling power, harvested output, performance and net recovery.
Setup 2 against setup 1 isolates the thermal penalty of the hardware. Setup 3 against setup 2
isolates the energy recovered.

**Gate:** a measured positive \(P_{\text{net}}\) at some boundary.

### Phase 5: closed-loop power management

A controller that drives auxiliary loads and self-powered sensors from recovered energy, judged on
power availability, thermal and electrical stability, control latency and storage behaviour.

### Phase 6: package integration

Only after a measured positive net benefit: thin-film harvesters, advanced and heterogeneous
packaging, thermal interface engineering, integrated power management, and co-design of cooling and
harvesting. This phase needs semiconductor fabrication and packaging partners.

## 10. Success criteria

| Criterion | Evidence required |
|---|---|
| Conversion | Measured electrical output |
| Net benefit | Positive \(P_{\text{net}}\) at a stated boundary |
| Thermal compatibility | No unacceptable rise in junction temperature |
| Cooling compatibility | No disproportionate cooling penalty |
| Electrical stability | Stable, regulated output |
| Computational integrity | No unacceptable loss of workload performance |
| Reproducibility | Documented conditions and repeatable measurements |

A negative result does not fail the project. If TPV proves impractical at GPU temperatures while
edge thermoelectrics show promise, that is a finding. If recovery pays only for sensors, or only at
the coolant loop, that defines a realistic application.

## 11. Beyond GPUs

The same questions apply to AI accelerators, HPC processors, data-centre server packages, network
processors, power electronics and edge hardware. The long-term aim is to make energy recovery a
standard question in electronic-package design, asked alongside cooling rather than after it.

## 12. Open questions

1. **Technology.** Which mechanism gives the highest net output under realistic GPU conditions?
2. **Materials.** Which semiconductors or heterostructures convert efficiently near 350 K?
3. **Integration.** Can a harvester sit in or near the package without raising thermal resistance?
4. **Gradients.** Which existing gradients can be used without taxing the cooler?
5. **Radiative coupling.** Can near-field TPV or TR reach useful power density at these temperatures?
6. **Loads.** Which loads gain most from recovered energy, and from self-powered sensing?
7. **Control.** Can a closed loop maximise net recovery while keeping thermal and electrical stability?
8. **Economics.** Do the added materials, packaging and manufacturing cost pay for the energy?
9. **Scale.** Does recovery grow more attractive at higher-power accelerators, at the rack loop, or
   neither?
10. **Heat reuse.** At what coolant temperature does converting heat to electricity beat using it as
    heat?

## 13. Open-source implementation

The program will start as a public, multidisciplinary repository, `self-powered-gpu`:

```text
self-powered-gpu/
├── README.md, LICENSE, CITATION.cff
├── docs/          proposal, architecture, thermodynamics, energy accounting, methodology
├── research/      thermophotovoltaic/, thermoelectric/, thermoradiative/, packaging/
├── simulation/    thermal_model.py, energy_recovery.py, conversion_models.py, power_controller.py
├── experiments/   test platform, measurement protocol, results/
├── hardware/      thermal fixture, power management
└── references/    bibliography
```

The repository keeps theoretical models, simulated results and measured results apart. Every
experimental claim carries its conditions and its data.

## 14. An invitation

This proposal is exploratory. It does not claim that a self-powered GPU exists, or that any
conversion technology is ready for a package. It names an opportunity and the measurements that
would settle it.

We invite semiconductor researchers, photovoltaic and thermoelectric specialists, materials
scientists, thermal engineers, GPU architects, power-electronics designers, university groups and
independent hardware builders. Contributions can be analysis, simulation, materials, device models,
experiment designs, measurements, or criticism. The comments below and the repository are both open.

## 15. Conclusion: from heat management to heat utilisation

Thermal management and energy recovery are different goals. The first removes unwanted heat. The
second asks whether some of it can do work.

The physics is unforgiving at chip temperatures. Far-field radiation yields milliwatts, and a
thermoelectric layer yields a percent or two at the cost of the cooler's headroom. That is exactly
why the question deserves careful measurement rather than enthusiasm. The idea has real footholds:
self-powered sensing, unused gradients, and the warm coolant loops that AI data centres are
building now.

A GPU will never run on its own heat. The question is whether the next generation of computing
hardware can recover enough of its wasted energy to make a measurable difference.

**Perhaps the next step in GPU architecture is not only to compute more with less electricity, but
to recover some of the electricity already spent.**

---

## References

### Thermophotovoltaic conversion

1. Burger, T., … Lenert, A. (2022). Semitransparent thermophotovoltaics for efficient utilization of
   moderate temperature thermal radiation. *Proceedings of the National Academy of Sciences* 119(48),
   e2215977119. <https://doi.org/10.1073/pnas.2215977119>
2. LaPotin, A., … Henry, A. (2022). Thermophotovoltaic efficiency of 40%. *Nature* 604, 287–291.
   <https://doi.org/10.1038/s41586-022-04473-y>
3. Chen, S., … Shuai, Y. (2024). A review on current development of thermophotovoltaic technology in
   heat recovery. *International Journal of Extreme Manufacturing* 6(2), 022009.
   <https://doi.org/10.1088/2631-7990/ad1dca>
4. Mittapally, R., … Meyhofer, E. (2023). Near-field thermophotovoltaic energy conversion: progress
   and opportunities. *Physical Review Applied* 19, 037002.
   <https://doi.org/10.1103/PhysRevApplied.19.037002>
5. Habibi, M., … Cui, L. (2025). Enhanced power density in zero-vacuum-gap thermophotovoltaic
   devices. *Energy & Environmental Science* 18, 1514–1523. <https://doi.org/10.1039/D4EE04604H>

### Thermoradiative and thermophotonic conversion

6. Nielsen, M. P., … Ekins-Daukes, N. J. (2024). Semiconductor thermoradiative power conversion.
   *Nature Photonics* 18, 1137–1146. <https://doi.org/10.1038/s41566-024-01537-5>
7. Sadi, T., … Oksanen, J. (2022). Prospects and requirements for thermophotonic waste heat energy
   harvesting. *Solar Energy Materials and Solar Cells* 239, 111635.
   <https://doi.org/10.1016/j.solmat.2022.111635>

### Thermal recovery at the device

8. Yu, F., … Li, D. (2026). Thermal recovery system for high-power devices. *Advanced Energy
   Materials* 16(25), e71052. <https://doi.org/10.1002/aenm.71052> It combines thermoelectric and
   hydrovoltaic modules for simultaneous cooling and power generation, demonstrated on AlGaN
   deep-ultraviolet LEDs, not GPUs.

### Measurement and fundamentals

9. Yi, F., … Zhao, C. Y. (2025). Towards-standardization energy conversion efficiency measuring
   system for thermophotovoltaic cells. *Applied Energy* 377, 124657.
   <https://doi.org/10.1016/j.apenergy.2024.124657>
10. Tervo, E., Bagherisereshki, E. and Zhang, Z. (2018). Near-field radiative thermoelectric energy
    converters: a review. *Frontiers in Energy* 12(1), 5–21.
    <https://doi.org/10.1007/s11708-017-0517-z>

---

**Research disclaimer.** This page presents an open research hypothesis and a proposed experimental
program. It claims no demonstrated GPU energy recovery, no commercial readiness and no
self-sustaining computing device. The estimates in §7 are first-order bounds, not predictions, and
every performance expectation needs experimental validation.
