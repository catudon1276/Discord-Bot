import os
import discord
import re
import random

# Discord bot token を環境変数から取得
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
if not TOKEN:
    raise ValueError("環境変数 DISCORD_BOT_TOKEN が設定されていません！")

# Set up required intents
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Dictionary to store user language preferences
user_languages = {}

# Dictionary for localized strings
LOCALIZED_STRINGS = {
    'ja': {
        'help_title': "**🎲 ダイスボットの使い方**",
        'help_intro': "以下のコマンドでダイスを振ることができます。すべてのダイスロールはメッセージを編集して結果を追記します。",
        'help_roll_title': "1. ダイスを振る",
        'help_roll_format': "・**書式**: `(ダイス数)d(面数)` または `dice(ダイス数)d(面数)=`",
        'help_roll_example': "・**例**: `1d6` → `1d6(3) = [3]`\n　　　`2d6+1d8` → `2d6[9]+1d8[7] = [16]`\n　　　`3d6×5` → `3d6[12]×5 = [60]`\n　　　`(1d4+1)÷2d8` → `(1d4[3]+1)÷2d8[10] = [0]`",
        'help_roll_limits': "・**上限**: ダイス数1〜100、面数1〜10000",
        'help_d100_title': "2. d100専用コマンド",
        'help_d100_format': "・**書式**: `d100`",
        'help_d100_desc': "・`1d100` と同じです。クリティカル・ファンブルが表示されます。",
        'help_ignore_title': "3. ダイスロールを無視する",
        'help_ignore_desc': "・メッセージの先頭にシングルクォート `'` または `’` をつけると、ダイスロールとして認識されません",
        'help_ignore_example': "・**例**: `'`dice1d6=` はただのテキストになります",
        'help_lang_title': "4. 言語設定",
        'help_lang_desc': "・`[言語コード]`を`en`にすると英語、`ja`にすると日本語になります。",
        'help_lang_example': "・**書式**: `/dice lang [言語コード]`",
        'critical': " ✨クリティカル！",
        'fumble': " 💀ファンブル！",
        'error_message': "エラーが発生しました。",
        'lang_en_success': "言語設定を英語に変更しました。",
        'lang_ja_success': "言語設定を日本語に変更しました。"
    },
    'en': {
        'help_title': "**🎲 Dice Bot Usage**",
        'help_intro': "Roll dice with the commands below. All dice rolls will edit the original message to add the result.",
        'help_roll_title': "1. Rolling Dice",
        'help_roll_format': "- **Format**: `(Number of Dice)d(Number of Sides)` or `dice(Number of Dice)d(Number of Sides)=`",
        'help_roll_example': "- **Examples**: `1d6` → `1d6(3) = [3]`\n　　　`2d6+1d8` → `2d6[9]+1d8[7] = [16]`\n　　　`3d6×5` → `3d6[12]×5 = [60]`\n　　　`(1d4+1)÷2d8` → `(1d4[3]+1)÷2d8[10] = [0]`",
        'help_roll_limits': "- **Limits**: 1-100 dice, 1-10,000 sides",
        'help_d100_title': "2. The `d100` Exclusive Command",
        'help_d100_format': "- **Format**: `d100`",
        'help_d100_desc': "- Equivalent to `1d100`, but it displays critical hits and fumbles.",
        'help_ignore_title': "3. Ignoring a Dice Roll",
        'help_ignore_desc': "- If your message starts with a single quote (`'` or `’`), the dice roll will not be recognized.",
        'help_ignore_example': "- **Example**: `'`dice1d6=` will be treated as plain text.",
        'help_lang_title': "4. Language Settings",
        'help_lang_desc': "- `[Language Code]` can be `en` for English or `ja` for Japanese.",
        'help_lang_example': "- **Format**: `/dice lang [language code]`",
        'critical': " ✨ Critical!",
        'fumble': " 💀 Fumble!",
        'error_message': "An error occurred.",
        'lang_en_success': "Language has been set to English.",
        'lang_ja_success': "Language has been set to Japanese."
    }
}

def get_localized_text(user_id, key):
    lang = user_languages.get(user_id, 'ja')
    return LOCALIZED_STRINGS[lang].get(key, 'Error: Text not found')

def roll_dice(dice_count, dice_sides):
    return [random.randint(1, dice_sides) for _ in range(dice_count)]

@client.event
async def on_ready():
    pass

@client.event
async def on_message(message):
    if message.author.bot:
        return

    content = message.content
    user_id = message.author.id

    # 言語設定コマンド
    if content.lower().strip() == '/dice lang en':
        user_languages[user_id] = 'en'
        await message.channel.send(get_localized_text(user_id, 'lang_en_success'))
        return
    elif content.lower().strip() == '/dice lang ja':
        user_languages[user_id] = 'ja'
        await message.channel.send(get_localized_text(user_id, 'lang_ja_success'))
        return

    # /help dice コマンド
    if content.lower().strip() == '/help dice':
        help_message = f"""
{get_localized_text(user_id, 'help_title')}

{get_localized_text(user_id, 'help_intro')}

{get_localized_text(user_id, 'help_roll_title')}
{get_localized_text(user_id, 'help_roll_format')}
{get_localized_text(user_id, 'help_roll_example')}
{get_localized_text(user_id, 'help_roll_limits')}

{get_localized_text(user_id, 'help_d100_title')}
{get_localized_text(user_id, 'help_d100_format')}
{get_localized_text(user_id, 'help_d100_desc')}

{get_localized_text(user_id, 'help_ignore_title')}
{get_localized_text(user_id, 'help_ignore_desc')}
{get_localized_text(user_id, 'help_ignore_example')}

{get_localized_text(user_id, 'help_lang_title')}
{get_localized_text(user_id, 'help_lang_desc')}
{get_localized_text(user_id, 'help_lang_example')}
"""
        await message.channel.send(help_message)
        return

    # 先頭が ' または ’ の場合は無視
    if content.startswith(("'", "’")):
        return

    has_operator = re.search(r"[+\-*/×÷]", content)
    dice_matches = list(re.finditer(r"(\d*)[dD](\d+)", content))
    if dice_matches:
        replacements = []
        expression_values = {}
        for i, match in enumerate(dice_matches):
            dice_count = int(match.group(1) or 1)
            dice_sides = int(match.group(2))
            if dice_count > 100 or dice_sides > 10000:
                continue
            results = roll_dice(dice_count, dice_sides)
            total = sum(results)
            if has_operator:
                result_str = f"[{total}]"
            elif dice_count > 10:
                result_str = f"({total})"
            else:
                result_str = f"({', '.join(map(str, results))})"
            replacements.append((match.start(), match.end(), f"{match.group()}{result_str}"))
            expression_values[f"d{i}"] = total

        modified_content = content
        for start, end, repl_text in reversed(replacements):
            modified_content = modified_content[:start] + repl_text + modified_content[end:]

        expression_to_eval = content.replace('×', '*').replace('÷', '/')
        for i, match in enumerate(dice_matches):
            expression_to_eval = expression_to_eval.replace(match.group(), f"d{i}", 1)

        final_total = eval(expression_to_eval, {}, expression_values)
        final_message = f"{modified_content} = [{final_total}]"

        is_simple_d100 = re.fullmatch(r"(\d*)[dD]100", content.strip())
        if not has_operator and is_simple_d100 and len(replacements) == 1:
            first_dice_count = int(is_simple_d100.group(1) or 1)
            if first_dice_count == 1:
                first_roll_value = list(expression_values.values())[0]
                if first_roll_value == 100:
                    final_message += get_localized_text(user_id, 'critical')
                elif first_roll_value == 1:
                    final_message += get_localized_text(user_id, 'fumble')

        await message.channel.send(final_message)

# Start the bot
client.run(TOKEN)
