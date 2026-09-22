# ============================================================
# CSE-481 Engineering Economics
# Scenario 3 — Technical Reversal Events
#
# Extended English teaching version:
# - Downloads ASELS.IS daily OHLCV data
# - Calculates Bollinger Bands, RSI, KAMA, Supertrend, Ichimoku, Volume
# - Detects several technical reversal events
# - Measures 5-day forward returns
# - Prints detailed English explanations together with calculated values
#
# Educational use only.
# ============================================================

# If needed:
# pip install yfinance pandas numpy matplotlib

import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf


# ------------------------------------------------------------
# 1. SETTINGS
# ------------------------------------------------------------

TICKER = "ASELS.IS"
START_DATE = "2020-01-01"
END_DATE = None

FORWARD_DAYS = 5
SUCCESS_THRESHOLD = 0.0


# ------------------------------------------------------------
# 2. HELPERS
# ------------------------------------------------------------

def print_section(title):
    print("\n" + "=" * 90)
    print(title)
    print("=" * 90)


def print_metric_definition(name, value, explanation):
    print(f"\n{name}: {value}")
    print(explanation)


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

    needed = ["Open", "High", "Low", "Close", "Volume"]
    df = df[needed].dropna()

    return df


# ------------------------------------------------------------
# 4. BOLLINGER BANDS
# ------------------------------------------------------------

def add_bollinger_bands(df, window=20, num_std=2):
    df = df.copy()

    df["BB_Middle"] = df["Close"].rolling(window).mean()
    std = df["Close"].rolling(window).std()

    df["BB_Upper"] = df["BB_Middle"] + num_std * std
    df["BB_Lower"] = df["BB_Middle"] - num_std * std

    return df


# ------------------------------------------------------------
# 5. RSI
# ------------------------------------------------------------

def add_rsi(df, period=14):
    df = df.copy()

    delta = df["Close"].diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.ewm(
        alpha=1 / period,
        adjust=False
    ).mean()

    avg_loss = loss.ewm(
        alpha=1 / period,
        adjust=False
    ).mean()

    rs = avg_gain / avg_loss.replace(0, np.nan)

    df["RSI"] = 100 - (100 / (1 + rs))

    return df


# ------------------------------------------------------------
# 6. KAMA
# ------------------------------------------------------------

def add_kama(df, er_period=10, fast=2, slow=30):
    df = df.copy()

    close = df["Close"]

    change = (close - close.shift(er_period)).abs()
    volatility = close.diff().abs().rolling(er_period).sum()

    er = change / volatility.replace(0, np.nan)

    fast_sc = 2 / (fast + 1)
    slow_sc = 2 / (slow + 1)

    smoothing_constant = (
        er * (fast_sc - slow_sc) + slow_sc
    ) ** 2

    kama = pd.Series(index=df.index, dtype=float)

    if len(df) > er_period:
        kama.iloc[er_period] = close.iloc[er_period]

        for i in range(er_period + 1, len(df)):
            prev_kama = kama.iloc[i - 1]

            if pd.isna(prev_kama):
                prev_kama = close.iloc[i - 1]

            sc = smoothing_constant.iloc[i]

            if pd.isna(sc):
                kama.iloc[i] = prev_kama
            else:
                kama.iloc[i] = (
                    prev_kama
                    + sc * (close.iloc[i] - prev_kama)
                )

    df["KAMA"] = kama
    df["KAMA_Slope"] = df["KAMA"].diff()

    return df


# ------------------------------------------------------------
# 7. ATR
# ------------------------------------------------------------

def add_atr(df, period=10):
    df = df.copy()

    high_low = df["High"] - df["Low"]
    high_prev_close = (
        df["High"] - df["Close"].shift(1)
    ).abs()

    low_prev_close = (
        df["Low"] - df["Close"].shift(1)
    ).abs()

    tr = pd.concat(
        [high_low, high_prev_close, low_prev_close],
        axis=1
    ).max(axis=1)

    df["ATR"] = tr.rolling(period).mean()

    return df


# ------------------------------------------------------------
# 8. SUPERTREND
# ------------------------------------------------------------

def add_supertrend(df, period=10, multiplier=3.0):
    df = add_atr(df, period=period)

    hl2 = (df["High"] + df["Low"]) / 2

    basic_upper = hl2 + multiplier * df["ATR"]
    basic_lower = hl2 - multiplier * df["ATR"]

    final_upper = pd.Series(index=df.index, dtype=float)
    final_lower = pd.Series(index=df.index, dtype=float)
    supertrend = pd.Series(index=df.index, dtype=float)
    direction = pd.Series(index=df.index, dtype=float)

    for i in range(len(df)):
        if i == 0:
            final_upper.iloc[i] = basic_upper.iloc[i]
            final_lower.iloc[i] = basic_lower.iloc[i]
            supertrend.iloc[i] = np.nan
            direction.iloc[i] = 0
            continue

        if (
            basic_upper.iloc[i] < final_upper.iloc[i - 1]
            or df["Close"].iloc[i - 1] > final_upper.iloc[i - 1]
        ):
            final_upper.iloc[i] = basic_upper.iloc[i]
        else:
            final_upper.iloc[i] = final_upper.iloc[i - 1]

        if (
            basic_lower.iloc[i] > final_lower.iloc[i - 1]
            or df["Close"].iloc[i - 1] < final_lower.iloc[i - 1]
        ):
            final_lower.iloc[i] = basic_lower.iloc[i]
        else:
            final_lower.iloc[i] = final_lower.iloc[i - 1]

        prev_supertrend = supertrend.iloc[i - 1]

        if pd.isna(prev_supertrend):
            supertrend.iloc[i] = final_lower.iloc[i]
            direction.iloc[i] = 1
            continue

        if prev_supertrend == final_upper.iloc[i - 1]:
            if df["Close"].iloc[i] <= final_upper.iloc[i]:
                supertrend.iloc[i] = final_upper.iloc[i]
                direction.iloc[i] = -1
            else:
                supertrend.iloc[i] = final_lower.iloc[i]
                direction.iloc[i] = 1
        else:
            if df["Close"].iloc[i] >= final_lower.iloc[i]:
                supertrend.iloc[i] = final_lower.iloc[i]
                direction.iloc[i] = 1
            else:
                supertrend.iloc[i] = final_upper.iloc[i]
                direction.iloc[i] = -1

    df["Supertrend"] = supertrend
    df["Supertrend_Direction"] = direction

    df["Supertrend_Bullish_Flip"] = (
        (df["Supertrend_Direction"].shift(1) == -1)
        & (df["Supertrend_Direction"] == 1)
    )

    return df


# ------------------------------------------------------------
# 9. ICHIMOKU CLOUD
# ------------------------------------------------------------

def add_ichimoku(df):
    df = df.copy()

    high_9 = df["High"].rolling(9).max()
    low_9 = df["Low"].rolling(9).min()
    df["Tenkan"] = (high_9 + low_9) / 2

    high_26 = df["High"].rolling(26).max()
    low_26 = df["Low"].rolling(26).min()
    df["Kijun"] = (high_26 + low_26) / 2

    span_a_raw = (df["Tenkan"] + df["Kijun"]) / 2
    df["Senkou_A"] = span_a_raw.shift(26)

    high_52 = df["High"].rolling(52).max()
    low_52 = df["Low"].rolling(52).min()
    span_b_raw = (high_52 + low_52) / 2
    df["Senkou_B"] = span_b_raw.shift(26)

    df["Cloud_Top"] = df[
        ["Senkou_A", "Senkou_B"]
    ].max(axis=1)

    df["Cloud_Bottom"] = df[
        ["Senkou_A", "Senkou_B"]
    ].min(axis=1)

    df["Ichimoku_Bullish_Breakout"] = (
        (df["Close"].shift(1) <= df["Cloud_Top"].shift(1))
        & (df["Close"] > df["Cloud_Top"])
    )

    return df


# ------------------------------------------------------------
# 10. VOLUME FEATURES
# ------------------------------------------------------------

def add_volume_features(df, window=20):
    df = df.copy()

    df["Volume_MA"] = df["Volume"].rolling(window).mean()
    df["Volume_Rise"] = df["Volume"] > df["Volume_MA"]

    return df


# ------------------------------------------------------------
# 11. FORWARD RETURNS
# ------------------------------------------------------------

def add_forward_returns(df, forward_days=5):
    df = df.copy()

    df[f"Forward_{forward_days}D_Return"] = (
        df["Close"].shift(-forward_days) / df["Close"] - 1
    )

    return df


# ------------------------------------------------------------
# 12. DETECT REVERSAL EVENTS
# ------------------------------------------------------------

def detect_reversal_events(df):
    df = df.copy()

    # Bollinger reversal:
    # Yesterday closed at/below lower band,
    # today closes back above lower band.
    df["Bollinger_Reversal"] = (
        (df["Close"].shift(1) <= df["BB_Lower"].shift(1))
        & (df["Close"] > df["BB_Lower"])
    )

    # RSI local trough:
    # Yesterday's RSI is lower than both the day before and today,
    # and the trough value is below 40.
    df["RSI_Local_Trough"] = (
        (df["RSI"].shift(1) < df["RSI"].shift(2))
        & (df["RSI"].shift(1) < df["RSI"])
        & (df["RSI"].shift(1) < 40)
    )

    # RSI trough with volume confirmation.
    df["RSI_Trough_Volume"] = (
        df["RSI_Local_Trough"]
        & df["Volume_Rise"]
    )

    # KAMA bullish turn:
    # slope changes from flat/negative to positive.
    df["KAMA_Bullish_Turn"] = (
        (df["KAMA_Slope"].shift(1) <= 0)
        & (df["KAMA_Slope"] > 0)
    )

    # Broad trend reversal event.
    df["Trend_Reversal_Event"] = (
        df["Supertrend_Bullish_Flip"]
        | df["Ichimoku_Bullish_Breakout"]
        | df["KAMA_Bullish_Turn"]
    )

    # Strong combined event.
    df["Strong_Reversal_Event"] = (
        df["Bollinger_Reversal"]
        & df["RSI_Local_Trough"]
        & df["Volume_Rise"]
        & df["Trend_Reversal_Event"]
    )

    return df


# ------------------------------------------------------------
# 13. EVENT SUMMARY
# ------------------------------------------------------------

def event_summary(
    df,
    event_column,
    forward_return_column,
    threshold=0.0
):
    events = df[df[event_column] == True].copy()
    events = events.dropna(
        subset=[forward_return_column]
    )

    count = len(events)

    if count == 0:
        return pd.Series({
            "Event_Count": 0,
            "Successful_Events": 0,
            "Success_Rate_%": np.nan,
            "Average_Forward_Return_%": np.nan,
            "Median_Forward_Return_%": np.nan
        })

    successful = (
        events[forward_return_column] > threshold
    ).sum()

    success_rate = successful / count

    return pd.Series({
        "Event_Count": count,
        "Successful_Events": successful,
        "Success_Rate_%": success_rate * 100,
        "Average_Forward_Return_%":
            events[forward_return_column].mean() * 100,
        "Median_Forward_Return_%":
            events[forward_return_column].median() * 100
    })


def build_event_comparison(df, forward_days=5):
    fwd_col = f"Forward_{forward_days}D_Return"

    events = {
        "Bollinger Reversal":
            "Bollinger_Reversal",

        "RSI Local Trough":
            "RSI_Local_Trough",

        "RSI Trough + Volume":
            "RSI_Trough_Volume",

        "KAMA Bullish Turn":
            "KAMA_Bullish_Turn",

        "Supertrend Bullish Flip":
            "Supertrend_Bullish_Flip",

        "Ichimoku Bullish Breakout":
            "Ichimoku_Bullish_Breakout",

        "Trend Reversal Event":
            "Trend_Reversal_Event",

        "Strong Combined Reversal":
            "Strong_Reversal_Event"
    }

    rows = []

    for label, column in events.items():
        summary = event_summary(
            df,
            event_column=column,
            forward_return_column=fwd_col,
            threshold=SUCCESS_THRESHOLD
        )

        summary.name = label
        rows.append(summary)

    return pd.DataFrame(rows)


# ------------------------------------------------------------
# 14. DETAILED ENGLISH EXPLANATIONS
# ------------------------------------------------------------

def explain_event_table(comparison):
    print_section("HOW TO READ THE REVERSAL EVENT SUMMARY")

    print("""
Event_Count:
Number of times the technical event was detected in the historical sample.

Example:
If Bollinger Reversal Event_Count = 31,
the system found 31 historical Bollinger reversal events.

A larger event count usually provides more evidence than a very small sample.
For example, 2 events and 100 events should not be treated as equally reliable.
""")

    print("""
Successful_Events:
Number of detected events for which the forward return was positive.

With FORWARD_DAYS = 5:
an event is counted as successful when the stock price is higher 5 trading days later.
""")

    print("""
Success_Rate_%:
Successful_Events / Event_Count * 100

Example:
20 successful events out of 31 total events:

20 / 31 = 64.52%

Important:
Success Rate measures frequency, not the size of the price move.
A +0.1% return and a +10% return are both counted as 'successful'.
""")

    print("""
Average_Forward_Return_%:
Average percentage return from the event date to 5 trading days later.

Example:
If Bollinger Reversal Average_Forward_Return_% = 2.11%,
the mean 5-day return after all detected Bollinger reversal events was +2.11%.

This measures magnitude, not only success/failure.
""")

    print("""
Median_Forward_Return_%:
The middle 5-day forward return after sorting all event outcomes.

Median is less sensitive to extreme positive or negative observations than Average.

If Average = +2.11% but Median = +0.58%,
some large positive outcomes may be pulling the average upward.
""")

    print("\nCALCULATED VALUES FROM THIS RUN")
    print("-" * 90)

    for event_name, row in comparison.iterrows():
        print(f"\n{event_name}")
        print(f"  Event Count              : {int(row['Event_Count'])}")
        print(f"  Successful Events        : {int(row['Successful_Events'])}")

        if pd.isna(row["Success_Rate_%"]):
            print("  Success Rate             : N/A")
            print("  Average Forward Return   : N/A")
            print("  Median Forward Return    : N/A")
        else:
            print(f"  Success Rate             : {row['Success_Rate_%']:.2f}%")
            print(f"  Average Forward Return   : {row['Average_Forward_Return_%']:.2f}%")
            print(f"  Median Forward Return    : {row['Median_Forward_Return_%']:.2f}%")

        if row["Event_Count"] < 5:
            print("  Evidence Warning         : Very small sample size.")
        elif row["Event_Count"] < 20:
            print("  Evidence Warning         : Limited sample size.")
        else:
            print("  Evidence Note            : Larger historical sample, but still requires validation.")


def explain_rsi_local_trough(df):
    print_section("RSI LOCAL TROUGH — DETAILED EXPLANATION")

    troughs = df[df["RSI_Local_Trough"]].copy()

    print("""
RSI < 30 and RSI Local Trough are NOT the same concept.

RSI < 30:
A level condition. It asks:
'Is RSI currently below 30?'

RSI Local Trough:
A shape/event condition. It asks:
'Did RSI form a local low and start turning upward?'

The code detects a local trough when:
RSI[t-1] < RSI[t-2]
AND
RSI[t-1] < RSI[t]
AND
RSI[t-1] < 40

Example:
Day 1 RSI = 45
Day 2 RSI = 37   <- local trough
Day 3 RSI = 42

The dots on the RSI chart are NOT automatic BUY signals.
They are historical reversal events that we test statistically.
""")

    print(f"Detected RSI Local Trough events: {len(troughs)}")

    if not troughs.empty:
        fwd_col = f"Forward_{FORWARD_DAYS}D_Return"
        valid = troughs.dropna(subset=[fwd_col])

        if not valid.empty:
            successful = (valid[fwd_col] > SUCCESS_THRESHOLD).sum()
            success_rate = successful / len(valid) * 100
            avg_ret = valid[fwd_col].mean() * 100
            med_ret = valid[fwd_col].median() * 100

            print(f"Successful {FORWARD_DAYS}-day rebounds: {successful}")
            print(f"Success Rate: {success_rate:.2f}%")
            print(f"Average {FORWARD_DAYS}-day return: {avg_ret:.2f}%")
            print(f"Median {FORWARD_DAYS}-day return: {med_ret:.2f}%")

            print("""
Interpretation:
The objective is not to claim that RSI always works.
The objective is to ask:

'When an RSI local trough occurred historically,
how often was the forward return positive,
and how large was the typical forward move?'
""")


def explain_forward_return():
    print_section("WHAT IS FORWARD_5D_RETURN?")

    print(f"""
Forward_{FORWARD_DAYS}D_Return measures the return from the event date
to {FORWARD_DAYS} trading days later.

Formula:

Forward Return =
(Price after {FORWARD_DAYS} trading days / Event-day price) - 1

Example:
Event-day price = 100
Price 5 trading days later = 108

Forward 5D Return = (108 / 100) - 1 = +8%

If the future price is not yet available,
Forward_5D_Return is NaN.

NaN is correct behavior:
the system must not invent future data.
""")


# ------------------------------------------------------------
# 15. VISUALIZATIONS
# ------------------------------------------------------------

def plot_price_with_bollinger_events(df, ticker, label):
    plot_df = df.tail(250).copy()

    plt.figure(figsize=(12, 6))

    plt.plot(
        plot_df.index,
        plot_df["Close"],
        label="Close"
    )

    plt.plot(
        plot_df.index,
        plot_df["BB_Upper"],
        label="Upper Bollinger"
    )

    plt.plot(
        plot_df.index,
        plot_df["BB_Lower"],
        label="Lower Bollinger"
    )

    events = plot_df[
        plot_df["Bollinger_Reversal"]
    ]

    plt.scatter(
        events.index,
        events["Close"],
        marker="^",
        s=70,
        label="Bollinger Reversal"
    )

    plt.title(
        f"{ticker} — Bollinger Reversal Events ({label})"
    )

    plt.xlabel("Date")
    plt.ylabel("Adjusted Price")
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_rsi(df, ticker, label):
    plot_df = df.tail(250).copy()

    plt.figure(figsize=(12, 4))

    plt.plot(
        plot_df.index,
        plot_df["RSI"],
        label="RSI"
    )

    plt.axhline(30, linestyle="--", label="RSI 30")
    plt.axhline(50, linestyle="--", label="RSI 50")
    plt.axhline(70, linestyle="--", label="RSI 70")

    troughs = plot_df[
        plot_df["RSI_Local_Trough"]
    ]

    plt.scatter(
        troughs.index,
        troughs["RSI"],
        marker="o",
        s=50,
        label="RSI Local Trough"
    )

    plt.title(
        f"{ticker} — RSI and Local Trough Events ({label})"
    )

    plt.ylabel("RSI")
    plt.legend()
    plt.tight_layout()
    plt.show()


# ------------------------------------------------------------
# 16. MAIN ANALYSIS
# ------------------------------------------------------------

def run_analysis(start_date, end_date, label):

    print_section(f"SCENARIO 3 — TECHNICAL REVERSAL EVENTS — {label}")

    df = load_stock_data(
        ticker=TICKER,
        start=start_date,
        end=end_date
    )

    print(f"Ticker: {TICKER}")
    print(
        f"Data period: "
        f"{df.index.min().date()} -> "
        f"{df.index.max().date()}"
    )
    print(f"Daily observations: {len(df)}")

    # Calculate indicators
    df = add_bollinger_bands(df)
    df = add_rsi(df)
    df = add_kama(df)
    df = add_supertrend(df)
    df = add_ichimoku(df)
    df = add_volume_features(df)

    # Forward returns
    df = add_forward_returns(
        df,
        forward_days=FORWARD_DAYS
    )

    # Detect reversal events
    df = detect_reversal_events(df)

    # Event comparison
    comparison = build_event_comparison(
        df,
        forward_days=FORWARD_DAYS
    )

    print_section(
        f"REVERSAL EVENT SUMMARY — {FORWARD_DAYS}-DAY FORWARD RETURN"
    )

    print(
        comparison
        .sort_values(
            "Success_Rate_%",
            ascending=False
        )
        .round(2)
    )

    # Detailed table explanation
    explain_event_table(comparison)

    # RSI explanation
    explain_rsi_local_trough(df)

    # Forward return explanation
    explain_forward_return()

    # Bollinger example
    bollinger_events = df[
        df["Bollinger_Reversal"]
    ].dropna(
        subset=[f"Forward_{FORWARD_DAYS}D_Return"]
    )

    successes = (
        bollinger_events[
            f"Forward_{FORWARD_DAYS}D_Return"
        ] > SUCCESS_THRESHOLD
    ).sum()

    print_section("BOLLINGER REVERSAL EXAMPLE")

    print(f"Detected Bollinger reversal events: {len(bollinger_events)}")
    print(f"Successful {FORWARD_DAYS}-day rebounds: {successes}")

    if len(bollinger_events) > 0:
        success_rate = successes / len(bollinger_events) * 100
        avg_ret = (
            bollinger_events[f"Forward_{FORWARD_DAYS}D_Return"].mean()
            * 100
        )
        med_ret = (
            bollinger_events[f"Forward_{FORWARD_DAYS}D_Return"].median()
            * 100
        )

        print(f"Success Rate: {success_rate:.2f}%")
        print(f"Average {FORWARD_DAYS}-day return: {avg_ret:.2f}%")
        print(f"Median {FORWARD_DAYS}-day return: {med_ret:.2f}%")

        print("""
Interpretation:
A Bollinger reversal means price moved back above the lower Bollinger Band
after previously closing at or below it.

This event is NOT treated as an automatic BUY signal.
Instead, the system asks:

'After this event occurred historically,
how often was the 5-day forward return positive?'

Success Rate tells us how often the event was followed by a positive return.
Average Forward Return tells us the average size of the move.
Median Forward Return helps us see whether the average is being distorted by outliers.
""")

    # Recent events
    event_cols = [
        "Close",
        "RSI",
        "Bollinger_Reversal",
        "RSI_Local_Trough",
        "Volume_Rise",
        "KAMA_Bullish_Turn",
        "Supertrend_Bullish_Flip",
        "Ichimoku_Bullish_Breakout",
        "Strong_Reversal_Event",
        f"Forward_{FORWARD_DAYS}D_Return"
    ]

    recent_events = df[
        df[
            [
                "Bollinger_Reversal",
                "RSI_Local_Trough",
                "KAMA_Bullish_Turn",
                "Supertrend_Bullish_Flip",
                "Ichimoku_Bullish_Breakout"
            ]
        ].any(axis=1)
    ][event_cols].tail(20).copy()

    recent_events[
        f"Forward_{FORWARD_DAYS}D_Return"
    ] *= 100

    print_section("RECENT DETECTED REVERSAL EVENTS")
    print(recent_events.round(2))

    print("""
How to read this table:

Close
    Adjusted closing price on the event date.

RSI
    RSI value on that date.

Bollinger_Reversal
    True if a lower-band reversal event was detected.

RSI_Local_Trough
    True if RSI formed a local trough according to the event rule.

Volume_Rise
    True if volume was above its moving average.

KAMA_Bullish_Turn
    True if KAMA slope changed from non-positive to positive.

Supertrend_Bullish_Flip
    True if Supertrend direction changed from bearish to bullish.

Ichimoku_Bullish_Breakout
    True if price crossed above the top of the Ichimoku cloud.

Strong_Reversal_Event
    True only when several reversal conditions were satisfied together.

Forward_5D_Return
    Percentage price return five trading days after the event.
    Positive = price increased.
    Negative = price decreased.
    NaN = five future trading days are not yet available.
""")

    # Final teaching interpretation
    print_section("FINAL INTERPRETATION")

    print("""
The objective is NOT to assume that every technical indicator works.

The system treats each technical signal as a historical EVENT.

For each event, it asks:

1. How many times did this event occur?
2. How many of those events were followed by a positive 5-day return?
3. What was the success rate?
4. What was the average forward return?
5. What was the median forward return?
6. Is the sample size large enough to support a meaningful conclusion?

A stronger research event may combine:

Bollinger reversal
+ RSI local trough
+ volume confirmation
+ KAMA / Supertrend / Ichimoku trend confirmation

However, adding more indicators does NOT automatically improve the signal.
More filters can reduce the event count too much and create a very small sample.

Key lesson:
The dots on the chart are not BUY signals.
They are historical events that must be tested statistically.

Better research question:
'Under what conditions, how often, and with what forward return
did a technical reversal event work historically?'
""")

    # Visualizations
    plot_price_with_bollinger_events(
        df,
        TICKER,
        label
    )

    plot_rsi(
        df,
        TICKER,
        label
    )

    return {
        "data": df,
        "event_comparison": comparison,
        "bollinger_events": bollinger_events,
        "recent_events": recent_events
    }


# ------------------------------------------------------------
# 17. RUN THREE TIME WINDOWS
# ------------------------------------------------------------

def run_three_periods():
    today = pd.Timestamp.today().normalize()

    last_2_years_start = (
        today - pd.DateOffset(years=2)
    ).strftime("%Y-%m-%d")

    last_1_year_start = (
        today - pd.DateOffset(years=1)
    ).strftime("%Y-%m-%d")

    # --------------------------------------------------------
    # ANALYSIS 1 — FULL PERIOD
    # --------------------------------------------------------
    full_period = run_analysis(
        start_date=START_DATE,
        end_date=END_DATE,
        label="FULL PERIOD — FROM 2020"
    )

    # --------------------------------------------------------
    # ANALYSIS 2 — LAST 2 YEARS
    # --------------------------------------------------------
    last_2_years = run_analysis(
        start_date=last_2_years_start,
        end_date=END_DATE,
        label="LAST 2 YEARS"
    )

    # --------------------------------------------------------
    # ANALYSIS 3 — LAST 1 YEAR
    # --------------------------------------------------------
    last_1_year = run_analysis(
        start_date=last_1_year_start,
        end_date=END_DATE,
        label="LAST 1 YEAR"
    )

    # --------------------------------------------------------
    # FINAL COMPARISON
    # --------------------------------------------------------
    print_section(
        "FINAL COMPARISON — FULL PERIOD vs LAST 2 YEARS vs LAST 1 YEAR"
    )

    full_cmp = full_period["event_comparison"].copy()
    two_cmp = last_2_years["event_comparison"].copy()
    one_cmp = last_1_year["event_comparison"].copy()

    summary_rows = []

    for event_name in full_cmp.index:
        summary_rows.append({
            "Event": event_name,

            "Full_Count":
                full_cmp.loc[event_name, "Event_Count"],
            "Full_Success_%":
                full_cmp.loc[event_name, "Success_Rate_%"],
            "Full_Avg_5D_%":
                full_cmp.loc[event_name, "Average_Forward_Return_%"],

            "2Y_Count":
                two_cmp.loc[event_name, "Event_Count"],
            "2Y_Success_%":
                two_cmp.loc[event_name, "Success_Rate_%"],
            "2Y_Avg_5D_%":
                two_cmp.loc[event_name, "Average_Forward_Return_%"],

            "1Y_Count":
                one_cmp.loc[event_name, "Event_Count"],
            "1Y_Success_%":
                one_cmp.loc[event_name, "Success_Rate_%"],
            "1Y_Avg_5D_%":
                one_cmp.loc[event_name, "Average_Forward_Return_%"],
        })

    final_comparison = pd.DataFrame(summary_rows).set_index("Event")

    print(final_comparison.round(2))

    print("""
HOW TO READ THE THREE-PERIOD COMPARISON:

FULL PERIOD
    Shows the long-run historical behavior since 2020.

LAST 2 YEARS
    Shows whether the same technical event has behaved similarly
    under more recent market conditions.

LAST 1 YEAR
    Shows the most recent behavior and helps detect possible
    market-regime changes.

Important:
A technical event may look strong over the full historical sample
but become weaker in the last 1 or 2 years.

That does not automatically mean the indicator is useless.
It may mean:
- the market regime changed,
- volatility changed,
- the stock behavior changed,
- the historical effect weakened,
- or the recent sample size is too small.

Therefore, always compare:
Event Count
+ Success Rate
+ Average Forward Return
+ Median Forward Return
across multiple time windows.
""")

    return {
        "full_period": full_period,
        "last_2_years": last_2_years,
        "last_1_year": last_1_year,
        "final_comparison": final_comparison
    }


# ------------------------------------------------------------
# 18. RUN
# ------------------------------------------------------------

if __name__ == "__main__":
    results = run_three_periods()
