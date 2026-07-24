# R Data Frame Import Script for Comparative Legislative Data Platform
# Jurisdiction: Scottish Parliament (GB-SCT, May 1999 - Present)
# URL: https://legislativedata.org/api/v1/GB-SCT/canonical/bills

suppressPackageStartupMessages({
  if (!require("jsonlite")) install.packages("jsonlite")
  if (!require("dplyr")) install.packages("dplyr")
})

cat("Fetching 473 canonical bill records from legislativedata.org...
")
url <- "https://legislativedata.org/static/data/GB-SCT_canonical_bills.json"
df <- jsonlite::fromJSON(url)

cat("Successfully imported dataset into R Data Frame 'df'.
")
cat("Dimensions:", dim(df)[1], "rows x", dim(df)[2], "variables.
")
head(df)
