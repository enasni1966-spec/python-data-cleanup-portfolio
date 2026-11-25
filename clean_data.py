import pandas as pd
import numpy as np
import re

# 1. Load raw dataset
df = pd.read_csv("messy_customers.csv")
initial_rows = len(df)

# 2. Standardize whitespace and casing on names & cities
df["full_name"] = (
    df["full_name"]
    .astype(str)
    .str.strip()
    .str.replace(r"\s+", " ", regex=True)
    .str.title()
)
df["city"] = df["city"].astype(str).str.strip().str.title()

# 3. Standardize state names to 2-letter USPS abbreviations
state_map = {
    "california": "CA", "texas": "TX", "illinois": "IL", "ohio": "OH",
    "washington": "WA", "michigan": "MI", "tennessee": "TN",
    "wisconsin": "WI", "georgia": "GA", "minnesota": "MN"
}
df["state"] = (
    df["state"]
    .astype(str)
    .str.strip()
    .str.lower()
    .replace(state_map)
    .str.upper()
)

# 4. Fix common email domain typos & standardize lowercase
df["email"] = df["email"].astype(str).str.strip().str.lower()
email_fixes = {
    r"@gmial\.com$": "@gmail.com",
    r"@gmail\.con$": "@gmail.com",
    r"@yahoo\.con$": "@yahoo.com",
}
for pattern, replacement in email_fixes.items():
    df["email"] = df["email"].str.replace(pattern, replacement, regex=True)

# 5. Deduplicate (first exact rows, then duplicate emails keeping earliest signup)
df["signup_date"] = pd.to_datetime(df["signup_date"], format="mixed", errors="coerce")
df = df.sort_values("signup_date").drop_duplicates()
df = df.drop_duplicates(subset=["email"], keep="first")

# 6. Normalize phone numbers to (XXX) XXX-XXXX
def format_phone(val):
    if pd.isna(val):
        return np.nan
    digits = re.sub(r"\D", "", str(val))
    if len(digits) == 11 and digits.startswith("1"):
        digits = digits[1:]
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    return np.nan

df["phone"] = df["phone"].apply(format_phone)

# 7. Clean currency formatting & handle invalid/negative spend
df["total_spent"] = (
    df["total_spent"]
    .astype(str)
    .str.replace(r"[\$,]", "", regex=True)
    .str.strip()
)
df["total_spent"] = pd.to_numeric(df["total_spent"], errors="coerce")
df.loc[df["total_spent"] < 0, "total_spent"] = np.nan
df["total_spent"] = df["total_spent"].fillna(0.0).round(2)

# 8. Sort by customer_id and export
df = df.sort_values("customer_id").reset_index(drop=True)
df.to_csv("cleaned_customers.csv", index=False)

print(f"Cleanup complete: {initial_rows} raw rows -> {len(df)} clean unique records.")
