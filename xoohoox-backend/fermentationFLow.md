XooHooX Fermentation & Distillation Flowchart (Unified)

Phase 1: Raw Material & Chemistry Prep

Input: Fruit (e.g., Lemons) → Cold Pressed Juice

Target Batch: 100L

Initial Readings:

Raw pH: 1.8

SG: 1.03

Adjustments:

Add 11–12 kg Sodium Bicarbonate (endo thermic reaction)

Target SG > 1.07, pH > 5

Allow 1 hour for reaction

Note: Work in small batches, scale up

Phase 2: Heat Activation & Nutrient Prep

Heat batch to 30–32°C, allow to rest 24 hrs

Prepare nutrient mix (4–5 g/L) + Yeast (5 g/L)

Rest 15 mins

Pitch into batch at >30°C

Phase 3: Fermentation

Monitor Fermentation Kinetics (daily readings)

Target ABV: 7–8%

Typical yield from 100L ferment: ~15L distillate

Test 3: 1L Ferment → Yields 100 mL distillate

Phase 4: Distillation Ladder ("Upscale")

Test

Volume

Process

Yield

3

1L

D1 Pot Distil

~100 mL

4

5L

D1 Pot Distil

350–500 mL

5

30L

D1 Pot Distil

2–3 L

6

100L

D1 Pot Distil

~15 L

7

—

D2 Reflux/Infuse

Optional

Test after each distillation for: ABV, Methanol, Esters, VOCs

Optionally retain 1L raw and steep samples for archival

Notes:

Fermentation is influenced by SG, pH, and Yeast strain

Distillate quality improves with each upscale stage

Still waste should be analyzed (Test 8) for environmental reporting

process:
  name: XooHooX Fermentation & Distillation
  stages:
    - name: Chemistry Prep
      input: "Cold pressed fruit juice"
      adjustments:
        - sodium_bicarb: 11-12kg
        - target_pH: ">5"
        - target_SG: ">1.07"
      notes:
        - reaction: endothermic
        - rest: 1h

    - name: Heat Activation
      steps:
        - heat_to: "30-32C"
        - rest: "24h"

    - name: Nutrient & Yeast
      nutrient: "4-5g/L"
      yeast: "Mauri 5g/L"
      rest: "15m"
      pitch_conditions:
        temp: ">30C"
        pH: ">5"
        SG: ">1.07"

    - name: Fermentation
      monitoring: "daily kinetics"
      min_abv: "7%"
      full_batch: "100L"
      expected_yield: "15L distillate"

    - name: Distillation Ladder
      steps:
        - test_3:
            volume: "1L"
            method: "D1 Pot Still"
            yield: "~100mL"
        - test_4:
            volume: "5L"
            yield: "350-500mL"
        - test_5:
            volume: "30L"
            yield: "2-3L"
        - test_6:
            volume: "100L"
            yield: "~15L"
        - test_7:
            method: "D2 Reflux/Infuse"
            optional: true

    - name: Quality Tests
      metrics:
        - abv
        - methanol
        - esters
        - fusel_oils
        - VOCs