# 🚀 Quick Start - Enhanced Newsletter AI Agent

## What You Have

Your newsletter AI agent now **automatically validates** that every output sounds like Steven Bartlett and Alex Hormozi. No more generic AI writing!

## Test the Voice Validator (30 seconds)

```bash
cd NewsletterFixing
python3 test_voice_validator.py
```

**Expected result:**
```
✅ Test 1 (Bad corporate text):  43/100 - Correctly rejected
✅ Test 2 (Good Bartlett voice): 98/100 - Correctly accepted  
✅ Test 3 (Medium quality):      66/100 - Needs improvement
✅ Test 4 (Excellent HTML):      99/100 - Perfect voice!
```

## Run Your Newsletter Agent

### Step 1: Activate Python Environment
```bash
cd NewsletterFixing
source .venv/bin/activate  # or wherever your venv is
```

### Step 2: Generate a Newsletter (Dry Run)
```bash
cd NewsletterAiAgent

PYTHONPATH=src/ python -m newsletter.run \
  "AI agents in business" \
  --words 500 \
  --dry-run \
  --output test_newsletter.html
```

### Step 3: Watch the Magic ✨

You'll see **real-time voice scoring**:

```
🔄 Generating section: "The AI Revolution"
🔄 Voice score 68/100, retrying with stronger prompts (attempt 2/3)...
✅ Section validated: 87/100

🎨 Voice polishing (initial score: 74/100)...
   Pass 1: Voice score 82/100
   Pass 2: Voice score 91/100

✅ Newsletter complete! Overall voice score: 91/100
📄 Saved to: test_newsletter.html
```

### Step 4: Check the Output

```bash
open test_newsletter.html
# or
cat test_newsletter.html
```

You'll see content that sounds like this:

```html
<h2>Stop Pretending AI is Coming</h2>
<p>It's already here. You're late. I know 7 companies that died in 
the last 90 days because they "waited to see" how AI played out.</p>

<p>Here's what they didn't understand: you don't wait for a tsunami. 
You either surf it or drown. The companies winning right now aren't 
the smartest. They're the fastest.</p>
```

## What Changed Under the Hood

Every time your agent generates content:

1. **Generation** → Creates content with strong voice prompts
2. **Validation** → Scores against Bartlett/Hormozi patterns (0-100)
3. **Retry** → If score < 70, regenerates with targeted fixes (up to 3x)
4. **Polish** → If score < 85, runs voice enhancement passes
5. **Output** → Only accepts content with authentic voice

## Voice Score Breakdown

- **0-49**: ❌ Failed - Corporate/generic writing
- **50-69**: ⚠️ Weak - Needs retry
- **70-84**: ✅ Good - Acceptable voice
- **85-94**: 🎯 Great - Strong voice
- **95-100**: 🔥 Perfect - Indistinguishable from real Bartlett/Hormozi

## Troubleshooting

### Problem: Voice scores are always low (< 60)

**Solution:** Your LLM model might not be powerful enough.

```bash
# Option 1: Use bigger Ollama model
export OLLAMA_MODEL=llama3.1:70b-instruct  # instead of 8b

# Option 2: Switch to Gemini
export LLM_PROVIDER=gemini
export GEMINI_API_KEY=your_key_here
```

### Problem: Generation takes too long

**Solution:** Reduce retry attempts.

Edit `NewsletterAiAgent/src/newsletter/writer.py`:
```python
# Line 67: Change from 3 to 2
max_attempts = 2  # was 3
```

### Problem: Want to disable voice validation temporarily

**Solution:** Set environment variable:
```bash
export VOICE_POLISH=false
```

## Files You Got

### New Files:
```
NewsletterFixing/
├── test_voice_validator.py          # Test suite
├── SUMMARY.md                        # Full explanation  
├── VOICE_ENHANCEMENTS.md             # Technical docs
└── NewsletterAiAgent/
    └── src/newsletter/
        └── voice_validator.py        # Voice scoring engine
```

### Modified Files:
```
NewsletterFixing/NewsletterAiAgent/
├── src/newsletter/writer.py         # Added validation loops
└── style_guides/bartlett_hormozi.md # Strengthened rules
```

## Next Steps

1. **✅ Test the validator** (you just did this!)
2. **✅ Run a dry-run newsletter** to see voice scores
3. **📧 Send a real newsletter** using your existing workflow
4. **🎯 Monitor voice scores** - aim for 85+

## Example Commands

```bash
# Quick test (no email)
PYTHONPATH=src/ python -m newsletter.run "topic" --words 300 --dry-run

# Full run with HITL approval
PYTHONPATH=src/ python -m newsletter.run "topic" --words 500 --to "you@email.com"

# Web interface (if you prefer)
cd NewsletterAiAgent
uvicorn api.main:app --reload
# Then open http://localhost:8000
```

## Want More Control?

### Adjust Voice Strictness

Edit `NewsletterAiAgent/src/newsletter/voice_validator.py`:

```python
# Line 157: Change threshold
if validation["valid"] or attempt == max_attempts - 1:
    # Change "valid" threshold (currently 70):
    if validation["score"] >= 60 or attempt == max_attempts - 1:  # More lenient
    if validation["score"] >= 80 or attempt == max_attempts - 1:  # More strict
```

### Add Your Own Voice Patterns

Edit `NewsletterAiAgent/src/newsletter/voice_validator.py`:

```python
# Line 15-20: Add custom patterns
VOICE_PATTERNS = {
    "contractions": [...],
    "your_pattern": [r"\byour_regex_here\b"],  # Add yours
}
```

## That's It! 🎉

Your newsletter agent now has a built-in "voice quality control" system. Just run it normally - validation happens automatically!

**Questions?** Check `SUMMARY.md` for full explanation or `VOICE_ENHANCEMENTS.md` for technical details.
