# W04 stages 0 and 1 — the small first order, priced

Read 2026-11-10 for the [workshop road](workshop-road.md), on Bill's "Yes, price it". **Nothing
is ordered; Bill places any order himself.** Prices are each store's own page on that date, in
US dollars, before tax and shipping.

## The order

| Item | What it is for | Store | Price | Stock as shown |
|---|---|---|---|---|
| OpenRB-150 Starter Kit | One XL330-M288-T servo and the small board that connects it to the Mac over USB-C | [ROBOTIS US](https://robotis.us/products/openrb-150-starter-kit) | $52.79 | Add to cart, no lead-time notice |
| AWS SC-2KG scale, 2000 g × 0.1 g | Weighing the clock, the servo and every printed part | [American Weigh Scales](https://awscales.com/sc-2kg-precision-digital-pocket-scale-2kg-x-0-1g/) | $25.99 | In stock |
| iGaging Absolute Origin 6 in caliper, 100-700-06 | Measuring the clock shell and the servo; 0.01 mm resolution, 0.02 mm stated accuracy | [Penn Tool Co.](https://www.penntoolco.com/igaging-6-ip54-digital-caliper-absolute-origin-100-700-06/) | $83.95 | In stock per the page's data |
| **Total** | | | **$162.73** | |

Without the calipers, if a pair is already on hand: **$78.78**.

A USB-C data cable is needed and is not in the kit. The scale's batteries are included; a
calibration weight is not.

## Two changes from what was asked, and why

**One servo now, not two.** The second servo alone is $27.49, and the store marks it "lead time
required, end of November". One servo is enough for this stage: it replaces the recalled
output-axis offset with a measured one, gives a real mass and a real horn, and can be run. The
second matters for the hip-pair fit check, which also needs printed parts. It joins the later
parts order unless Bill wants it now.

**The board instead of the U2D2 adapter.** The U2D2 ($36.92) does not power a servo. It needs
the power hub board ($21.85) and a separate 5 V supply ($14.95 for a 5 V 4 A unit), $73.72 in
all, and the supply's plug does not fit the hub's jack without a further adapter. The
OpenRB-150 comes loaded with the same USB bridge and runs a 5 V servo from the USB-C cable
alone. The maker limits that USB power to 500 mA and says it is not for loaded motion, which is
enough to read, measure and move a bare servo. Load tests take 5 V on the board's screw
terminal, from the bench supply in stage 3. The board is also a candidate for the local motion
controller in [parts.csv](parts.csv); buying it does not select it.

**Do not buy the "DYNAMIXEL Starter Set".** Its supply is 12 V. This servo's input is 5 V, 6 V
at most.

## What the store page settles about the servo

Read from the maker's US store page: 20 × 34 × 26 mm, 18 g, 5 V input (3.7 to 6.0 V), stall
torque 0.52 N·m at 1.47 A, 103 rpm with no load, 4,096 steps per turn, one 180 mm cable and six
M2 × 6 bolts in the box. The output-axis offset in the
[leg packaging study](joints/leg-packaging.md) is still RECALLED; the calipers and this servo
replace it with a measurement, with or without the maker's drawing. The servo remains a size
and mass benchmark, not a selected motor.

## On arrival

1. Weigh the servo and measure its case, bosses and output-axis position; record them and
   correct the leg model's parameter files.
2. Measure and weigh the clock for [measurements.csv](measurements.csv) (G1 intake).
3. Connect the board and read the servo's position. The maker's servo tool is a download and
   waits for Bill's word.

## Sources

Store pages read 2026-11-10: [OpenRB-150 Starter Kit](https://robotis.us/products/openrb-150-starter-kit),
[XL330-M288-T](https://robotis.us/products/dynamixel-xl330-m288-t),
[U2D2](https://robotis.us/products/u2d2),
[U2D2 Power Hub Board Set](https://robotis.us/products/u2d2-power-hub-board-set),
[AWS SC-2KG](https://awscales.com/sc-2kg-precision-digital-pocket-scale-2kg-x-0-1g/),
[iGaging 100-700-06](https://www.penntoolco.com/igaging-6-ip54-digital-caliper-absolute-origin-100-700-06/),
[5 V 4 A supply](https://www.adafruit.com/product/1466).
Maker's manuals read the same day: [OpenRB-150](https://emanual.robotis.com/docs/en/parts/controller/openrb-150/),
[U2D2 Power Hub](https://emanual.robotis.com/docs/en/parts/interface/u2d2_power_hub/).
A Mitutoyo 500-196-30 caliper was reported at about $166 and not opened first-hand.
