#!/usr/bin/env python3
"""
Quick test to demonstrate the voice validator in action.
Run: python test_voice_validator.py
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'NewsletterAiAgent', 'src'))

from newsletter.voice_validator import validate_and_score

def print_result(label, text, result):
    """Pretty print validation results."""
    print(f"\n{'='*80}")
    print(f"TEST: {label}")
    print(f"{'='*80}")
    print(f"\nText:\n{text}\n")
    print(f"Score: {result['score']}/100 {'✅' if result['valid'] else '❌'}")
    print(f"Valid: {result['valid']}")
    
    if result.get('sentence_analysis'):
        sa = result['sentence_analysis']
        print(f"\nSentence Analysis:")
        print(f"  • Average length: {sa['avg_length']} words")
        print(f"  • Short sentences: {sa['short_ratio']*100:.0f}%")
        print(f"  • Total sentences: {sa['total_sentences']}")
    
    if result.get('positive_signals'):
        print(f"\nPositive Signals:")
        for signal, count in result['positive_signals'].items():
            if count > 0:
                print(f"  ✓ {signal}: {count}")
    
    if result.get('negative_signals'):
        print(f"\nNegative Signals (problems):")
        for signal, count in result['negative_signals'].items():
            if count > 0:
                print(f"  ✗ {signal}: {count}")
    
    if result.get('suggestions'):
        print(f"\nSuggestions:")
        for i, suggestion in enumerate(result['suggestions'], 1):
            print(f"  {i}. {suggestion}")


# Test Case 1: BAD - Generic corporate writing
bad_text = """
In today's newsletter, we will explore some interesting developments in 
the autonomous vehicle industry. This could potentially be a transformative 
technology that might help companies optimize their operations. The market 
is quite dynamic and companies should perhaps consider evaluating these 
solutions. It is important to leverage synergy between different stakeholders. 
The robust framework that was developed by industry leaders may facilitate 
better outcomes. This is an amazing opportunity that organizations could 
utilize to enhance their competitive advantage.
"""

# Test Case 2: GOOD - Bartlett/Hormozi style
good_text = """
<h2>You're Losing $10k Every Day</h2>
<p>I fired my best friend last Tuesday. He was my co-founder. He was also 
destroying the company. The hardest decision I've ever made saved my business.

Here's what I learned: loyalty to people can't come before loyalty to the mission. 
If someone isn't performing, you have three options: 1) Train them better, 
2) Move them to a different role, 3) Let them go. Option 4 (do nothing) is 
choosing failure.

Most founders wait 6 months too long. You know within 2 weeks if someone's 
a fit. Everything after that is just expensive hope. Stop hoping. Start deciding.

What's your "$10k/day mistake"? Who are you keeping around because it's easier 
than having the hard conversation?</p>

<h3>Playbook</h3>
<ul>
<li>Audit your team: identify the bottom 10% performers by next Friday</li>
<li>Have direct 1-on-1s: "Here's what's not working, here's the standard, do you want this?"</li>
<li>Set 30-day improvement plans with weekly check-ins</li>
<li>If no progress by week 3, start exit planning</li>
<li>Be generous with severance but fast with decision</li>
</ul>
"""

# Test Case 3: MEDIUM - Partially good voice
medium_text = """
<h2>Stop Wasting Money on Ads</h2>
<p>You don't have a marketing problem. You have an offer problem. If your ad 
doesn't work, it's because what you're selling isn't worth buying. The conversion 
rate might be low because the value proposition could potentially be improved. 
Companies that have successfully scaled their operations often utilize a framework 
that optimizes customer acquisition. This interesting approach has been amazing 
for growth.</p>
"""

# Test Case 4: HTML content
html_text = """
<h2>Fire Fast, Hire Slow</h2>
<p>I've made this mistake 47 times. I'll probably make it again. But I'm getting better.</p>

<p>You know someone's wrong for the role within 2 weeks. Your gut tells you. The data confirms it. 
But you wait 6 months because you're scared. Scared of being wrong. Scared of being mean. 
Scared of starting over.</p>

<p>Here's the math: A bad hire costs you $50k minimum. That's salary, lost productivity, and 
the opportunity cost of not having the right person. Multiply that by 6 months. You just lit 
$25k on fire because you couldn't have a 15-minute conversation.</p>

<p>Stop it. Rip the band-aid off. Your A-players are watching. When you keep the C-players, 
you're telling the A-players their effort doesn't matter. They'll leave. Then you're really screwed.</p>

<h3>Playbook</h3>
<ul>
<li>Set a 2-week trial for all new hires with clear success metrics</li>
<li>Have a review meeting on day 10 (not day 14)</li>
<li>If it's not a "hell yes" by day 14, it's a no</li>
<li>Document everything for clean termination</li>
<li>Exit fast: generous severance, same day departure</li>
</ul>
"""

if __name__ == "__main__":
    print("\n" + "="*80)
    print("VOICE VALIDATOR TEST SUITE")
    print("Testing Bartlett/Hormozi voice detection")
    print("="*80)
    
    # Run tests
    result1 = validate_and_score(bad_text)
    print_result("BAD - Generic Corporate Writing", bad_text[:200] + "...", result1)
    
    result2 = validate_and_score(good_text)
    print_result("GOOD - Authentic Bartlett/Hormozi Voice", good_text[:200] + "...", result2)
    
    result3 = validate_and_score(medium_text)
    print_result("MEDIUM - Mixed Voice Quality", medium_text[:200] + "...", result3)
    
    result4 = validate_and_score(html_text)
    print_result("EXCELLENT - HTML with Strong Voice", html_text[:200] + "...", result4)
    
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    print(f"Test 1 (Bad):      {result1['score']}/100 {'✅ PASS' if not result1['valid'] else '❌ FAIL'} (should be invalid)")
    print(f"Test 2 (Good):     {result2['score']}/100 {'✅ PASS' if result2['valid'] else '❌ FAIL'} (should be valid)")
    print(f"Test 3 (Medium):   {result3['score']}/100 {'ℹ️  INFO'} (borderline case)")
    print(f"Test 4 (HTML):     {result4['score']}/100 {'✅ PASS' if result4['valid'] else '❌ FAIL'} (should be valid)")
    print("\n")
