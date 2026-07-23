# Scottish Parliament (GB-SCT) Audit Variable Summary

**Specification Version:** 2.7.0 (Post-API Probe & Expert Review)  
**Purpose:** Unabridged, complete scannable checklist of ALL Scottish Parliament variables cataloged for `CanonicalBill` (Macro Level), `CanonicalAmendment` (Micro Level), `CommitteeContext` (Committee Level), and `ParsedProceedings` (Hansard Text Level).

---

## ENTITY 1: MACRO BILL LEVEL VARIABLES (`CanonicalBill`)

### 1. Assembly, Electoral & Executive Context
1. **`jurisdiction_code`**: Unique assembly code (`GB-SCT`)
2. **`name`**: Assembly name (*Scottish Parliament / Pàrlamaid na h-Alba*)
3. **`chamber_type`**: Chamber structure (`DEVOLVED_UNICAMERAL`)
4. **`statutory_seats_total`**: Statutory seat count (`129` MSP seats)
5. **`presiding_officer_neutral_count`**: Presiding officer neutral non-voting count (`1`)
6. **`parliament_term`**: Electoral period identifier (`Session 6`, `Session 5`, etc.)
7. **`term_start_date`**: Start date of parliamentary term (from `/api/sessions`, e.g. `2021-05-13`)
8. **`term_end_date`**: End date of parliamentary term (from `/api/sessions`, e.g. `2026-05-07`)
9. **`devolved_executive_name`**: Historical executive entity name (`"Scottish Executive"` 1999–2007; `"Scottish Government"` 2007–Present)
10. **`government_type`**: Executive arrangement (`SINGLE_PARTY_MAJORITY`, `SINGLE_PARTY_MINORITY`, `FORMAL_COALITION_MAJORITY`, `FORMAL_COALITION_MINORITY`, `CONFIDENCE_AND_SUPPLY`, `COOPERATION_AGREEMENT`, `CARETAKER_TECHNOCRATIC`)
11. **`governing_parties_list`**: Array of governing parties (e.g. `["SNP", "Scottish Greens"]` 2021–2024; `["SNP"]` 2024–Present)
12. **`parlgov_cabinet_id`**: Linked cabinet ID from ParlGov benchmark dataset (`GB-SCT-CAB-2021`)

### 2. Bill Identification, Sponsorship & Temporal Origin
13. **`local_bill_id`**: Native Holyrood reference code (e.g. `SP Bill 13`)
14. **`title_canonical`**: Standardized short title (e.g. *Gender Recognition Reform (Scotland) Bill*)
15. **`initiator_type`**: Neutral sponsor type (`EXECUTIVE`, `INDIVIDUAL_MEMBER`, `COMMITTEE`, `PRIVATE_ORGANISATION`)
16. **`initiator_party_governance_role`**: Primary sponsor party alignment on introduction date $T_{\text{Intro}}$ (`GOVERNING_PARTY`, `OPPOSITION_PARTY`, `CROSS_PARTY`)
17. **`initiator_member_id`**: Lead MSP sponsor persistent identifier (Wikidata QID / Holyrood MSP ID)
18. **`ministerial_portfolio_title`**: Lead Minister's exact portfolio title from `/api/GovernmentRoles` (e.g. *Cabinet Secretary for Health and Social Care*)
19. **`initiator_convener_member_id`**: Lead Committee Convener MSP ID (if Committee Bill)
20. **`initiator_organisation_name`**: Initiating Committee Name or External Promoter (if Committee or Private Bill)
21. **`third_party_organisation`**: External non-governmental promoter organisation from `/api/bills` (for Private Bills)

### 3. Progression, Stage Timelines & Multi-Day Debates
22. **`date_introduced`**: Date introduced in Parliament
23. **`date_final_outcome`**: Date of final passage, vote defeat, or withdrawal
24. **`duration_calendar_days`**: Total calendar days elapsed
25. **`duration_sitting_days`**: Total formal parliamentary sitting days elapsed
26. **`stage_1_lead_committee_report_date`**: Date Stage 1 report published by lead committee
27. **`stage_1_debate_start_date`**: Start date of Stage 1 debate in Chamber
28. **`stage_1_debate_end_date`**: End date of Stage 1 debate in Chamber
29. **`stage_1_debate_days_count`**: Number of sitting days Stage 1 debate straddled (e.g. `1` or `2` days)
30. **`stage_2_committee_start_date`**: Start date of Stage 2 committee amendment consideration
31. **`stage_2_committee_end_date`**: Completion date of Stage 2 committee consideration
32. **`stage_3_plenary_debate_start_date`**: Start date of Stage 3 plenary debate & final passage
33. **`stage_3_plenary_debate_end_date`**: End date of Stage 3 plenary debate & final passage
34. **`stage_3_debate_days_count`**: Number of sitting days Stage 3 debate straddled (e.g. `1` or `2` days)
35. **`royal_assent_date`**: Date of Royal Assent (*Promulgation*)
36. **`emergency_procedure_flag`**: `True`/`False` (Emergency Bill designation under Rule 9.21)
37. **`section_35_order_triggered_flag`**: `True`/`False` (Secretary of State Section 35 Scotland Act Order issued blocking Royal Assent)
38. **`programme_motion_flag`**: `UNAVAILABLE_HARD_GAP` (Westminster concept; Holyrood uses Business Motions agreed by Bureau)
39. **`guillotine_invoked_flag`**: `UNAVAILABLE_HARD_GAP` (Not applicable to Holyrood procedure)

### 4. Financial Resolutions (Rule 9.12)
40. **`financial_resolution_required_flag`**: `True`/`False` (Financial Resolution motion required under Rule 9.12 before Stage 2)
41. **`financial_resolution_approved_flag`**: `True`/`False` (Financial Resolution approved by Parliament)
42. **`financial_resolution_vote_date`**: Date of Financial Resolution vote
43. **`financial_resolution_aye_count`**: Financial Resolution Aye vote tally
44. **`financial_resolution_no_count`**: Financial Resolution No vote tally
45. **`financial_resolution_abstain_count`**: Financial Resolution Abstain vote tally

### 5. Plenary Motion Roll-Call Votes (NATIVE_DIRECT Feed)
*For every major Plenary Motion vote (Stage 1 Agreement, Financial Resolution, Emergency Designation, Stage 3 Passage), the platform records a complete decision-point vote object:*
46. **`decision_point_motion_type`**: `[STAGE_1_AGREEMENT, FINANCIAL_RESOLUTION, EMERGENCY_BILL_DESIGNATION, STAGE_3_PASSAGE]`
47. **`decision_point_vote_date`**: Date $T$ of division
48. **`decision_point_result`**: Outcome (`PASSED`, `DEFEATED`)
49. **`decision_point_aye_count` / `no_count` / `abstain_count`**: Plenary vote tallies
50. **`decision_point_party_cohesion_rate`**: Governing party voting unity rate
51. **`decision_point_voting_coalition_type`**: `[UNANIMOUS, GOVERNMENT_PARTY_LINE, CROSS_PARTY_MAJORITY]`
52. **`individual_msp_votes_array`**: Array of individual MSP vote choices paired with party affiliation evaluated on date $T$

### 6. Accompanying Bill Documents & Size Analytics
53. **`doc_as_introduced_url`**: Official URL of Bill text as introduced
54. **`doc_as_passed_url`**: Official URL of Bill text as enacted
55. **`policy_memorandum_url`**: Policy Memorandum URL & word count
56. **`financial_memorandum_url`**: Financial Memorandum URL & word count
57. **`explanatory_notes_url`**: Explanatory Notes URL & word count
58. **`combined_financial_explanatory_notes_url`**: Legacy Combined Financial & Explanatory Notes URL (pre-split format)
59. **`delegated_powers_memorandum_url`**: Delegated Powers Memorandum URL & word count
60. **`stage_1_lead_committee_report_url`**: Lead Committee Stage 1 Report URL & word count
61. **`bill_as_introduced_word_count`**: Word count of official text as introduced
62. **`bill_as_amended_stage_2_word_count`**: Word count post-Stage 2 committee amendments
63. **`bill_as_enacted_word_count`**: Word count of final enacted Act
64. **`text_expansion_ratio`**: Text growth ratio ($\frac{\text{word\_count\_enacted}}{\text{word\_count\_introduced}}$)
65. **`cap_topic_code`**: Comparative Agendas Project policy topic code
66. **`fiscal_impact_flag`**: `True`/`False` (Binding fiscal expenditure or taxation impact)

### 7. Final Disposition & Inter-Chamber Mechanisms
67. **`final_status`**: Terminal procedural status (`ENACTED`, `DEFEATED`, `WITHDRAWN`, `LAPSED`, `PENDING`, `VETOED`)
68. **`termination_mechanism`**: Terminal procedural event (`ENACTMENT`, `VOTE_DEFEAT`, `EXECUTIVE_WITHDRAWAL`, `DISSOLUTION_LAPSE`)

### 8. Macro Bill Amendment Aggregates
69. **`amendments_tabled_count`**: Total Stage 2 + Stage 3 amendments lodged
70. **`amendments_agreed_count`**: Total amendments formally adopted
71. **`amendments_non_executive_count`**: Total non-executive/opposition amendments lodged
72. **`committee_amendments_executive_acceptance_rate`**: Proportion of non-executive committee amendments supported by government (*from PhD dataset*)
73. **`bill_text_alteration_score`**: Text similarity score comparing introduced vs enacted text

---

## ENTITY 2: MICRO AMENDMENT LEVEL VARIABLES (`CanonicalAmendment`)

### 9. Granular Amendment Entity Records & Marshalled Lists
74. **`canonical_amendment_id`**: Persistent unique amendment identifier (e.g. `GB-SCT-S6-SPB13-AMD-042`)
75. **`local_amendment_number`**: Holyrood Marshalled List amendment number (e.g. `Amd 42`, `LOD 104`)
76. **`bill_id`**: Parent bill link (`SP Bill 13`)
77. **`marshalled_list_url`**: URL of source Marshalled List PDF/HTML document
78. **`stage_canonical`**: Stage of consideration (`COMMITTEE_STAGE`, `REPORT_STAGE`, `FINAL_PASSAGE`)
79. **`stage_raw`**: Native stage text (e.g. *Stage 2 Equalities Committee Day 3*)
80. **`committee_name`**: Scrutinising committee name from `/api/committees`
81. **`committee_type`**: Committee type from `/api/committeetypes` (`Mandatory`, `Subject`, `Ad Hoc`)
82. **`date_tabled`**: Date amendment lodged
83. **`date_decided`**: Date voted on or disposed
84. **`sponsor_member_id`**: Lead MSP sponsor Wikidata QID
85. **`sponsor_name`**: Full name of lead MSP sponsor
86. **`sponsor_party_on_tabling_date`**: MSP party status evaluated on exact tabling date $T_{\text{Tabled}}$
87. **`sponsor_party_leadership_role`**: Sponsor party frontbench role on tabling date from `/api/memberpartyroles` (e.g. Leader, Whip)
88. **`sponsor_governance_role`**: Sponsor institutional alignment (`EXECUTIVE_MINISTER`, `GOVERNING_BACKBENCH`, `OPPOSITION_MEMBER`, `CROSS_PARTY`)
89. **`co_sponsors_count`**: Count of co-signing MSPs
90. **`target_clause_or_schedule`**: Structural target in Bill (e.g. *Section 4, Page 3, Line 12*)
91. **`amendment_action_type`**: Text alteration type (`INSERTION`, `DELETION`, `SUBSTITUTION`)
92. **`government_position`**: Executive stance during debate (`SUPPORTED`, `OPPOSED`, `NEUTRAL_NO_STANCE`, `MINISTERIAL_OWN_AMENDMENT`)
93. **`disposition_canonical`**: Final outcome (`AGREED_TO`, `DEFEATED`, `WITHDRAWN`, `NOT_MOVED`, `FALLEN`)
94. **`decision_mechanism`**: Decision method (`VOICE_VOTE_UNANIMOUS`, `DIVISION_ROLL_CALL`, `WITHDRAWN_WITHOUT_VOTE`)
95. **`division_id`**: Linked roll-call division vote ID
96. **`aye_count` / `no_count` / `abstain_count`**: Division vote tallies
97. **`party_dissent_rate_on_amendment`**: Proportion of governing MSPs rebelling against frontbench whip on this amendment division

---

## ENTITY 3: COMMITTEE CONTEXT & MEMBERSHIP (`CommitteeContext`)

### 10. Native Committee Roster Engine (from `/api/PersonCommitteeRoles`)
98. **`committee_id`**: Unique committee ID from `/api/committees`
99. **`committee_name`**: Official committee name (e.g. *Equalities, Human Rights and Civil Justice Committee*)
100. **`committee_type`**: Committee classification (`Mandatory`, `Subject`, `Ad Hoc`)
101. **`committee_convener_member_id`**: MSP ID of Committee Convener (evaluated on date $T$)
102. **`committee_deputy_convener_member_id`**: MSP ID of Deputy Convener (evaluated on date $T$)
103. **`committee_membership_roster`**: Complete array of MSP members assigned to committee with exact `ValidFromDate` and `ValidUntilDate` bounds

---

## DOMAIN 11: PARSED PROCEEDINGS & OFFICIAL REPORT ANALYTICS

### 11. Plenary & Committee Proceedings Text Ingestion
104. **`official_report_proceedings_url`**: Official Report Hansard transcript URL for bill debate
105. **`proceedings_total_word_count`**: Total word count of debate proceedings for the bill
106. **`proceedings_interventions_count`**: Total recorded speech interventions during debate
107. **`proceedings_msps_speaking_count`**: Count of unique MSPs participating in debate
108. **`executive_ministers_word_count_share`**: Proportion of debate word count spoken by Executive Ministers
109. **`backbench_msps_word_count_share`**: Proportion of debate word count spoken by backbench/opposition MSPs
