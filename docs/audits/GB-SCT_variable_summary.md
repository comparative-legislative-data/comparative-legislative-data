# Scottish Parliament (GB-SCT) Audit Variable Summary

**Specification Version:** 2.5.0  
**Purpose:** Unabridged, complete scannable checklist of ALL Scottish Parliament variables cataloged for `CanonicalBill` (Macro Level) and `CanonicalAmendment` (Micro Level).

---

## ENTITY 1: MACRO BILL LEVEL VARIABLES (`CanonicalBill`)

### 1. Assembly, Electoral & Executive Context
1. **`jurisdiction_code`**: Unique assembly code (`GB-SCT`)
2. **`name`**: Assembly name (*Scottish Parliament / Pàrlamaid na h-Alba*)
3. **`chamber_type`**: Chamber structure (`DEVOLVED_UNICAMERAL`)
4. **`statutory_seats_total`**: Statutory seat count (`129` MSP seats)
5. **`presiding_officer_neutral_count`**: Presiding officer neutral non-voting count (`1`)
6. **`parliament_term`**: Electoral period (`Session 6`, `Session 5`, etc.)
7. **`government_type`**: Executive arrangement (`SINGLE_PARTY_MAJORITY`, `SINGLE_PARTY_MINORITY`, `FORMAL_COALITION_MAJORITY`, `FORMAL_COALITION_MINORITY`, `CONFIDENCE_AND_SUPPLY`, `COOPERATION_AGREEMENT`, `CARETAKER_TECHNOCRATIC`)
8. **`parlgov_cabinet_id`**: Linked cabinet ID from ParlGov benchmark dataset (`GB-SCT-CAB-2021`)

### 2. Bill Identification, Sponsorship & Temporal Origin
9. **`local_bill_id`**: Native Holyrood reference code (e.g. `SP Bill 13`)
10. **`title_canonical`**: Standardized short title (e.g. *Gender Recognition Reform (Scotland) Bill*)
11. **`initiator_type`**: Neutral sponsor type (`EXECUTIVE`, `INDIVIDUAL_MEMBER`, `COMMITTEE`, `PRIVATE_ORGANISATION`)
12. **`initiator_party_governance_role`**: Primary sponsor party alignment on introduction date $T_{\text{Intro}}$ (`GOVERNING_PARTY`, `OPPOSITION_PARTY`, `CROSS_PARTY`)
13. **`initiator_member_id`**: Disambiguated lead MSP sponsor persistent identifier (Wikidata QID / MSP ID)

### 3. Progression, Stage Timelines & Procedural Flags
14. **`date_introduced`**: Date introduced in Parliament
15. **`date_final_outcome`**: Date of final passage, vote defeat, or withdrawal
16. **`duration_calendar_days`**: Total calendar days elapsed
17. **`duration_sitting_days`**: Total formal parliamentary sitting days elapsed
18. **`stage_1_lead_committee_report_date`**: Date Stage 1 report published by lead committee
19. **`stage_1_parliament_agreement_vote_date`**: Date of formal Stage 1 debate & agreement vote in Chamber
20. **`stage_2_committee_start_date`**: Start date of Stage 2 committee amendment consideration
21. **`stage_2_committee_end_date`**: Completion date of Stage 2 committee consideration
22. **`stage_3_plenary_debate_date`**: Date of Stage 3 plenary debate & final passage vote
23. **`royal_assent_date`**: Date of Royal Assent (*Promulgation*)
24. **`programme_motion_flag`**: `True`/`False` (Timetabling or programme motion imposed)
25. **`guillotine_invoked_flag`**: `True`/`False` (Debate closure or guillotine motion invoked)
26. **`emergency_procedure_flag`**: `True`/`False` (Emergency Bill designation under Rule 9.21)
27. **`financial_resolution_motion_flag`**: `True`/`False` (Financial Resolution motion required under Rule 9.12 before Stage 2)
28. **`section_35_order_triggered_flag`**: `True`/`False` (Secretary of State Section 35 Scotland Act Order issued blocking Royal Assent)

### 4. Final Disposition & Inter-Chamber Mechanisms
29. **`final_status`**: Terminal procedural status (`ENACTED`, `DEFEATED`, `WITHDRAWN`, `LAPSED`, `PENDING`, `VETOED`)
30. **`termination_mechanism`**: Terminal procedural event (`ENACTMENT`, `VOTE_DEFEAT`, `EXECUTIVE_WITHDRAWAL`, `DISSOLUTION_LAPSE`)
31. **`chamber_ping_pong_count`**: Bicameral amendment exchange count (N/A for unicameral Holyrood)

### 5. Bill Documentation & Text Size Analytics
32. **`doc_as_introduced_url`**: Official URL of Bill text as introduced
33. **`doc_as_passed_url`**: Official URL of Bill text as enacted
34. **`bill_as_introduced_word_count`**: Word count of official text as introduced
35. **`bill_as_amended_stage_2_word_count`**: Word count post-Stage 2 committee amendments
36. **`bill_as_enacted_word_count`**: Word count of final enacted Act
37. `text_expansion_ratio`: Text growth ratio ($\frac{\text{word\_count\_enacted}}{\text{word\_count\_introduced}}$)
38. **`cap_topic_code`**: Comparative Agendas Project policy topic code
39. **`fiscal_impact_flag`**: `True`/`False` (Binding fiscal expenditure or taxation impact)

### 6. Committee Scrutiny & Evidence
40. **`lead_committee_name`**: Primary scrutinising committee assigned (e.g. *Equalities, Human Rights and Civil Justice Committee*)
41. **`committee_evidence_submissions_count`**: Total published written evidence submissions received

### 7. Macro Bill Amendment Aggregates
42. **`amendments_tabled_count`**: Total Stage 2 + Stage 3 amendments lodged
43. **`amendments_agreed_count`**: Total amendments formally adopted
44. **`amendments_non_executive_count`**: Total non-executive/opposition amendments lodged
45. **`committee_amendments_executive_acceptance_rate`**: Proportion of non-executive committee amendments supported by government (*from PhD hand-coded dataset*)
46. **`bill_text_alteration_score`**: Text similarity score comparing introduced vs enacted text

### 8. Divisions, Floor Arithmetic & Voting Coalitions
47. **`divisions_count`**: Total recorded roll-call division votes held on the bill
48. **`effective_majority_margin_at_event_date`**: Floor majority margin ($\text{Governing Seats}_T - \text{Opposition Seats}_T$) evaluated on division date $T$
49. **`party_dissent_rate_at_event_date`**: Proportion of party MSPs rebelling against frontbench whip on division date $T$
50. **`voting_coalition_type`**: Division voting alignment (`UNANIMOUS`, `GOVERNMENT_PARTY_LINE`, `CROSS_PARTY_MAJORITY`)

---

## ENTITY 2: MICRO AMENDMENT LEVEL VARIABLES (`CanonicalAmendment`)

### 9. Granular Amendment Entity Records
51. **`canonical_amendment_id`**: Persistent unique amendment identifier (e.g. `GB-SCT-S6-SPB13-AMD-042`)
52. **`local_amendment_number`**: Holyrood Marshalled List amendment number (e.g. `Amd 42`, `LOD 104`)
53. **`bill_id`**: Parent bill link (`SP Bill 13`)
54. **`stage_canonical`**: Stage of consideration (`COMMITTEE_STAGE`, `REPORT_STAGE`, `FINAL_PASSAGE`)
55. **`stage_raw`**: Native stage text (e.g. *Stage 2 Equalities Committee Day 3*)
56. **`committee_name`**: Scrutinising committee name
57. **`date_tabled`**: Date amendment lodged
58. **`date_decided`**: Date voted on or disposed
59. **`sponsor_member_id`**: Lead MSP sponsor Wikidata QID
60. **`sponsor_name`**: Full name of lead MSP sponsor
61. **`sponsor_party_on_tabling_date`**: MSP party status evaluated on exact tabling date $T_{\text{Tabled}}$
62. **`sponsor_governance_role`**: Sponsor institutional alignment (`EXECUTIVE_MINISTER`, `GOVERNING_BACKBENCH`, `OPPOSITION_MEMBER`, `CROSS_PARTY`)
63. **`co_sponsors_count`**: Count of co-signing MSPs
64. **`target_clause_or_schedule`**: Structural target in Bill (e.g. *Section 4, Page 3, Line 12*)
65. **`amendment_action_type`**: Text alteration type (`INSERTION`, `DELETION`, `SUBSTITUTION`, `PROBING`) *(from PhD dataset)*
66. **`government_position`**: Executive stance during debate (`SUPPORTED`, `OPPOSED`, `NEUTRAL_NO_STANCE`, `MINISTERIAL_OWN_AMENDMENT`)
67. **`disposition_canonical`**: Final outcome (`AGREED_TO`, `DEFEATED`, `WITHDRAWN`, `NOT_MOVED`, `FALLEN`)
68. **`decision_mechanism`**: Decision method (`VOICE_VOTE_UNANIMOUS`, `DIVISION_ROLL_CALL`, `WITHDRAWN_WITHOUT_VOTE`)
69. **`division_id`**: Linked roll-call division vote ID
70. **`aye_count`**: Division Aye vote tally
71. **`no_count`**: Division No vote tally
72. **`abstain_count`**: Division Abstain vote tally
73. **`party_dissent_rate_on_amendment`**: Proportion of governing MSPs rebelling against frontbench whip on this amendment division

---

## INSTITUTIONAL HARD GAPS
74. **`committee_stage_2_informal_paper_gap`**: `RECORDED_BUT_UNDIGITIZED` (Informal Stage 2 committee working notes not published in open API format)
