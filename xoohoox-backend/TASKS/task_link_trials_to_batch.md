
# 🔗 Cursor Task: Link Fermentation Trials to Batch UI (XooHooX)

## 🎯 Objective:
Enable users to access fermentation trials and upscale tracking directly from the batch UI.

---

## 🖥️ Current State:
- The Dashboard shows Active Batches correctly.
- Users can click “View Details” for each batch.
- However, there is **no way to view or access fermentation trials** for a given batch.

---

## ✅ Tasks to Complete

### 1. Add Trial Access to Batch Details Page

- On the page rendered by clicking “View Details” for a batch:
  - Add a **new tab** or **section** titled **"Trials"**
  - Display a **table or list of fermentation trials** for that batch

### 2. Display Trial Metadata

For each trial, show:

| Trial ID | Yeast | Juice Type | ABV | Status | Actions |
|----------|-------|------------|-----|--------|---------|
| T-042-01 | Y-A   | JP1        | 7.8% | Fermenting | [ View Trial ] |
| T-042-02 | Y-B   | JP1        | 8.5% | Vinegar | [ View Trial ] |

### 3. Add “View Trial” Button

- Button should link to the **Trial Detail page**
- Page should include:
  - `TrialInfo`
  - `UpscaleHistoryTable`
  - `Start Next Upscale` button

---

## 📦 Optional Enhancements

- Allow sorting/filtering of trials by status or juice variant
- Add “Create New Trial” action from within the batch
- Include quick status icons (✅, ⚠️, ❌) for compound test results if available

---

## 🧠 Implementation Tips

- Use route structure like:
  ```
  /batches/:batchId/trials
  /trials/:trialId
  ```
- Consider adding a `trials` sidebar link if you want global trial management

---

**Task Owner:** Cursor (frontend + API route links)  
**Source:** Alex + Zara.X system trace  
**Date:** April 12, 2025
