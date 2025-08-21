
# 🧪 Cursor Spec: Batch-to-Trial Fermentation Tracking (XooHooX)

## 🎯 Purpose:
Allow a single fruit batch (e.g., 100L Lemon) to be split into **multiple fermentation trials**, each using different conditions like yeast strain, juice type (JP1–JP5), or nutrient combos.

---

## ✅ Functional Requirements:

### 1. Data Model Relationships
- `Batch` has many `FermentationTrial` entries
- Each `FermentationTrial` must track:
  - `trial_id` (e.g., `T-042-03`)
  - `yeast_strain`
  - `juice_variant` (JP1–JP5)
  - `initial_volume`
  - `SG`, `pH`, `BRIX`
  - `ABV` (over time)
  - `path_taken` (`vinegar`, `distillation`, `archived`)
  - `daily_readings[]`
  - `upscale_history[]`
  - `compound_results`

---

## 2. UI Requirements

### A. Batch Overview
- Show core fruit batch info (type, date, volume, etc.)
- Show total trials created (e.g., “16 Trials active”)

### B. Fermentation Trial Table

| Trial ID | Juice Type | Yeast | SG | ABV | Path | Status |
|----------|------------|-------|----|-----|------|--------|
| T-042-01 | JP1        | Y-A   | 1.070 | 7.3% | Distill | Fermenting |
| T-042-02 | JP1        | Y-B   | 1.072 | 8.5% | Vinegar | Vinegar Path |
| T-042-03 | JP2        | Y-C   | 1.060 | 6.9% | — | Awaiting |

- Click a row → open trial detail view

### C. Trial Detail Page
- Shows:
  - Full trial info
  - Daily metrics (table or chart)
  - Upscale ladder (Test 3 → Test 6)
  - Compound test summary
  - Sample retention
- Actions:
  - Record Daily Metrics
  - Start Upscale
  - Branch to Vinegar

---

## 3. Logic & Validation Rules
- Trials inherit parent batch chemistry
- ABV > 8% triggers branching prompt
- Trials are independently upscaled and tracked
- Trial outcomes feed into `Stage2Results`

---

## 4. API Endpoints
- `GET /batches/{id}/trials`
- `POST /trials`
- `PATCH /trials/{id}`
- `POST /trials/{id}/readings`
- `POST /trials/{id}/branch`
- `POST /trials/{id}/upscale`

---

## 📌 Dev Notes
- Use readable `trial_id`s like `T-042-01`
- UI must clearly show path taken
- Table and cards should be reusable
