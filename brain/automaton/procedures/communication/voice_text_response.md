# Procedure: Voice + Text Response

## When to Use
- Every response to Mike (Constitutional Amendment 2026-01-31)
- Until Mike says to stop

## Steps

1. **Generate TTS**
   ```
   tts(text="Summary of response")
   ```
   - Keep voice message concise (30-60 seconds max)
   - Hit the key points
   - Be conversational

2. **Send Voice First**
   ```
   message(action=send, filePath=..., asVoice=true)
   ```

3. **Send Full Text**
   ```
   message(action=send, message="Full detailed response with formatting")
   ```
   - Include markdown formatting
   - Add links and references
   - Use tables for comparisons
   - Include file paths for saved content

4. **Respond NO_REPLY**
   - Since we used message tool, respond NO_REPLY to avoid duplicate

## Success Criteria
- Voice message sent
- Text message sent
- Both contain consistent information
- Text has more detail than voice

## Common Pitfalls
- Forgetting the voice message
- Making voice too long (>90 seconds)
- Not saying NO_REPLY after sending

## Examples
- All responses to Mike since 2026-01-31 08:39 UTC
