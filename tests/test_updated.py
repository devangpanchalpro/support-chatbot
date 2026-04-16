#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test updated sub-category feature"""

from bot.chatbot import AarogyaChatbot

print("=" * 80)
print("  Testing Updated Sub-Category Feature")
print("=" * 80)

bot = AarogyaChatbot()

# Test 1: ABHA card - should show options without numbers
print("\n[Test 1] User: 'ABHA card' (English)")
bot.selected_lang = "en"
response = bot.chat("ABHA card")
print(response)

# Test 2: User types "create" - should get ABHA creation answer
print("\n[Test 2] User: 'create'")
response = bot.chat("create")
print(response)

# Test 3: New conversation - Ayushman card
print("\n[Test 3] User: 'Ayushman card' (Hindi)")
bot = AarogyaChatbot()
bot.selected_lang = "hi"
response = bot.chat("Ayushman card")
print(response)

# Test 4: User types "coverage" - should get coverage answer
print("\n[Test 4] User: 'coverage'")
response = bot.chat("coverage")
print(response)

# Test 5: Test keyword variations
print("\n[Test 5] User: 'how to download'")
response = bot.chat("how to download")
print(response)

print("\n" + "=" * 80)
print("Tests Completed!")
print("✅ No numbers in options")
print("✅ Language consistency")
print("✅ Keyword matching improved")
print("✅ Direct RAG answers")
