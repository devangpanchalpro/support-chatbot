#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Debug test for Ayushman"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

from bot.chatbot import AarogyaChatbot

print("=" * 70)
print("  Debug Test - Ayushman Card")
print("=" * 70)

bot = AarogyaChatbot()
bot.selected_lang = "en"

print("\nInput: 'Ayushman card'")
text = "Ayushman card"
intents = bot.detect_intent(text)
print(f"Detected Intents: {intents}")

main_cat = bot.get_main_category(intents)
print(f"Main Category: {main_cat}")

response = bot.chat("Ayushman card")
print(f"\nResponse:\n{response}")

if response is None:
    print("\nERROR: Response is None!")
    print("Checking build_response...")
    from bot.chatbot import AarogyaChatbot as AC2
    bot2 = AC2()
    bot2.selected_lang = "en"
    responses = []
    build_resp = bot2.build_response(intents, "Ayushman card", "en")
    print(f"build_response result: {build_resp}")
