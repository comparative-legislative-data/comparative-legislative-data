# Detailed Audited Schemas for Complex Endpoints

This document lists the complete nested structures of the Votes and Official Report endpoints, dynamically probed from the live data.

## Endpoint: `votesmotion`
Source URL: `https://data.parliament.scot/api/votesmotion?year=2024`

### Key Hierarchy:
- **ID** (str)
- **Detail** (Object):
  - **ID** (int)
  - **MotionAgendaItemID** (int)
  - **AgendaID** (int)
  - **Decision** (str)
  - **DecisionID** (int)
  - **VoteMSP** (str)
  - **VoteResult** (str)
  - **VoteFor** (int)
  - **VoteAgainst** (int)
  - **VoteCasting** (null)
  - **MSPSharesParty** (str)
- **Motion** (Object):
  - **Title** (str)
  - **Reference** (str)
  - **ID** (int)
- **Person** (Object):
  - **ID** (int)
  - **ParliamentaryName** (str)
  - **DisplayName** (str)
  - **PartyAbbreviation** (str)
  - **PartyName** (str)
  - **ConstituencyRegion** (str)
- **Time** (Object):
  - **Start** (str)
  - **End** (str)
  - **ParliamentaryYear** (str)
  - **Session** (str)
- **UpdatedElasticDate** (str)

---

## Endpoint: `orsplenarymeeting`
Source URL: `https://data.parliament.scot/api/orsplenarymeeting?year=2024`

### Key Hierarchy:
- **ID** (str)
- **Meeting** (Object):
  - **Title** (str)
  - **ID** (int)
- **Committee** (Object):
  - **Name** (str)
  - **ID** (int)
- **Time** (Object):
  - **Session** (str)
  - **Start** (str)
  - **End** (str)
  - **ParliamentaryYear** (str)
- **ItemOfBusiness** (Object):
  - **Heading** (str)
  - **HeadingType** (str)
  - **HeadingID** (int)
  - **HeadingDisplayOrder** (float)
  - **SubHeading** (null)
  - **SubHeadingType** (null)
  - **SubHeadingID** (null)
  - **SubHeadingDisplayOrder** (null)
  - **QuestionHeading** (str)
  - **QuestionHeadingID** (int)
  - **QuestionHeadingDisplayOrder** (float)
  - **DisplayOrder** (float)
  - **ID** (int)
  - **ParentID** (int)
- **Person** (Object):
  - **ParliamentaryName** (null)
  - **ID** (null)
  - **PartyName** (null)
  - **PartyAbbreviation** (null)
  - **ConstituencyRegion** (null)
- **Detail** (Object):
  - **SpeakerOffice** (str)
  - **SpeakerName** (str)
  - **SpeakerDisplayName** (str)
  - **ContributionDisplayOrder** (float)
  - **ContributionID** (int)
  - **EditedText** (str)
  - **EditedTextHTML** (str)
- **UpdatedElasticDate** (str)

---

## Endpoint: `orscommitteemeeting`
Source URL: `https://data.parliament.scot/api/orscommitteemeeting?year=2024`

### Key Hierarchy:
- **ID** (str)
- **RecordType** (str)
- **SubType** (str)
- **Meeting** (Object):
  - **ReportID** (int)
  - **Title** (str)
  - **ID** (int)
- **Committee** (Object):
  - **Name** (str)
  - **ID** (int)
- **Time** (Object):
  - **Session** (str)
  - **Start** (str)
  - **End** (str)
  - **ParliamentaryYear** (str)
- **ItemOfBusiness** (Object):
  - **Heading** (str)
  - **HeadingType** (str)
  - **HeadingID** (int)
  - **HeadingDisplayOrder** (float)
  - **SubHeading** (null)
  - **SubHeadingType** (null)
  - **SubHeadingID** (null)
  - **SubHeadingDisplayOrder** (null)
  - **QuestionHeading** (null)
  - **QuestionHeadingID** (null)
  - **QuestionHeadingDisplayOrder** (null)
  - **DisplayOrder** (float)
  - **ID** (int)
  - **ParentID** (int)
- **Person** (Object):
  - **ParliamentaryName** (null)
  - **ID** (null)
  - **BirthDate** (null)
  - **Gender** (null)
  - **PartyName** (null)
  - **PartyAbbreviation** (null)
  - **ConstituencyRegion** (null)
- **Detail** (Object):
  - **SpeakerOffice** (str)
  - **SpeakerName** (str)
  - **SpeakerDisplayName** (str)
  - **ContributionDisplayOrder** (float)
  - **ContributionID** (int)
  - **EditedText** (str)
  - **EditedTextHTML** (str)
- **Location** (Object):
  - **Geometry** (null)
- **UpdatedDate** (str)
- **UpdatedElasticDate** (str)

---
