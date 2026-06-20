# Evaluation Report

## Dataset Used

Development and evaluation were performed using:

dataset/sample_claims.csv

Final predictions were generated using:

dataset/claims.csv

---

## Strategy Comparison

### Strategy 1 – Rule-Based Only

Components:

* Keyword extraction
* User history analysis
* Evidence requirement matching

Advantages:

* Fast
* No API cost
* Reliable execution

Limitations:

* Limited visual understanding
* Cannot verify image contents

---

### Strategy 2 – Hybrid Gemini + Rules

Components:

* Gemini image analysis
* Rule-based validation
* User history scoring

Advantages:

* Better visual verification
* More accurate damage classification
* Better contradiction detection

Limitations:

* Subject to API quotas
* Higher latency

---

## Final Strategy Used

The final submission uses:

* Rule-based parsing
* User history risk analysis
* Evidence validation
* Prompt injection detection

Gemini image verification remains implemented but was disabled because the free-tier quota was exhausted during development.

---

## Operational Analysis

### Approximate Model Calls

Sample dataset:

* 0 Gemini calls (fallback mode)

Test dataset:

* 0 Gemini calls (fallback mode)

If Gemini were enabled:

* Approximately 1 image analysis call per claim

Estimated:

* Sample set: ~15–20 calls
* Test set: ~40–60 calls

---

### Approximate Token Usage

Fallback mode:

* 0 API tokens

Gemini mode estimate:

Input:

* 300–600 tokens per claim

Output:

* 50–100 tokens per claim

Average:

* ~700 tokens per claim

---

### Number of Images Processed

Sample dataset:

* Approximately 20 images

Test dataset:

* Approximately 60+ images

Images are processed locally.

---

### Approximate Cost

Fallback mode:

$0

Gemini mode estimate:

Less than $1 for the provided datasets under standard Gemini pricing assumptions.

---

### Runtime

Rule-based pipeline:

* Less than 5 seconds

Gemini mode:

* Approximately 2–5 seconds per claim

Estimated total runtime:

* 2–4 minutes for the complete dataset

---

### TPM / RPM Considerations

Potential Gemini limitations:

* Requests Per Minute (RPM)
* Tokens Per Minute (TPM)

Mitigation strategies:

* Retry handling
* Rule-based fallback
* Local CSV processing
* Optional batching
* Reduced repeated calls

---

### Caching Strategy

Potential production improvements:

* Image hash caching
* Repeated claim caching
* Duplicate image detection

These were considered but not required for the current dataset size.

---

## Conclusion

The final system successfully:

* Parses claim conversations
* Detects issue types
* Detects prompt injection attempts
* Uses user history for risk scoring
* Validates evidence requirements
* Produces structured output.csv

The architecture supports future extension using Gemini image verification when API quota is available.
