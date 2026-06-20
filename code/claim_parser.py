import re

def parse_claim(user_claim, claim_object):

    text = str(user_claim).lower()

    issue_type = "unknown"
    object_part = "unknown"

    # Prompt Injection Detection
    if (
        "ignore previous instructions" in text
        or "ignore all previous instructions" in text
        or "mark supported" in text
        or "set severity" in text
        or "override" in text
        or "system prompt" in text
        or "approve immediately" in text
        or "skip manual review" in text
        or "follow this instruction" in text
        or "approve the claim" in text
    ):
        return "prompt_injection_attempt", "unknown"

    # Issue Detection
    if "glass shatter" in text or "shattered" in text:
        issue_type = "glass_shatter"

    elif "dent" in text:
        issue_type = "dent"

    elif "scratch" in text or "scrape" in text:
        issue_type = "scratch"

    elif "crack" in text:
        issue_type = "crack"

    elif (
        "screen damage" in text
        or "display damage" in text
    ):
        issue_type = "crack"

    elif (
        "broken" in text
        or "snapped" in text
        or "detached" in text
    ):
        issue_type = "broken_part"

    elif "missing" in text:
        issue_type = "missing_part"

    elif "water" in text:
        issue_type = "water_damage"

    elif "stain" in text:
        issue_type = "stain"

    elif "torn" in text:
        issue_type = "torn_packaging"

    elif "crushed" in text:
        issue_type = "crushed_packaging"

    # =====================
    # CAR PARTS
    # =====================

    if "rear bumper" in text:
        object_part = "rear_bumper"

    elif "front bumper" in text:
        object_part = "front_bumper"

    elif "bumper" in text:
        object_part = "front_bumper"

    elif "mirror" in text:
        object_part = "side_mirror"

    elif "windshield" in text:
        object_part = "windshield"

    elif "door" in text:
        object_part = "door"

    elif "hood" in text:
        object_part = "hood"

    elif "headlight" in text:
        object_part = "headlight"

    elif (
        "taillight" in text
        or "rear light" in text
        or "back light" in text
    ):
        object_part = "taillight"

    # =====================
    # LAPTOP PARTS
    # =====================

    elif "screen" in text:
        object_part = "screen"

    elif "keyboard" in text:
        object_part = "keyboard"

    elif "trackpad" in text:
        object_part = "trackpad"

    elif "hinge" in text:
        object_part = "hinge"

    elif "lid" in text:
        object_part = "lid"

    elif (
        claim_object == "laptop"
        and "corner" in text
    ):
        object_part = "corner"

    elif (
        claim_object == "laptop"
        and "body" in text
    ):
        object_part = "body"

    # =====================
    # PACKAGE PARTS
    # =====================

    elif "box" in text:
        object_part = "box"

    elif (
        claim_object == "package"
        and "corner" in text
    ):
        object_part = "package_corner"

    elif "label" in text:
        object_part = "label"

    elif "seal" in text:
        object_part = "seal"

    return issue_type, object_part