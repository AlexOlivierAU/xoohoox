# 🧩 XooHooX UI → Backend Mapping Guide
**Date:** 2025-04-23  
**Purpose:** Connect UI screens to backend routes, database tables, and expected fields. Built to support 80+ mobile UI views across Grower, Lab, Admin, and R&D roles.

---

## ✅ Format Explanation
Each entry follows:
- `📱 Screen:` Name in the UI (Uizard)
- `🔁 Type:` Form / Dashboard / Reference
- `🔗 Endpoint:` Suggested API route
- `🗃️ Table:` Suggested DB table
- `🧬 Key Fields:` Critical fields needed

---

## 🍇 Core Modules (Grower / Farm View)

### 1. **Produce Batch Dispatch**
- 📱 Screen: "Dispatch Produce"
- 🔁 Type: Form
- 🔗 Endpoint: `POST /api/batch/dispatch`
- 🗃️ Table: `batches`
- 🧬 Key Fields: `grower_id`, `produce_type`, `varietal`, `dispatch_date`, `quantity_kg`, `batch_id`

### 2. **Juicing Input**
- 📱 Screen: "Juicing Input Form"
- 🔁 Type: Form
- 🔗 Endpoint: `POST /api/juicing/log`
- 🗃️ Table: `juicing_logs`
- 🧬 Key Fields: `batch_id`, `juice_type`, `juicing_date`, `yield_liters`, `sediment_notes`

### 3. **Farm Crop Data**
- 📱 Screen: "Farm Details"
- 🔁 Type: Form
- 🔗 Endpoint: `POST /api/farm/update`
- 🗃️ Table: `farms`
- 🧬 Key Fields: `farm_id`, `field_name`, `crop_type`, `soil_notes`, `weather_notes`, `season`

---

## 🧪 Lab Process Modules

### 4. **Fermentation Log**
- 📱 Screen: "Fermentation Kinetics Log"
- 🔁 Type: Form
- 🔗 Endpoint: `POST /api/fermentation/log`
- 🗃️ Table: `fermentation_logs`
- 🧬 Key Fields: `batch_id`, `day_number`, `temperature`, `ph_level`, `sg_reading`, `notes`

### 5. **Evaluation Entry**
- 📱 Screen: "Evaluation Form"
- 🔁 Type: Form
- 🔗 Endpoint: `POST /api/evaluation/submit`
- 🗃️ Table: `evaluations`
- 🧬 Key Fields: `sample_id`, `score_aroma`, `score_color`, `score_taste`, `evaluator_name`, `comments`

---

## 🧫 Yeast R&D Suite

### 6. **Yeast Library Manager**
- 📱 Screen: "Add/Edit Yeast Strain"
- 🔁 Type: Form
- 🔗 Endpoint: `POST /api/yeast/add`
- 🗃️ Table: `yeast_strains`
- 🧬 Key Fields: `strain_name`, `genetic_notes`, `function_tags`, `origin`, `last_tested_batch`

### 7. **Strain Performance Comparison**
- 📱 Screen: "Compare Strains"
- 🔁 Type: Dashboard
- 🔗 Endpoint: `GET /api/yeast/compare`
- 🗃️ Table(s): `yeast_strains`, `evaluations`, `fermentation_logs`
- 🧬 Key Fields: `strain_id`, `batch_ids`, `avg_yield`, `avg_score`, `tags`

---

## 💼 Admin + Reporting

### 8. **User Role Manager**
- 📱 Screen: "User Management"
- 🔁 Type: Dashboard + Form
- 🔗 Endpoint: `GET /api/users`, `POST /api/users/update`
- 🗃️ Table: `users`
- 🧬 Key Fields: `user_id`, `role`, `email`, `assigned_batches`

### 9. **Batch Report Generator**
- 📱 Screen: "Generate Batch PDF"
- 🔁 Type: Export
- 🔗 Endpoint: `GET /api/report/batch/:batch_id`
- 🗃️ Sources: `batches`, `juicing_logs`, `evaluations`, `yeast_strains`
- 🧬 Key Fields: Full batch traceability

---

## 📦 Coming Soon (To Sprint)

- Grant Tracker (R&D export)
- Invoice Generator
- Substrate Log
- My Tasks view

---

Let me know when you're ready for the next export or need database schema examples. This file is now ready to download and share with your devs.
