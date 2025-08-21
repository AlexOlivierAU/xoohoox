
# 🔼 Cursor Spec: Upscale Tracking for Fermentation Trials (XooHooX)

## 🎯 Purpose:
Enable each fermentation trial to be upscaled multiple times across standard volume stages (Test 3–6). These upscales must be tracked as independent runs but linked directly to the originating trial.

---

## ✅ Functional Requirements:

### 1. Data Model

#### New Model: `UpscaleRun`
Each `FermentationTrial` can have many `UpscaleRun` records.

**Fields:**
- `trial_id` (foreign key to FermentationTrial)
- `upscale_id` (e.g. `U-042-03-5L`)
- `stage` (e.g., Test 4, Test 5, Test 6)
- `volume` (e.g., 5L, 30L, 100L)
- `yield` (e.g., 480mL)
- `abv_result`
- `compound_summary` (optional: methanol, esters, vanillin, etc.)
- `status` (`pending`, `complete`, `failed`)
- `timestamp`

---

## 2. UI Requirements

### A. Upscale History Table (in Trial Detail View)

| Stage   | Volume | Date       | Yield   | ABV  | Compound OK? |
|---------|--------|------------|---------|------|---------------|
| Test 4  | 5 L    | 2025-04-02 | 480 mL  | 8.0% | ✅             |
| Test 5  | 30 L   | 2025-04-05 | 2.9 L   | 8.2% | ✅             |
| Test 6  | 100 L  | —          | —       | —    | 🔄 Pending     |

### B. UI Actions
- [Start Next Upscale]
- [Record Yield]
- [Input Compound Results]
- [Mark as Complete]

---

## 3. Logic & Validation Rules

- Upscale must match allowed test stages (Test 3–6)
- Trial must meet ABV or completion criteria before upscaling
- Yield and compound results required for stage completion
- Only one active upscale per trial at a time

---

## 4. API Requirements

- `GET /trials/{id}/upscales` — view past upscales
- `POST /trials/{id}/upscales` — create new upscale run
- `PATCH /upscales/{id}` — update yield/results
- `POST /upscales/{id}/complete` — finalize stage

---

## 📌 Dev Notes

- Upscale IDs should follow pattern: `U-{batch}-{trial_id}-{volume}` (e.g., `U-042-03-30L`)
- Table should display in trial detail view
- Consider color badges for status indicators (Pending, OK, Fail)

