
# ✅ Cursor Task: Implement Upscale History in Trial Detail Page

## 📍 File: `TrialDetail.tsx`

---

## 🎯 Objective:
Implement a clear and interactive UI section to display and manage **UpscaleRuns** for a given fermentation trial. This allows the user to review past upscale results and initiate the next stage when eligible.

---

## 🧩 Components & Layout

```tsx
<TrialInfo trial={trial} />

<UpscaleHistoryTable trialId={trial.id} />

<Button onClick={startNextUpscale}>
  Start Next Upscale
</Button>
```

---

## 🛠️ Tasks to Complete

### 1. Create or Update the Following Components:

#### ✅ `TrialInfo`
- Displays basic trial metadata: Juice Type, Yeast Strain, SG, ABV, Status

#### ✅ `UpscaleHistoryTable`
- Table format showing:
  - Stage (Test 3–6)
  - Volume (1L, 5L, 30L, 100L)
  - Yield
  - ABV
  - Compound Test (OK, Fail, Pending)
- Pulls data from `/trials/{id}/upscales`

#### ✅ `useUpscaleActions` (Hook or Service)
- Handles call to `POST /trials/{id}/upscales` to create the next stage
- Handles `PATCH /upscales/{id}` for result updates

---

### 2. Button Behavior

- Button: “Start Next Upscale”
- Shown only when trial status = `"Fermenting"` and previous upscale is complete
- Triggers backend creation of new `UpscaleRun` linked to the trial
- Add success confirmation and toast

---

## 💡 UX Notes

- Consider a visual ladder-style layout next to the table
- Use icon indicators for compound test results (✅ ⚠️ ❌)
- Include modal confirmation for starting new upscale

---

## 📦 Backend Endpoint Requirements

- `GET /trials/:id/upscales`
- `POST /trials/:id/upscales`
- `PATCH /upscales/:id`
- `POST /upscales/:id/complete`

---

## 🧠 Bonus

- Allow inline editing of compound test results if status = pending
- Add progress indicator to show stage advancement from Test 3 → 6

---

**Task Owner:** Cursor (frontend + API)  
**Spec Based On:** `xoohoox_upscale_tracking_spec.md` + wireframe visual  
**Date:** April 12, 2025
