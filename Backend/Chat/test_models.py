#!/usr/bin/env python3
"""
Test Groq API models to find working ones
"""
import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Initialize Groq client
api_key = os.environ.get("LLM_API_KEY") or os.environ.get("GROQ_API_KEY")
if not api_key:
    print("❌ No API key found!")
    exit(1)

client = Groq(api_key=api_key)

# Test current Llama models (as of 2025)
test_models = [
    "llama-3.1-70b-versatile",
    "llama-3.1-8b-instant", 
    "llama-3.2-90b-text-preview",
    "llama-3.2-11b-text-preview",
    "llama-3.2-3b-preview",
    "llama-3.2-1b-preview",
    "llama3-70b-8192",
    "llama3-8b-8192"
]

print("🧪 Testing Groq models...")
working_models = []

for model in test_models:
    try:
        print(f"\nTesting {model}...")
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": "Say 'Hello, this model works!'"}
            ],
            max_tokens=20,
            temperature=0.1
        )
        result = response.choices[0].message.content
        print(f"✅ {model}: {result}")
        working_models.append(model)
    except Exception as e:
        print(f"❌ {model}: {str(e)}")

print(f"\n🎯 Working models found: {len(working_models)}")
for model in working_models:
    print(f"  - {model}")

if working_models:
    print(f"\n💡 Recommended: {working_models[0]}")
else:
    print("\n⚠️ No working models found!")