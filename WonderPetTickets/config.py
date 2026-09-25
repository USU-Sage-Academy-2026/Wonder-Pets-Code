# ---------------------------------------------------------------------------
# Generation bucketing (used by sort_generation)
# ---------------------------------------------------------------------------

# Age bin edges for pd.cut. Intervals are right-inclusive by default:
# (18, 25], (25, 35], (35, 45], (45, 60], (60, 70]
bins = [18, 25, 35, 45, 60, 70]

# One label per interval above (always len(bins) - 1 labels).
labels = ['Gen Z', 'Millennials', 'Gen X', 'Boomers', 'Silent']

# ---------------------------------------------------------------------------
# Data-quality checks (used by flag_nulls)
# ---------------------------------------------------------------------------

# Rows with this many missing values or more are flagged.
null_count = 2
