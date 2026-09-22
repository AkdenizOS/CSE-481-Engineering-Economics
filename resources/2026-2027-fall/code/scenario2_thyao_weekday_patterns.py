# ============================================================
# CSE-481 Engineering Economics
# Scenario 2 — Weekday and Multi-Day Patterns
#
# Extended version:
# - Detailed English explanations in PRINT output
# - Runs THREE analyses for THYAO.IS:
#     1) Full period from 2020-01-01
#     2) Last 2 years
#     3) Last 1 year
#
# Educational use only.
# ============================================================

# If needed:
# pip install yfinance pandas numpy matplotlib python-dateutil

import warnings
warnings.filterwarnings("ignore")

from dateutil.relativedelta import relativedelta

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf


# ------------------------------------------------------------
# 1. SETTINGS
# ------------------------------------------------------------

TICKER = "THYAO.IS"
FULL_START_DATE = "2020-01-01"
END_DATE = None

TRANSACTION_COST = 0.001   # 0.10%
TRAIN_RATIO = 0.70


# ------------------------------------------------------------
# 2. PRINT HELPERS
# ------------------------------------------------------------

def print_section(title):
    print("\n" + "=" * 90)
    print(title)
    print("=" * 90)


def print_detailed_explanations():
    print_section("DETAILED METRIC EXPLANATIONS")

    print("""
Positive_Rate:
Shows the percentage of observations in which the return for that weekday was positive.

Example:
Monday Positive_Rate = 51.6%

This means approximately 51.6% of observed Mondays had a positive daily return.

Important:
Positive_Rate measures FREQUENCY, not MAGNITUDE.
A high Positive_Rate does not automatically imply a high average return.
Positive days may be small while negative days may be large.
""")

    print("""
Average Return and Standard Deviation:
Suppose Wednesday has a negative average return and Thursday has a positive average return.
We should NOT conclude that THYAO always falls on Wednesday and rises on Thursday.

If daily standard deviation is around 2-3%, actual day-to-day movements can be much larger
than the average weekday effect.

Example:
Thursday average return = +0.47%

But individual Thursday returns may look like:
+4.2%, -2.8%, +1.1%, -3.0%, +3.7%

Conclusion:
Average behavior is not a deterministic rule.
""")

    print("""
Average Thu-Fri return after pattern (%):
Measures the average compounded return of Thursday and Friday after the target pattern appears.

Target pattern:
Mon < 0
Tue < 0
Wed < 0
Thu > 0
Fri > 0

The compounded Thu-Fri return is calculated as:
(1 + Thu_Return) * (1 + Fri_Return) - 1

Example:
Thu = +3%
Fri = +2%

Combined return:
(1.03 * 1.02) - 1 = +5.06%

This metric answers:
'On average, how much did the stock move during Thursday and Friday after this pattern appeared?'
""")

    print("""
Median Thu-Fri return after pattern (%):
The median is the middle Thu-Fri return after sorting all observed pattern returns.

Example:
+1%, +2%, +3%, +4%, +20%

Average = +6%
Median  = +3%

The +20% observation strongly increases the average.
The median is less sensitive to such extreme observations.

Therefore, Average and Median should be interpreted together.
If they are close, the result is less likely to be driven by only a few extreme outcomes.
""")

    print("""
Positive Thu-Fri rate (%):
Shows how often the combined Thursday-Friday return was positive after the target pattern.

Example:
10 pattern events
8 positive outcomes
2 negative outcomes

Positive Thu-Fri Rate = 8 / 10 = 80%

Important:
1 / 1 = 100%
100 / 100 = 100%

Both are mathematically 100%, but they do NOT provide the same statistical evidence.
Always interpret Positive Rate together with Event Count.
""")

    print("""
Average after transaction cost (%):
The average pattern return after subtracting an assumed transaction cost.

Example:
Average Thu-Fri Return = +5.72%
Transaction Cost       =  0.10%
Net Average Return     = +5.62%

Transaction cost may represent:
- brokerage commissions,
- bid-ask spread,
- fees,
- slippage.

A strategy may look profitable before costs but lose much of its advantage after costs.
""")

    print("""
ISO_Year and ISO_Week:
These fields are used to group dates into standardized calendar weeks.

Example:
ISO_Year = 2024
ISO_Week = 16

This means ISO week 16 of the year 2024.

The purpose is to group Monday through Friday into the same weekly observation
so that the weekday pattern can be evaluated week by week.

ISO week numbering is especially useful around year-end and year-start boundaries.
""")

    print("""
Out-of-sample interpretation:
Suppose the target pattern appears only once in the out-of-sample period.

If that one event is positive:
Positive Rate = 100%

However, this is weak evidence because it is based on only one observation.

Correct interpretation:
'Interesting observation, but insufficient out-of-sample evidence for a strong conclusion.'
""")

    print("""
Why should we be careful?
A visible weekday pattern may appear purely by chance.

If we test many possible combinations, some may look successful because of randomness.
This is related to data snooping and multiple-testing bias.

Therefore, the pattern should be tested:
- across longer periods,
- across multiple stocks,
- across different market regimes,
- and after transaction costs.

A robust pattern should ideally survive bull markets, bear markets,
high-volatility periods, low-volatility periods, and different interest-rate environments.
""")


# ------------------------------------------------------------
# 3. DOWNLOAD DATA
# ------------------------------------------------------------

def load_stock_data(ticker, start, end=None):
    df = yf.download(
        ticker,
        start=start,
        end=end,
        auto_adjust=True,
        progress=False
    )

    if df.empty:
        raise ValueError(f"No data found for {ticker}")

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df = df.copy()
    df.index = pd.to_datetime(df.index)

    df["Return"] = df["Close"].pct_change()

    df["WeekdayNum"] = df.index.dayofweek
    df["Weekday"] = df["WeekdayNum"].map({
        0: "Mon",
        1: "Tue",
        2: "Wed",
        3: "Thu",
        4: "Fri"
    })

    iso = df.index.isocalendar()
    df["ISO_Year"] = iso.year.astype(int)
    df["ISO_Week"] = iso.week.astype(int)

    return df.dropna(subset=["Return"])


# ------------------------------------------------------------
# 4. WEEKDAY STATISTICS
# ------------------------------------------------------------

def weekday_statistics(df):
    stats = (
        df.groupby("Weekday")["Return"]
        .agg(
            Observations="count",
            Average_Return="mean",
            Median_Return="median",
            Std_Dev="std",
            Positive_Rate=lambda x: (x > 0).mean()
        )
    )

    stats = stats.reindex(["Mon", "Tue", "Wed", "Thu", "Fri"])

    for col in ["Average_Return", "Median_Return", "Std_Dev", "Positive_Rate"]:
        stats[col] *= 100

    return stats


# ------------------------------------------------------------
# 5. BUILD WEEKLY TABLE
# ------------------------------------------------------------

def build_weekly_pattern_table(df):
    weekly = (
        df.pivot_table(
            index=["ISO_Year", "ISO_Week"],
            columns="Weekday",
            values="Return",
            aggfunc="first"
        )
        .reset_index()
    )

    for day in ["Mon", "Tue", "Wed", "Thu", "Fri"]:
        if day not in weekly.columns:
            weekly[day] = np.nan

    return weekly[
        ["ISO_Year", "ISO_Week", "Mon", "Tue", "Wed", "Thu", "Fri"]
    ]


# ------------------------------------------------------------
# 6. DETECT TARGET PATTERN
# ------------------------------------------------------------

def detect_pattern(weekly):
    weekly = weekly.copy()

    weekly["Complete_Week"] = weekly[
        ["Mon", "Tue", "Wed", "Thu", "Fri"]
    ].notna().all(axis=1)

    weekly["Pattern"] = (
        weekly["Complete_Week"]
        & (weekly["Mon"] < 0)
        & (weekly["Tue"] < 0)
        & (weekly["Wed"] < 0)
        & (weekly["Thu"] > 0)
        & (weekly["Fri"] > 0)
    )

    weekly["Weekly_Return"] = (
        (1 + weekly["Mon"])
        * (1 + weekly["Tue"])
        * (1 + weekly["Wed"])
        * (1 + weekly["Thu"])
        * (1 + weekly["Fri"])
        - 1
    )

    weekly["Thu_Fri_Return"] = (
        (1 + weekly["Thu"])
        * (1 + weekly["Fri"])
        - 1
    )

    return weekly


# ------------------------------------------------------------
# 7. PATTERN SUMMARY
# ------------------------------------------------------------

def pattern_summary(weekly, transaction_cost=0.001):
    complete = weekly[weekly["Complete_Week"]].copy()
    patterns = complete[complete["Pattern"]].copy()

    total_complete_weeks = len(complete)
    pattern_count = len(patterns)

    frequency = (
        pattern_count / total_complete_weeks
        if total_complete_weeks > 0
        else np.nan
    )

    if pattern_count > 0:
        avg_thu_fri = patterns["Thu_Fri_Return"].mean()
        median_thu_fri = patterns["Thu_Fri_Return"].median()
        positive_rate = (patterns["Thu_Fri_Return"] > 0).mean()
        avg_after_cost = avg_thu_fri - transaction_cost
    else:
        avg_thu_fri = np.nan
        median_thu_fri = np.nan
        positive_rate = np.nan
        avg_after_cost = np.nan

    return pd.Series({
        "Complete weeks": total_complete_weeks,
        "Pattern occurrences": pattern_count,
        "Pattern frequency (%)": frequency * 100,
        "Average Thu-Fri return after pattern (%)": avg_thu_fri * 100,
        "Median Thu-Fri return after pattern (%)": median_thu_fri * 100,
        "Positive Thu-Fri rate (%)": positive_rate * 100,
        "Average after transaction cost (%)": avg_after_cost * 100,
    })


# ------------------------------------------------------------
# 8. TIME-BASED TRAIN / TEST SPLIT
# ------------------------------------------------------------

def train_test_split_by_time(df, train_ratio=0.70):
    split_index = int(len(df) * train_ratio)

    train = df.iloc[:split_index].copy()
    test = df.iloc[split_index:].copy()

    return train, test


# ------------------------------------------------------------
# 9. VISUALIZATION
# ------------------------------------------------------------

def plot_weekday_average_returns(stats, ticker, label):
    values = stats["Average_Return"]

    plt.figure(figsize=(9, 5))
    plt.bar(values.index, values.values)
    plt.axhline(0, linewidth=1)

    plt.title(f"{ticker} — Average Daily Return by Weekday ({label})")
    plt.xlabel("Weekday")
    plt.ylabel("Average Return (%)")
    plt.tight_layout()
    plt.show()


# ------------------------------------------------------------
# 10. RUN ONE ANALYSIS WINDOW
# ------------------------------------------------------------

def run_single_analysis(ticker, start_date, end_date, label, show_plot=True):
    print_section(f"{ticker} — {label}")

    df = load_stock_data(
        ticker=ticker,
        start=start_date,
        end=end_date
    )

    print(f"Data period: {df.index.min().date()} -> {df.index.max().date()}")
    print(f"Daily observations: {len(df)}")

    # Weekday statistics
    stats = weekday_statistics(df)

    print("\nWEEKDAY STATISTICS")
    print(stats.round(3))

    print("\nInterpretation:")
    print("- Positive_Rate = percentage of observations with a positive daily return.")
    print("- Average_Return = mean daily return for that weekday.")
    print("- Median_Return = middle daily return for that weekday.")
    print("- Std_Dev = variability of daily returns around the average.")
    print("- A positive weekday average is NOT a deterministic rule.")
    print("- If Std_Dev is much larger than Average_Return, daily outcomes vary widely.")

    # Weekly pattern
    weekly = detect_pattern(
        build_weekly_pattern_table(df)
    )

    summary = pattern_summary(
        weekly,
        transaction_cost=TRANSACTION_COST
    )

    print("\nTARGET PATTERN")
    print("Mon < 0, Tue < 0, Wed < 0, Thu > 0, Fri > 0")

    print("\nPATTERN SUMMARY")
    print(summary.round(3))

    print("\nMETRIC INTERPRETATION")
    print(
        f"Average Thu-Fri return after pattern: "
        f"{summary['Average Thu-Fri return after pattern (%)']:.3f}%"
    )
    print(
        "Meaning: average compounded return of Thursday and Friday "
        "after the target pattern."
    )

    print(
        f"\nMedian Thu-Fri return after pattern: "
        f"{summary['Median Thu-Fri return after pattern (%)']:.3f}%"
    )
    print(
        "Meaning: middle Thu-Fri result after sorting all event returns. "
        "It is less sensitive to outliers."
    )

    print(
        f"\nPositive Thu-Fri rate: "
        f"{summary['Positive Thu-Fri rate (%)']:.3f}%"
    )
    print(
        "Meaning: percentage of detected pattern events where the combined "
        "Thursday-Friday return was positive."
    )

    print(
        f"\nAverage after transaction cost: "
        f"{summary['Average after transaction cost (%)']:.3f}%"
    )
    print(
        "Meaning: average Thu-Fri return after subtracting the assumed "
        f"{TRANSACTION_COST * 100:.2f}% transaction cost."
    )

    # Matching weeks
    pattern_weeks = weekly[weekly["Pattern"]].copy()

    if not pattern_weeks.empty:
        display_cols = [
            "ISO_Year",
            "ISO_Week",
            "Mon",
            "Tue",
            "Wed",
            "Thu",
            "Fri",
            "Thu_Fri_Return",
            "Weekly_Return"
        ]

        display_table = pattern_weeks[display_cols].copy()

        for col in [
            "Mon", "Tue", "Wed", "Thu", "Fri",
            "Thu_Fri_Return", "Weekly_Return"
        ]:
            display_table[col] *= 100

        print("\nMATCHING WEEKS (%)")
        print(display_table.round(2))

        print("\nISO_Year / ISO_Week explanation:")
        print(
            "ISO_Year and ISO_Week identify the standardized calendar week "
            "used to group Monday through Friday into the same weekly observation."
        )
    else:
        print("\nNo matching complete weeks were found.")

    # Out-of-sample test
    train_df, test_df = train_test_split_by_time(
        df,
        train_ratio=TRAIN_RATIO
    )

    train_weekly = detect_pattern(
        build_weekly_pattern_table(train_df)
    )

    test_weekly = detect_pattern(
        build_weekly_pattern_table(test_df)
    )

    train_summary = pattern_summary(
        train_weekly,
        transaction_cost=TRANSACTION_COST
    )

    test_summary = pattern_summary(
        test_weekly,
        transaction_cost=TRANSACTION_COST
    )

    comparison = pd.DataFrame({
        "In-Sample": train_summary,
        "Out-of-Sample": test_summary
    })

    print("\nIN-SAMPLE VS OUT-OF-SAMPLE")
    print(comparison.round(3))

    test_occurrences = int(test_summary["Pattern occurrences"])
    test_return = test_summary[
        "Average Thu-Fri return after pattern (%)"
    ]

    print("\nOUT-OF-SAMPLE INTERPRETATION")

    if test_occurrences == 0:
        print(
            "The target pattern did not appear in the out-of-sample period."
        )
        print(
            "There is not enough unseen evidence to support a strong conclusion."
        )

    elif test_occurrences == 1:
        print(
            "The target pattern appeared once in the out-of-sample period."
        )
        print(
            f"Average Thu-Fri return after the pattern: {test_return:.3f}%"
        )
        print(
            "Important: this result is based on only one observation."
        )
        print(
            "Even if the Positive Thu-Fri Rate is 100%, the statistical evidence is weak."
        )

    else:
        print(
            f"The target pattern appeared {test_occurrences} times "
            "in the out-of-sample period."
        )
        print(
            f"Average Thu-Fri return after the pattern: {test_return:.3f}%"
        )

    print("\nIMPORTANT WARNING")
    print(
        "A visible weekday pattern may be caused by chance."
    )
    print(
        "It should be tested across longer periods, multiple stocks, "
        "different market regimes and after transaction costs."
    )
    print(
        "If the pattern is strong in-sample but weak out-of-sample, "
        "it may be overfit or regime-dependent."
    )

    if show_plot:
        plot_weekday_average_returns(
            stats,
            ticker,
            label
        )

    return {
        "data": df,
        "weekday_stats": stats,
        "weekly_table": weekly,
        "summary": summary,
        "in_sample_summary": train_summary,
        "out_of_sample_summary": test_summary
    }


# ------------------------------------------------------------
# 11. RUN THREE ANALYSES
# ------------------------------------------------------------

def run_three_analyses():
    print_section("SCENARIO 2 — WEEKDAY AND MULTI-DAY PATTERNS")
    print(f"Ticker: {TICKER}")

    print_detailed_explanations()

    today = pd.Timestamp.today().normalize()

    last_2y_start = (
        today - relativedelta(years=2)
    ).strftime("%Y-%m-%d")

    last_1y_start = (
        today - relativedelta(years=1)
    ).strftime("%Y-%m-%d")

    # 1) Full period
    full_results = run_single_analysis(
        ticker=TICKER,
        start_date=FULL_START_DATE,
        end_date=END_DATE,
        label="FULL PERIOD — FROM 2020",
        show_plot=True
    )

    # 2) Last 2 years
    two_year_results = run_single_analysis(
        ticker=TICKER,
        start_date=last_2y_start,
        end_date=END_DATE,
        label="LAST 2 YEARS",
        show_plot=True
    )

    # 3) Last 1 year
    one_year_results = run_single_analysis(
        ticker=TICKER,
        start_date=last_1y_start,
        end_date=END_DATE,
        label="LAST 1 YEAR",
        show_plot=True
    )

    # Final comparison
    print_section(
        "FINAL COMPARISON — FULL PERIOD vs LAST 2 YEARS vs LAST 1 YEAR"
    )

    comparison = pd.DataFrame({
        "Full Period": full_results["summary"],
        "Last 2 Years": two_year_results["summary"],
        "Last 1 Year": one_year_results["summary"]
    })

    print(comparison.round(3))

    print("\nFINAL INTERPRETATION")
    print(
        "The same pattern may behave differently across different time windows."
    )
    print(
        "Full-period performance alone is not sufficient."
    )
    print(
        "The last 2 years and last 1 year help us see whether the pattern "
        "still exists under more recent market conditions."
    )
    print(
        "If the pattern is strong over the full period but weak in the last year, "
        "it may be regime-dependent rather than robust."
    )

    return {
        "full_period": full_results,
        "last_2_years": two_year_results,
        "last_1_year": one_year_results,
        "comparison": comparison
    }


# ------------------------------------------------------------
# 12. RUN
# ------------------------------------------------------------

if __name__ == "__main__":
    results = run_three_analyses()
