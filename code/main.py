import pandas as pd

from claim_parser import parse_claim
from risk_analyzer import analyze_risk
# from image_analyzer import analyze_images

claims_df = pd.read_csv("../dataset/claims.csv")
history_df = pd.read_csv("../dataset/user_history.csv")
evidence_df = pd.read_csv("../dataset/evidence_requirements.csv")

results = []

for _, row in claims_df.iterrows():

    user_id = row["user_id"]

    history_row = history_df[
        history_df["user_id"] == user_id
    ]

    if len(history_row) > 0:
        history_row = history_row.iloc[0]

        risk_flags = analyze_risk(
            history_row
        )

    else:
        risk_flags = "none"

    issue_type, object_part = parse_claim(
        row["user_claim"],
        row["claim_object"]
    )

    # Uncomment after Gemini quota resets

    # image_result = analyze_images(
    #     row["image_paths"],
    #     row["claim_object"],
    #     row["user_claim"]
    # )

    image_result = {
        "valid_image": True,
        "risk_flags": "none",
        "issue_type": issue_type,
        "object_part": object_part,
        "supporting_image_ids": "img_1"
    }

    # =====================
    # Evidence Rules
    # =====================

    provided_images = len(
        [
            img.strip()
            for img in str(
                row["image_paths"]
            ).split(";")
            if img.strip()
        ]
    )

    required_images = 1

    evidence_standard_met = (
        provided_images >= required_images
    )

    object_rules = evidence_df[
        evidence_df["claim_object"]
        == row["claim_object"]
    ]

    if evidence_standard_met:

        evidence_reason = "; ".join(
            object_rules[
                "minimum_image_evidence"
            ].tolist()
        )

    else:

        evidence_reason = (
            "No images provided"
        )

    # =====================
    # Severity Rules
    # =====================

    if issue_type in [
        "glass_shatter",
        "broken_part"
    ]:

        severity = "high"

    elif issue_type in [
        "dent",
        "scratch",
        "stain",
        "crack"
    ]:

        severity = "medium"

    elif issue_type == "unknown":

        severity = "unknown"

    else:

        severity = "low"

    # =====================
    # Merge Risk Flags
    # =====================

    combined_flags = []

    if risk_flags != "none":
        combined_flags.append(
            risk_flags
        )

    if (
        image_result["risk_flags"]
        != "none"
    ):
        combined_flags.append(
            image_result["risk_flags"]
        )

    final_risk_flags = (
        ";".join(combined_flags)
        if combined_flags
        else "none"
    )

    # =====================
    # Claim Decision
    # =====================

    if (
        issue_type
        == "prompt_injection_attempt"
    ):

        claim_status = (
            "not_enough_information"
        )

        justification = (
            "Prompt injection detected"
        )

    elif (
        "manual_review_required"
        in final_risk_flags
    ):

        claim_status = (
            "not_enough_information"
        )

        justification = (
            "Risk profile requires review"
        )

    elif not evidence_standard_met:

        claim_status = (
            "not_enough_information"
        )

        justification = (
            "Evidence requirements not met"
        )

    else:

        claim_status = (
            "supported"
        )

        justification = (
            "Evidence and claim appear consistent"
        )

    result = {

        "user_id":
            row["user_id"],

        "image_paths":
            row["image_paths"],

        "user_claim":
            row["user_claim"],

        "claim_object":
            row["claim_object"],

        "evidence_standard_met":
            evidence_standard_met,

        "evidence_standard_met_reason":
            evidence_reason,

        "risk_flags":
            final_risk_flags,

        "issue_type":
            image_result[
                "issue_type"
            ],

        "object_part":
            image_result[
                "object_part"
            ],

        "claim_status":
            claim_status,

        "claim_status_justification":
            justification,

        "supporting_image_ids":
            image_result[
                "supporting_image_ids"
            ],

        "valid_image":
            image_result[
                "valid_image"
            ],

        "severity":
            severity
    }

    results.append(result)

output_df = pd.DataFrame(results)

output_df.to_csv(
    "../dataset/output.csv",
    index=False
)

print(
    "output.csv generated successfully"
)