# Senedd (Welsh Parliament) Exploratory Research

**Assembly Identifier:** `GB-WLS`  
**Purpose:** Initial consideration of Welsh Parliament open data, endpoint availability, and ingestion/normalization mapping strategy.

---

## 1. Upstream Data Sources & API Footprint

Unlike the Scottish Parliament's modern JSON OData feeds, the Senedd data is split across legacy SOAP/XML services and XML library streams.

### 1.1 Meeting and Member Data (Modern.Gov)
The Senedd uses the **Modern.Gov** decision management platform. Its public XML/SOAP web service is located at:
`http://business.senedd.wales/mgwebservice.asmx`

Key XML functions for ingestion mapping:
*   `GetCouncillors` (returns Member information, including name, party, gender, and contact links).
*   `GetCommitteeMeetings` (returns committee agendas, attendance lists, and parsed decisions).
*   `GetWards` (returns electoral division/constituency indexes).

### 1.2 Proceedings & Transcripts (Plenary)
Official transcripts of Senedd Plenary sessions (Record of Proceedings) are exposed via a dedicated XML export endpoint:
`http://record.senedd.wales/XMLExport`

### 1.3 Legislation (Bills and Acts)
Bills undergo progress (Stage 1 to Stage 4) in the Senedd. Legislative data is formatted using **Crown XML (CLML)** and must be scraped from individual Bill listings under `https://senedd.wales/legislation`.

---

## 2. Proposed Database Mirror Layer (`raw_gb_wls_*`)

To establish our pristine raw replica layer (Database A) for Wales, we will mirror Senedd entities into these relational schemas:

*   `raw_gb_wls_members` (MS names, genders, and contacts parsed from `GetCouncillors`).
*   `raw_gb_wls_memberparties` (Sessional party affiliations and validity bounds).
*   `raw_gb_wls_parties` (Welsh party names and lookups).
*   `raw_gb_wls_bills` (Bill ID, title, type, and sponsor relationships).
*   `raw_gb_wls_billstages` (Sessional stage dates, votes, and events).

---

## 3. Sessional Boundaries & Coalition Map

To construct the canonical research layer (Database B), we must resolve temporal coalitions and governing status for Wales. Senedd sessions (1 to 6) partition using these date boundaries and coalitions:

### Session 1: 1999–2003
*   **Dates:** `1999-05-06` to `2003-04-30`
*   **Cabinet Coalition:** Labour & Liberal Democrats (from October 2000 onwards; Labour minority prior).

### Session 2: 2003–2007
*   **Dates:** `2003-05-01` to `2007-05-02`
*   **Cabinet Coalition:** Labour Majority / Minority administration.

### Session 3: 2007–2011
*   **Dates:** `2007-05-03` to `2011-05-04`
*   **Cabinet Coalition:** "One Wales" Labour & Plaid Cymru Coalition (from July 2007 onwards).

### Session 4: 2011–2016
*   **Dates:** `2011-05-05` to `2016-05-04`
*   **Cabinet Coalition:** Labour Minority administration.

### Session 5: 2016–2021
*   **Dates:** `2016-05-05` to `2021-05-05`
*   **Cabinet Coalition:** Labour, Liberal Democrat, and Independent coalition cabinet (led by Carwyn Jones and Mark Drakeford).

### Session 6: 2021–Present
*   **Dates:** `2021-05-06` onwards
*   **Cabinet Coalition:** Labour & Plaid Cymru Co-operation Agreement (signed 22 November 2021; terminated 17 May 2024 by Plaid Cymru).

---

## 4. Key Comparative Replication Challenges

1.  **XML Parser Ingests:** We must write an XML-to-SQL converter (potentially in Python using `lxml` or `xml.etree`) rather than our lightweight HTTP JSON request loops used for Scotland.
2.  **Modern.Gov Casing Drift:** Modern.Gov attributes are frequently upper-camel-cased or vary across updates. Ingestion contracts (Pydantic models) will be critical.
3.  **Bill Progression Normalization:** Senedd bills have different stage definitions (e.g. Stage 1 Committee report, Stage 2 Detailed scrutiny, Stage 3 Report stage, Stage 4 Passing vote). We will need to map these to our standardized T1/T2/T3 timescales during the Database B view compilation.
