# Audit of candidates_v3

No bills removed: 200 in, 200 out, same IDs and order. `coded_lean` renamed to `lean` on all 200. 172 bills changed (171 text, 9 lean, 8 of them both); 28 unchanged.

Tags: **A** sourced or predicted claim, **R** real-bill similarity, **L** loaded language, **B** lean balance, **E** lean label, **M** mirror pair, **F** out of date against current law.

Drafting rule for A: removed attributions, hedges and behavioral forecasts. Kept proposal terms, the number of people covered, and plain budget figures ("costing about $X"). Tradeoffs are restated as who pays, who loses a rule, or what is given up.

Real-bill matches, sponsor history and current-law points are from memory, with no web check. New invented figures appear in econ_rule_expiry, ss_housing_time_limit, imm_asylum_wait_abroad, cj_juvenile_adult_prosecution, env_ev_fee and gun_wait_require.

## Lean changes

Total moved: left 80 to 76, right 80 to 75, mixed 40 to 49.

| Bill | Change | Reason |
|---|---|---|
| imm_visa_job_change | left to mixed | Backed by both business-minded and worker-minded members. Author flag. |
| tech_platform_self_preference | left to mixed | The best-known version had sponsors from both parties. Author flag. |
| env_review_time_limit | right to mixed | Permitting limits draw support from both parties. Author flag. |
| ss_disability_asset_limit | left to mixed | Well-known version had sponsors from both parties. |
| cj_record_sealing | left to mixed | Well-known version had sponsors from both parties. |
| tech_contractor_china_gear | right to mixed | China procurement limits pass with both parties. |
| intl_china_investment | right to mixed | Outbound investment limits have sponsors from both parties; matches intl_taiwan_military_aid. |
| tech_drone_waivers | right to mixed | Pushed under both parties; no clear party owner. |
| edu_test_growth_funding | right to mixed | Test-based funding was backed by reformers in both parties and opposed by some on each side. |

Author flags kept: `tech_adult_site_id` stays right (federal bills mostly from that side, though state votes crossed party lines). `ss_foster_care_age` stays mixed (foster care is cross-party; the work condition cuts against a clean left label).

## Mirror pairs

21 links kept, 0 removed, 5 pairs revised into true opposites. All 21 link a left bill to a right bill.

| Pair | Revision |
|---|---|
| imm_status_bar / imm_status_path | Both now cover the same group: people here without authorization over 10 years. |
| cj_drug_min_raise / cj_drug_min_end | Both now cover drug trafficking. Before: fentanyl trafficking only versus all drug offenses. |
| env_ev_fee / env_ev_credit | Rewritten as a barred credit plus fee versus a new credit, each stating the other's term. |
| soc_sports_inclusion / soc_sports_restrict | Both now cover girls' teams. Before: all transgender students versus girls only. |
| gun_private_check_require / gun_private_check_bar | Scope matched: dropped the single-state limit from the bar. |

## Could not fix without changing the policy

The specifics or structure were changed where noted in the table below, but the idea itself remains recognizable:

- imm_child_arrivals_residence: any relief for people brought as children recalls the same famous bills.
- soc_permanent_daylight: the policy is the bill; reworded only.
- gun_suppressor_registration: deregistration is the core of the famous bill.
- hc_medicaid_work_hours: rule now differs in age, hours and checks, but it is still a Medicaid work rule, and one is already law.
- gov_major_rule_approval: congressional approval of major rules is the famous bill's whole mechanism.
- gov_dc_statehood: admission terms are fixed by the idea.
- gov_proof_citizenship: restructured around a records match, still recalls the famous bill.
- edu_scholarship_credit: amount changed, structure unchanged.

## Flagged, left as is

| Bill | Issue |
|---|---|
| soc_abortion_week_14 | Close to a well-known 15-week bill with the same exceptions. The week number is in the ID, so left alone. |
| soc_abortion_week_20 | Mirror thresholds differ (14 versus 20). Opposed in direction and cannot both stand, but not symmetric. |
| env_carbon_fee, env_carbon_fee_bar | Budget figures kept; common idea. |
| intl_ally_troop_spending | Right label is debatable: mainstream hawks on that side would oppose it. |
| tax_child_credit_refund | "Parents with no earned income" is plain but has some rhetorical pull. |
| edu_loan_cancel | "No relief for those who already repaid" is plain but mirrors one side's argument. |
| inf_transit_shift, inf_highway_shift | Real opposites with no `mirror_of`. Not added because the brief covered only removing or revising links. Dollar figures differ ($10B vs $5B). |
| cj_death_penalty_end, cj_death_penalty_expand | Related, not linked, not exact opposites. Left unlinked. |
| econ_noncompete_limit, gun_nonviolent_restoration, cj_marijuana_deschedule | Labels are defensible but have cross-party support. Kept. |
| econ_central_bank_audit, imm_asylum_wait_abroad, gov_release_voting, soc_orientation_discrimination, inf_air_traffic_corporation, gun_rifle_feature_ban, econ_union_card_recognition | Text changed (see below), but the idea still recalls a known bill or program. |

## Changed bills

| Bill | Tags | Reason |
|---|---|---|
| econ_min_wage_index | A | Removed "budget analysts project" and job-loss forecast. |
| econ_min_wage_hold | A | Same; parallel to its mirror. |
| econ_union_private_ballot | A | Removed forecast that fewer drives succeed; stated the election period. |
| econ_union_card_recognition | A | Parallel to mirror; period stated as removed. |
| econ_overtime_threshold | R A | Dollar threshold tracked a real rule; now a state-median formula. Removed "may lead". |
| econ_merger_burden | A | Removed "blocking deals that could have lowered costs"; review period is now a term. |
| econ_noncompete_limit | L | Removed "making job changes easier". |
| econ_loan_rate_cap | A | Removed "estimated" credit-loss forecast; stated as a bar on lending above the cap. |
| econ_rule_expiry | B A | Added a $500M review cost; removed "uncertainty". |
| econ_app_worker_status | L | Replaced "preserving flexible schedules". |
| econ_spending_growth_cap | A | "Projected deficits" became planned spending. |
| econ_license_reciprocity | L | Replaced "making it easier". |
| econ_central_bank_audit | A | Removed "increasing the risk". |
| econ_machinery_tariff | L | Replaced "supporting domestic toolmakers". |
| tax_estate_exempt_lower | L | Removed "family farms" as a persuasive beneficiary. |
| tax_estate_exempt_raise | L | Same. |
| tax_corp_rate_cut | A | Removed "economists expecting". |
| tax_corp_rate_raise | A | Same. |
| tax_gains_top_earners | R | $1M threshold matched a well-known budget proposal; now $2M. |
| tax_net_worth | A | Removed "estimated". |
| tax_buyback_excise | R L | 4 percent matched a well-known proposal; now 5. Removed "retirement funds". |
| tax_two_bracket | L | Removed "simplifying filing"; named affected brackets. |
| tax_full_expensing | A | Removed "possible gains in investment". |
| tax_enforcement_cut | A | Removed "projected". |
| tax_universal_savings | R A | $10,000 matched a real bill; now $8,000. Distribution forecast became "no income limit". |
| tax_state_local_deduction | R | Author flag. Income-cap repeal became an 8-percent-of-income limit. |
| tax_fund_manager_income | A | Removed forecast of fund restructuring. |
| tax_mortgage_deduction_phaseout | A | Removed home-value forecast. |
| hc_drug_negotiation_expand | A | Removed "projected" new-medicine forecast. |
| hc_drug_negotiation_limit | A | Same. |
| hc_federal_plan_exchange | A | Removed 10 percent premium forecast. |
| hc_premium_credit_extend | R | 8.5 percent and uncapped range tracked real law; now 9 percent, 400 to 600 percent of poverty. |
| hc_nurse_ratios | A L | Removed "could lead rural hospitals to close". |
| hc_medicaid_work_hours | R A | Author flag. Age, hours and checks changed; removed "budget analysts project". |
| hc_savings_account_limits | A | Distribution forecast became a plain eligibility term. |
| hc_medicaid_per_person | B | Removed "giving states more program flexibility". |
| hc_interstate_plans | B A | Removed "widening choices" and premium forecast. |
| hc_malpractice_cap | A L | Removed premium forecast and "severely injured". |
| hc_drug_import | A | Removed 20 percent price forecast. |
| hc_site_payment_parity | L | Removed "including some rural ones". |
| hc_living_donor_credit | A L | Removed transplant forecast and "low-income donors". |
| tech_ai_audit_exempt | M | Now names the same six months and $5M as its mirror. |
| tech_data_opt_in | A | "Reducing revenue" became limiting data sales. |
| tech_hiring_software_audit | A | Removed "may lead smaller firms to drop"; now no small-firm exemption. |
| tech_platform_self_preference | E R L | 50M-user test tracked a real bill; now 80M, marketplaces and app stores. Removed "users rely on". |
| tech_platform_viewpoint | A | Removed "possibly". |
| tech_adult_site_id | A | Removed breach forecast; stated the ID requirement. |
| tech_token_exemption | R | $75M matched real bills; now $40M. |
| tech_contractor_china_gear | E A | Removed "foreign supply-chain risks". |
| tech_drone_waivers | E A | Removed collision and privacy risk forecast. |
| tech_repair_access | A | Removed cost and security-risk forecast. |
| tech_face_recognition_warrant | A | Removed "days or weeks". |
| tech_message_decrypt | A | Removed "weakening security"; stated the design limit. |
| ss_paid_leave | R | 0.4 percent matched a real bill; now 0.5. Cost stated as a job-hold rule. |
| ss_child_care_cap | A | Removed "may not meet". |
| ss_voucher_guarantee | A | Removed rent forecast; now no spending limit. |
| ss_disability_asset_limit | E R | $2,000 to $10,000 matched a real bill; now $7,500. |
| ss_payroll_tax_above_cap | A | "Extending solvency" kept as a figure, reworded to match its counterpart. |
| ss_retirement_age_69 | A | Same. |
| ss_housing_time_limit | B A | Added a $3B budget figure; removed "eviction risk". |
| ss_religious_providers | B | Removed "widening the pool". |
| ss_benefit_recheck | A | Removed savings forecast. |
| ss_foster_care_age | L | "Cannot meet" became "do not meet". |
| edu_loan_full_repay | L | Removed "low-income borrowers and public service workers". |
| edu_community_college | R A | 75/25 matched a real bill; now 60/40. Removed enrollment forecast. |
| edu_preschool_match | A L | Removed "shifting families"; stated where funds go. |
| edu_forprofit_debt_test | R L | 8 percent matched a real rule; now 10. Removed "older and working students". |
| edu_scholarship_credit | R A | $5,000 matched a real bill; now $3,000. Removed revenue forecast. |
| edu_course_materials_online | L | "Complicating" became a plain planning requirement. |
| edu_endowment_tax | A | "Reducing funds" became "funds colleges can use". |
| edu_test_growth_funding | E L | Removed "rewarding improving districts". |
| edu_program_block_grant | A | Savings became a cut to administrative funding. |
| edu_phone_ban | L | Removed "emergencies". |
| edu_short_program_grants | A | Removed "uneven completion rates"; now no minimum completion rate. |
| edu_state_accreditors | A | Removed "increasing the risk". |
| imm_status_bar | M L | Same population as mirror. Removed "reducing labor supply". |
| imm_status_path | M | Same population as mirror. |
| imm_refugee_floor | L | Removed "communities with limited housing". |
| imm_refugee_ceiling | L | "Lengthening waits" became a plain limit. |
| imm_child_arrivals_residence | R | Author flag. Permanent residence became renewable ten-year residence; added age test. |
| imm_court_lawyers | A | Removed missed-hearing forecast. |
| imm_detention_limit | A | Removed "may miss hearings". |
| imm_visa_job_change | E A | Removed wage forecast. |
| imm_work_verification | L | Removed "wrongly flagging about 1 percent". |
| imm_asylum_wait_abroad | B A L | Added a $1B cost; removed arrival forecast and "border towns with limited services". |
| imm_family_visa_limit | R L | Tracked a real bill; now a ten-year phaseout moving half to employment visas. Removed "separating families". |
| imm_border_barriers | A | Removed crossing forecasts. |
| imm_visa_highest_wage | A | Removed 20 percent pay forecast. |
| imm_stem_graduate_residence | A | "Increasing competition" reworded plainly. |
| cj_drug_min_raise | M | Same scope as mirror. Removed "leverage in plea talks". |
| cj_drug_min_end | M | Same scope as mirror. |
| cj_bail_limit | A | Removed "may fail to appear". |
| cj_officer_lawsuits | A | Removed "possibly affecting recruitment". |
| cj_body_camera_database | A | Removed "privacy concerns". |
| cj_record_sealing | E L | Removed "easing job searches". |
| cj_death_penalty_end | L | Removed "terrorism and mass murder". |
| cj_death_penalty_expand | A | Removed "possibly deterring". |
| cj_juvenile_adult_prosecution | B L | Added a $50M cost; removed "serious offenders". |
| cj_repeat_pretrial_hold | L | Removed "later acquitted". |
| cj_forfeiture_conviction | L | "Reducing" became "ending" those seizures. |
| cj_marijuana_deschedule | A | Removed "complicating enforcement". |
| cj_older_prisoner_release | L | "Releasing violent" became a plain coverage statement. |
| gun_private_check_require | R | Close-family exemption tracked a real bill; now a sale-for-money test with a gift exemption. |
| gun_private_check_bar | M | Scope matched to mirror. |
| gun_wait_bar | A | Removed "some studies link". |
| gun_wait_require | A L | Same; removed "people facing immediate threats". New figure: about 40 states with no waiting period. |
| gun_rifle_feature_ban | L | Removed "popular sporting rifles" and "mass shootings". |
| gun_rifle_age_21 | L | Removed hunters and rural persuasion. |
| gun_maker_liability | L | Removed "shooting victims". |
| gun_carry_reciprocity | R | Author flag. Now limited to visits of up to 30 days. |
| gun_suppressor_registration | R A F | Author flag. Tax already zero since 2026, so removed; keeps checks; removed hearing and locating forecasts. |
| gun_school_staff_arming | A | Removed accident and liability risks. |
| gun_dealer_inspections | A L | Removed "burdens" and "likely". |
| gun_voluntary_self_list | L | Removed "people at risk of suicide". |
| gun_nonviolent_restoration | L | Removed "some who later offend". |
| env_ev_fee | M F A | No federal credit exists to end, so it now bars one. Removed "projected". |
| env_ev_credit | M F A | Now creates the credit. Removed "projected"; distribution became "no income limit". |
| env_lease_pause | A | "Lowering long-term emissions" became lower production. |
| env_lease_required | A | Same. |
| env_clean_power_standard | A | Removed bill-increase forecast. |
| env_methane_inspections | A | Removed "leading some small wells to close". |
| env_review_time_limit | E R | One year and 150 pages tracked real law; now 18 months and 200 pages. |
| env_wetland_scope | A | "Freeing for development" merged into permit coverage. |
| env_appliance_payback | A | Removed energy-use forecast. |
| env_reactor_licensing | A L | Removed "low-carbon" benefit claim. |
| env_ethanol_phaseout | A | Removed price forecast. |
| env_transmission_siting | A | Forecast of five years saved became a two-year limit. |
| intl_defense_cut | A | Removed readiness forecast as a closing clause; now a plain funding cut. |
| intl_arms_rights_condition | A | Removed "possibly straining". |
| intl_trade_labor_terms | A | Removed "raising conditions abroad" and price forecast. |
| intl_china_investment | E | Label only. |
| intl_taiwan_military_aid | A | Removed "increasing the risk of conflict". |
| intl_tariff_approval | R | 60 days matched a real bill; now 120 days, tariffs above 10 percent. |
| gov_mail_excuse | A | Removed "projected" turnout forecast. |
| gov_mail_universal | A | Same. |
| gov_auto_registration | A | Removed "increasing list errors". |
| gov_dc_statehood | A | Removed "changing the balance of the Senate". |
| gov_small_donor_match | L | Removed "candidates some taxpayers oppose". |
| gov_release_voting | B | Added parole scope, a plain stated term. |
| gov_proof_citizenship | R A L | Now a records match with a document fallback. Removed "estimated" and "burdening". |
| gov_photo_id | A | Removed turnout and confidence forecasts. |
| gov_senior_staff_at_will | R L | 50,000 tracked a real order; now top two grades, 30,000. Removed "poor performers". |
| gov_agency_relocation | L | Removed "losing experienced employees". |
| gov_major_rule_approval | A | Removed "about 50 rules annually". Added a 90-day window. |
| gov_member_stock_ban | A | Removed "discouraging some people". |
| gov_ranked_primaries | A | Removed "more ballot errors". |
| gov_term_limits_amendment | R A | Six and two terms tracked a known proposal; now 16 years total. Removed staff-influence forecast. |
| soc_sports_inclusion | M L | Same scope as mirror. Removed "competitive fairness". |
| soc_sports_restrict | M L | Same scope as mirror. Removed "disputes". |
| soc_orientation_discrimination | L | "Exposing" became "allowing lawsuits". |
| soc_contraceptive_coverage | L | Removed "act against their beliefs". |
| soc_pay_reporting | A | Removed lawsuit forecast. |
| soc_housing_harm_commission | R L | Removed "families harmed"; narrowed to denied federal home loans. |
| soc_ceremony_service_exemption | L | Replaced "widening religious accommodation". |
| soc_english_official | L | "Limiting access" became removing forms. |
| soc_minor_hormones_bar | L | Replaced the contested term "cross-sex hormones". |
| soc_teen_social_accounts | A | Removed screen-exposure forecast. |
| soc_betting_ads | L | Removed "young viewers". |
| soc_permanent_daylight | R L | Author flag. Reworded only. Removed "schoolchildren" and retail forecast. |
| inf_wage_exempt | A | Removed 7 percent forecast. |
| inf_wage_require | A | Same. |
| inf_transit_shift | L | "Sharpest effects" became a plain per-person term. |
| inf_highway_shift | L | Same. |
| inf_lead_lines | A | Rate rise now stated as how utilities cover the remainder. |
| inf_federal_bank | L | "Taxpayer risk" became a plain liability term. |
| inf_passenger_rail | A | Removed "uncertain ridership" and "projected"; fare rule is now a term. |
| inf_toll_leases | L | Named who pays. |
| inf_small_project_review | L | Parallel wording of the two removals. |
| inf_air_traffic_corporation | L | "Reducing" became "ending direct" control. |
| inf_road_mile_fee | A | Removed "privacy concerns". |
| inf_domestic_materials | F R | The domestic rule is already law; now removes its waivers. |
| inf_rural_fiber | A | Cost forecast became a per-home limit. |
