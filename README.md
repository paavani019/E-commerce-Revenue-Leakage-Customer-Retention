## E-commerce Revenue Leakage & Customer Retention Analysis

### Project title
**E-commerce Revenue Leakage & Customer Retention Analysis**

### Why this exists (business problem with financial impact)
This project is designed like a real e-commerce performance investigation, not a “dashboard build.”

**Problem framing**: revenue is leaking through hidden inefficiencies across:
- **Customer behavior**: repeat activity that is operationally expensive but low value, plus high-risk churn pockets that threaten future revenue.
- **Retention dynamics**: a small portion of customers often funds a disproportionate share of revenue; losing them creates an immediate top-line hole.
- **Product economics**: categories with low sales contribution but high shipping pressure can quietly compress margin and distort growth decisions.

**Financial implication (what’s at stake)**:
- Preventable churn is a direct loss of *future* revenue (CLV).
- Serving low-value high-frequency demand is a margin leak (cost-to-serve).
- Shipping-heavy categories can create margin pressure that doesn’t show up if you only watch gross revenue.

### Dataset (real transactions)
This project uses the **Olist Brazilian e-commerce dataset** (public, real transaction logs) contained in `archive.zip` and extracted to `data/raw/`.

Core transaction tables used:
- **`olist_orders_dataset.csv`**: order lifecycle & timestamps (purchase → delivery)
- **`olist_order_payments_dataset.csv`**: actual paid value by order (used as revenue)
- **`olist_order_items_dataset.csv`**: item price + freight (used for product/shipping economics)
- **`olist_customers_dataset.csv`**: `customer_unique_id` ties repeat purchases across orders
- **`olist_order_reviews_dataset.csv`**: review score as friction/satisfaction signal
- **`olist_products_dataset.csv`** + **translation**: product category mapping for product performance

### Data understanding (columns → business meaning)
Key fields used in the analysis and why they matter:
- **`order_id`**: the atomic unit for orders, payments, and fulfillment outcomes.
- **`customer_unique_id`**: customer identity across multiple orders (required for retention, CLV, and churn logic).
- **`order_status`**: revenue recognition gate; this project treats **delivered** orders as realized revenue.
- **`order_purchase_timestamp`**: the time anchor for cohorts, RFM recency, and seasonality.
- **`payment_value`**: paid amount (revenue proxy that includes real checkout totals).
- **`price`** / **`freight_value`**: item value vs shipping pressure (shipping-heavy categories are margin-risk).
- **`review_score`**: customer experience friction signal (retention risk indicator).
- **`product_category_name`** (translated): category performance rollups for inventory/pricing actions.

### Data cleaning (business-driven)
Cleaning is not “because it’s standard”—each step prevents a financial misread:
- **Deduplicated keys**:
  - Orders deduped on `order_id` (prevents double-counted revenue and inflated order volume).
  - Order items deduped on (`order_id`, `order_item_id`) (prevents inflated units and GMV).
  - Payments deduped on (`order_id`, `payment_sequential`) (prevents overstatement of paid revenue).
- **Datetime parsing**:
  - Enforces valid timestamps (without this, cohort retention and churn windows become incorrect).
- **Missing values handling**:
  - Missing delivery timestamps are preserved (they’re operational signals, not noise).
  - Missing reviews are left as missing (silence ≠ satisfaction).
- **Outlier flagging (99.9th percentile)**:
  - Extreme `price`, `freight_value`, and `payment_value` rows are flagged for review because they can dominate leakage estimates and misprioritize categories.

### KPIs computed (business definitions)
- **Revenue**: sum of `payment_value` for **delivered** orders (paid revenue actually recognized)
- **Average Order Value (AOV)**: revenue / delivered orders
- **Revenue per Customer**: revenue / active customers (delivered)
- **Retention rate**: cohort retention by first purchase month (repeat activity over time)
- **Churn proxy**: inactive for ≥ 90 days as of dataset end date
- **Customer Lifetime Value (estimated)**: median revenue-per-customer-per-month × expected active months (from retention curve)

### Advanced analysis (what makes it portfolio-level)
- **Revenue leakage detection**
  - Low-value high-frequency customers (cost-to-serve leakage)
  - High churn-risk revenue exposure (concentration risk)
  - Underperforming categories (low GMV + high freight pressure)
- **Customer segmentation**
  - RFM segmentation with action-oriented segment labels
  - Behavioral segmentation (payment preference + installments)
- **Churn risk modeling (rule-based)**
  - Transparent rules: inactivity + friction signals (satisfaction, ops friction, price sensitivity)
- **Time analysis**
  - Monthly revenue trends
  - Seasonality by month-of-year

### Outputs
After running, you get:
- **Executive memo**: `reports/insights.md` (quantified, decision-ready)
- **Charts**: `reports/figures/*.png`
- **Processed tables**: `data/processed/*.parquet`

### Tech stack & workflow (what you’ll showcase on a CV)
- **Python**: pandas, numpy, matplotlib/seaborn
- **Analytics engineering**: modular pipeline (`src/`) with reproducible outputs
- **Business analytics**: KPI design, RFM segmentation, churn-risk rules, sensitivity analysis, ROI/unit economics
- **Reporting**: executive-ready memo + charts exported to disk

### How to run
From the project root:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python scripts/unpack_data.py
python main.py
```

On Windows PowerShell (recommended):

```powershell
.\run.ps1 -Task setup
.\run.ps1 -Task run
```

### What to read first
- `reports/insights.md` (the “what changed in the business” narrative)
- `reports/figures/01_monthly_revenue.png` (trend + volatility)
- `reports/figures/02_rfm_segments.png` (who drives revenue)
- `reports/figures/03_churn_risk.png` (where revenue is at risk)

