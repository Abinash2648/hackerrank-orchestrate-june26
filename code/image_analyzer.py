import os
import json
from PIL import Image
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def analyze_images(image_paths, claim_object, user_claim):

    first_image = image_paths.split(";")[0].strip()

    full_path = os.path.join(
        "..",
        "dataset",
        first_image
    )

    if not os.path.exists(full_path):
        return {
            "valid_image": False,
            "risk_flags": "wrong_object",
            "issue_type": "unknown",
            "object_part": "unknown",
            "severity": "unknown",
            "supporting_image_ids": "none"
        }

    image = Image.open(full_path)

    prompt = f"""
You are an insurance claim reviewer.

Claim Object:
{claim_object}

User Claim:
{user_claim}

Return ONLY JSON.

Schema:

{{
 "issue_type":"",
 "object_part":"",
 "severity":"",
 "valid_image":true,
 "risk_flags":"none"
}}

Allowed issue_type:
dent,scratch,crack,glass_shatter,broken_part,
missing_part,torn_packaging,crushed_packaging,
water_damage,stain,none,unknown

Allowed severity:
low,medium,high,unknown

Analyze ONLY visible evidence.
"""
    print("Processing:", first_image)
    print("Using model: gemini-2.0-flash")
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[
            prompt,
            image
        ]
    )

    try:
        result = json.loads(response.text)

        result["supporting_image_ids"] = (
            os.path.splitext(
                os.path.basename(first_image)
            )[0]
        )

        return result

    except:
        return {
            "valid_image": True,
            "risk_flags": "manual_review_required",
            "issue_type": "unknown",
            "object_part": "unknown",
            "severity": "unknown",
            "supporting_image_ids": "none"
        }