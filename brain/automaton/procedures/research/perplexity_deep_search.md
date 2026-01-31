# Procedure: Perplexity Deep Search

## When to Use
- Mike asks for research on a topic
- Need current information (last 24-48 hours)
- Need comprehensive analysis with sources

## Steps

1. **Formulate Query**
   - Be specific about the topic
   - Include time constraints if needed
   - Specify industry/domain focus

2. **Call Perplexity API**
   ```bash
   curl -s "https://api.perplexity.ai/chat/completions" \
     -H "Authorization: Bearer $PERPLEXITY_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
       "model": "sonar",
       "messages": [
         {"role": "system", "content": "You are a research analyst. Be specific and cite sources."},
         {"role": "user", "content": "[YOUR QUERY]"}
       ]
     }'
   ```

3. **Save Results**
   - Create file in `brain/research/YYYY-MM-DD-topic.md`
   - Include raw findings + analysis
   - Note sources and relevance

4. **Synthesize for Mike**
   - Extract key insights
   - Connect to ShopTalk/FactoryLM if relevant
   - Identify actionable items

5. **Send Voice + Text**
   - Generate TTS summary
   - Include detailed text with links

## Success Criteria
- Research saved to brain/research/
- Voice message sent
- Text with full details sent
- Relevant to Mike's question

## Common Pitfalls
- API rate limiting (1 req/sec on free tier)
- Forgetting to save to file
- Not connecting findings to business context

## Examples
- 2026-01-31: Edge AI competitive landscape
- 2026-01-31: Modbus register templates
- 2026-01-31: Emerging tech scan
