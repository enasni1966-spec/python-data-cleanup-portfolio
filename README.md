# python-data-cleanup-portfolio
python-data-cleanup-portfolio
3# Python Customer Data Cleanup Pipeline

An automated Python (`pandas`) data-cleaning pipeline that transforms a corrupted CRM export into a standardized dataset.

## Key Issues Resolved
* **Deduplication:** Removed exact row duplicates and resolved fuzzy customer duplicates sharing the same email address.
* **Email Validation & Repair:** Fixed common domain typos (`@gmial.com`, `@gmail.con`, `@yahoo.con`) and standardized casing.
* **Date Standardization:** Unified inconsistent date formats into ISO `YYYY-MM-DD`.
* **Geographic Normalization:** Converted mixed state names into 2-letter abbreviations.
* **Phone & Currency Formatting:** Normalized phone numbers, stripped `$` symbols, and handled invalid values.

## Before & After Sample

### Before (`messy_customers.csv`)
| customer_id | full_name | email | signup_date | phone | state | total_spent |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1001 | `  john smith ` | john.smith@gmail.com | 2023-01-15 | (555) 123-4567 | NY | $120.50 |
| 1002 | SARAH CONNOR | sconnor@yahoo.com | 01/22/2023 | 555-987-6543 | ca | 450.00 |
| 1004 | emily davis | emily.davis@gmial.com | Feb 14, 2023 | 555.222.3333 | Texas | $89.99 |

### After (`cleaned_customers.csv`)
| customer_id | full_name | email | signup_date | phone | state | total_spent |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1001 | John Smith | john.smith@gmail.com | 2023-01-15 | 555-123-4567 | NY | 120.50 |
| 1002 | Sarah Connor | sconnor@yahoo.com | 2023-01-22 | 555-987-6543 | CA | 450.00 |
| 1004 | Emily Davis | emily.davis@gmail.com | 2023-02-14 | 555-222-3333 | TX | 89.99 |

## How to Run
```bash
pip install pandas
python clean_data.py
