# W04 stage 2 — printer comparison

Read 2026-11-10 for the [workshop road](workshop-road.md). **No printer is selected or
purchased; the pick below is a recommendation for Bill to accept or change, and he places any
order himself.** Prices are the US stores' own pages on that date, in US dollars, printer only,
before tax and shipping. Every one was a sale price, so each is checked again at checkout.

## What was read, and how

"Store" means the maker's own US store page, opened that day. "Reported" means a review or a
search summary, not opened first-hand.

| Machine | Price | Regular | Frame | Build volume, mm | Chamber | Nozzle | Evidence |
|---|---|---|---|---|---|---|---|
| Bambu Lab A1 | $259 | $299 | Open | 256 class | None | Not read | Store |
| Elegoo Centauri Carbon 2 | $319 | $359 | Enclosed | 256 × 256 × 256 | Heating not read | 350 °C; hardened, reported | Store |
| Bambu Lab P1S | $349 | $399 | Enclosed | 256 class | Passive, reported | Not read | Store, price only |
| **Bambu Lab P2S** | **$449** | $549 | Enclosed | 256 class | Passive, about 60 °C, reported | Hardened, 300 °C | Store |
| QIDI Q2 | $449 | $499 | Enclosed | 270 × 270 × 256 | 65 °C, actively heated | 370 °C | Store; in stock |
| Bambu Lab X2D | $589 | $649 | Enclosed, two nozzles | 256 class | 65 °C, actively heated, reported | Hardened, 300 °C | Store |
| Prusa CORE One+ kit | $925 | from $999, reported | Enclosed, self-assembly | 250 × 220 × 270 | Up to 55 °C | Brass 0.4 mm, 290 °C | Store; in stock |
| Prusa CORE One+ assembled | $1,202.78 | from $1,299 | Enclosed | 250 × 220 × 270 | Up to 55 °C | Brass 0.4 mm, 290 °C | Store |

Not carried further: the Creality K2 Pro (no current store price found; $599 reported in
September, on back-order), Bambu's larger A2L and H-series (more bed than Mack needs, from $439
open-frame and from $1,049 enclosed), and the A1 mini (180 mm bed, too small for the dock).

Running without a vendor cloud:

- **Prusa:** the store page says the printer is set up and run offline, from a USB drive or the
  local network, with no cloud dependency.
- **Bambu Lab:** cloud is the default. A "LAN Only" setting with "Developer Mode" is reported to
  run the printer without the cloud, with files and firmware moved on a card or over the local
  network. Reported from Bambu's wiki and third-party guides, not tried.
- **Elegoo and QIDI:** local network and USB printing are listed; whether an account is ever
  required was not read.

## Against what Mack needs

The needs are the ones in the [workshop road](workshop-road.md): small stiff hinge plates around
an 18 g servo, a base and later a dock within a 250 mm bed, PLA then PETG then TPU, and room to
move to fibre-filled or higher-temperature filament if thin plates flex.

| Machine | First-stage parts (PLA, PETG, TPU) | Fibre-filled and hot materials | Runs offline | Effort to own |
|---|---|---|---|---|
| A1 | Yes | No enclosure; fibre-filled PLA or PETG only with a hardened nozzle added | With the LAN setting | Lowest |
| Centauri Carbon 2 | Yes | Enclosed, hot nozzle; chamber heat unknown | Listed | Not assessed |
| P2S | Yes | Enclosed with a hardened nozzle; enough for small nylon and ASA parts | With the LAN setting | Low |
| Q2 | Yes | The most heat at this price | Listed | Not assessed |
| X2D | Yes | Heated chamber; second nozzle for a separate support material | With the LAN setting | Low |
| CORE One+ | Yes | Enclosed; a hardened nozzle is a separate purchase | By design | Kit is a build of its own |

## The pick

**Bambu Lab P2S, printer only, $449.** It is enclosed, ships with a hardened nozzle, has the
bed for every part including the dock, and asks the least of a first-time owner. Mack's stiff
parts are small, and small parts in nylon or ASA do not need an actively heated chamber. The
multi-colour unit is not needed: ivory housings and black feet print as separate parts.

The honest cost: it is cloud-first until the LAN setting is turned on, and that setting is
reported, not tried. Mack's part files are already public in this repository, so the exposure
is small, but the setting should be the first thing changed.

Alternatives, each for one reason:

- **Bambu Lab X2D, $589**, if larger ASA or polycarbonate parts or a dedicated support material
  are wanted from the start. Its second nozzle is fed differently from the first; reviews call
  that its compromise.
- **QIDI Q2, $449**, for the hottest chamber and nozzle at the P2S's price. Ownership effort was
  not assessed here, which is the only reason it is not the pick.
- **Prusa CORE One+ kit, $925**, if offline-by-design and open firmware outweigh twice the price
  and a day of assembly. Add a hardened nozzle for fibre-filled filament.
- **Bambu Lab A1, $259**, if the budget stays near the October allowance. It prints every
  first-stage part and none of the hot materials.

This is a judgment from store pages and reported reviews. No machine was tested, and no part of
Mack has been load-checked, so the case for fibre-filled material is still a likelihood.

## With the order

Filament for the first prints: PLA for fit checks, PETG for brackets, TPU for feet. A filament
dryer earns its place once TPU or nylon is in use. None of these were priced.

## Sources

Store pages read 2026-11-10: [Bambu Lab US printers](https://us.store.bambulab.com/collections/3d-printer),
[Elegoo Centauri Carbon 2](https://us.elegoo.com/products/centauri-carbon-2),
[QIDI Q2](https://us.qidi3d.com/products/qidi-q2),
[Prusa CORE One+ kit](https://www.prusa3d.com/product/prusa-core-one-kit/).

Reported, not opened first-hand: [X2D launch coverage](https://all3dp.com/4/bambu-lab-x2d/),
[P2S against X2D](https://planet3dp.com/bambu-lab-p2s-vs-x2d/),
[P2S against P1S](https://makers101.com/bambulab-p2s-vs-p1s/),
[Bambu LAN and developer mode guide](https://help.simplyprint.io/en/article/bambu-lab-lan-only-mode-and-developer-mode-how-to-enable-xa0hch/),
[Bambu third-party integration wiki](https://wiki.bambulab.com/en/software/third-party-integration),
[Centauri Carbon 2 review](https://www.tomshardware.com/3d-printing/elegoo-centauri-carbon-2-review),
[K2 Pro review](https://www.jcprintfarm.com/blogs/3d-printing-tech/creality-k2-pro-review).
