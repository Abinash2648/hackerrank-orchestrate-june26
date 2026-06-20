def analyze_risk(user_history_row):

    history_flags = str(
        user_history_row["history_flags"]
    ).strip()
    user_history_row["history_summary"]

    if history_flags and history_flags != "none":
        return history_flags

    flags = []

    if user_history_row["last_90_days_claim_count"] >= 5:
        flags.append("user_history_risk")

    if (
        user_history_row["manual_review_claim"] >= 2
        or
        user_history_row["rejected_claim"] >= 2
    ):
        flags.append("manual_review_required")

    if not flags:
        return "none"

    return ";".join(flags)