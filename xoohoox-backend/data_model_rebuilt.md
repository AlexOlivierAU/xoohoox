# XooHooX Catalyst Data Model (Reloaded)

| Table | Field Count | Fields |
|-------|-------------|--------|
| `BatchDispatch` | 18 | batch_id, grower, produce, varietal, quantity, containment_type, total_containers, grade, damaged, ripeness, pick_date, pack_date, transport_company, transport_type, pickup_date, dropoff_location, market_agent, delivery_date |
| `BatchTracking` | 16 | grower, grower_id, fruit, fruit_id, varietal, varietal_id, batch_id, delivery_date, juicing_date, juicing_method, sample_ids, ferment_date, ferment_formula, ferment_sample_ids, distil_date, distil_sample_ids |
| `DistillationResults` | 10 | grower, produce, varietal, batch_id, distill_stage, total_collected_ml, temp_peak_c, collection_start, collection_end, distillation_notes |
| `DistillationResults` | 15 | batch_id, date, distiller_name, fruit_type, varietal, wash_volume_l, distillate_volume_ml, heads_volume_ml, hearts_volume_ml, tails_volume_ml, peak_temp_c, abv_collected_percent, clarity_notes, aroma_notes, final_use_class |
| `FailureReports` | 8 | batch_id, date_reported, process_stage, failure_type, cause, action_taken, resolved, evaluator_notes |
| `FermentationKinetics` | 7 | batch_id, start_date, initial_brix, initial_ph, initial_temp, yeast_strain, notes |
| `FermentationPlan` | 11 | batch_id, grower, produce, varietal, start_date, brix_target, ph_target, temp_target_c, yeast_strain, substrate_notes, hypothesis_summary |
| `FermentationResults` | 11 | batch_id, evaluator_name, evaluation_date, final_abv, final_ph, clarity_score, color_notes, smell_notes, taste_notes, fermentation_result, additional_notes |
| `JuicingInputLog` | 11 | batch_id, grower, produce, varietal, weight_before_juicing, juice_volume, juice_clarity, separation_observed, method_used, date_collected, notes |
| `JuicingResults` | 7 | batch_id, amount_frozen_kg, defrost_start_time, defrost_finish_time, defrost_duration, clarified_volume_ml, clarified_yield_ratio |
| `LiquefactionMethod` | 7 | batch_id, liquefier_product, method_steps, timing_notes, produce_constraints, required_conditions, testing_notes |
| `LiquefactionPlan` | 9 | batch_id, grower, produce, varietal, target_yield_ml, substrate_type, liquefier_type, hypothesis_notes, start_date |
| `LiquefactionRuns` | 9 | grower, produce, varietal, batch_id, test_stage, extraction_point, extraction_start_date, extraction_yield_ml, extraction_notes |
| `ProducePrelimEval` | 14 | batch_id, grower, produce, varietal, harvest_date, collection_method, ripeness, visible_damage, contamination_notes, color_notes, odor_notes, firmness_notes, overall_score, evaluator_name |
| `ProductEvaluation` | 8 | batch_id, clarity_score, acidity_ph, aroma_notes, flavour_notes, viscosity_notes, classification_result, evaluator_name |
| `SensoryFeedback` | 10 | batch_id, panelist_type, date, clarity_score, aroma_notes, taste_notes, mouthfeel_notes, rating, suggested_use, evaluator_name |
| `VinegarKinetics` | 12 | grower, produce, varietal, batch_id, test_stage, substrate_type, start_date, acetic_acid_target, ph_initial, ph_final, vinegar_yield_ml, vinegar_notes |