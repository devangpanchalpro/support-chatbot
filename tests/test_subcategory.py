#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test subcategory feature"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

from bot.chatbot import AarogyaChatbot

bot = AarogyaChatbot()

print("=" * 70)
print("  Testing AarogyaOne Chatbot - Sub-Category Feature")
print("=" * 70)

# Test 1: User asks general "ABHA card"
print("\n[Test 1] User: 'ABHA card'")
bot.selected_lang = "en"
response = bot.chat("ABHA card")
print(response)

# Test 2: User selects option 1 (create)
print("\n[Test 2] User: '1'")
response = bot.chat("1")
print(response)

print("\n" + "=" * 70)

# Test 3: Ayushman card
print("\n[Test 3] User: 'Ayushman card'")
bot = AarogyaChatbot()
bot.selected_lang = "en"
response = bot.chat("Ayushman card")
print(response)

# Test 4: Select by keyword "coverage"
print("\n[Test 4] User: 'coverage'")
response = bot.chat("coverage")
print(response)

print("\n" + "=" * 70)
print("Tests Completed!")

