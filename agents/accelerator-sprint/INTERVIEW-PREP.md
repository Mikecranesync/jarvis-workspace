# YC INTERVIEW PREP - FACTORYLM
*Industrial AI / Predictive Maintenance Focus*

---

## EXECUTIVE SUMMARY

FactoryLM is building the AI-first industrial predictive maintenance platform for SME manufacturers. We're creating a hierarchical AI architecture (edge → local → cloud) that converts maintenance insights into executable code, moving intelligence as close to factory equipment as possible.

**Key Positioning**: "Like Palantir for factory maintenance, but designed for SMEs instead of enterprises."

---

## TOP 20 LIKELY QUESTIONS & FACTORYLM-SPECIFIC ANSWERS

### 1. What is your company working on?
**Answer**: "FactoryLM is an AI-first predictive maintenance platform for small and medium manufacturers. We use a hierarchical AI architecture - edge devices, local GPU processing, and cloud - to predict equipment failures before they happen and convert those insights into executable maintenance code. Think like Palantir for factory maintenance, but designed for SMEs instead of enterprises."

### 2. What problem are you solving?
**Answer**: "Manufacturing downtime costs SMEs $50B annually. Current solutions like IBM Maximo cost $300K+ and take 18 months to implement. Meanwhile, 70% of SME factories still use paper-based maintenance. We're building the first AI-native solution that can be deployed in days, not months, starting at $500/month."

### 3. Why now?
**Answer**: "Three converging factors: 1) Edge AI hardware like Raspberry Pi now has enough compute for real-time inference, 2) SME manufacturers are facing a skilled technician shortage - 2M unfilled jobs by 2025, and 3) Modern LLMs can finally convert maintenance insights into executable code, which wasn't possible even 2 years ago."

### 4. How do you make money?
**Answer**: "SaaS model starting at $500/month for basic predictive maintenance, scaling to $5K/month for multi-facility deployments. We also charge $2K for hardware deployment and $50/hour for custom integrations. Our pilot customers are paying $1,200/month average."

### 5. Who are your customers?
**Answer**: "SME manufacturers with $5-50M revenue who have critical equipment but can't afford enterprise solutions. Our sweet spot is metal fabrication, food processing, and automotive parts suppliers. They typically have 20-200 pieces of equipment and lose $10K+ per unplanned downtime event."

### 6. What's your competitive advantage?
**Answer**: "We're the only solution that runs AI inference at the edge while automatically generating maintenance code. Competitors either require cloud connectivity (unreliable in factories) or need expensive on-site technicians. Our hierarchical architecture means intelligence flows downward - we convert AI insights into executable scripts that factory workers can run."

### 7. How big is the market?
**Answer**: "SME manufacturing maintenance is a $120B market. Just in the US, there are 250,000 manufacturing facilities with $5-50M revenue. If we capture 1% at $5K average annual contract value, that's $125M ARR opportunity in our initial target market."

### 8. What traction do you have?
**Answer**: "We have 5 pilot customers paying an average of $1,200/month. Our best customer, a metal fabrication shop, reduced unplanned downtime by 40% and increased their equipment effectiveness score from 65% to 82%. We're processing data from 127 pieces of equipment across these pilots."

### 9. Who are your competitors?
**Answer**: "Traditional: IBM Maximo, Siemens MindSphere - too expensive and complex for SMEs. Modern: Augury, Senseye - cloud-only solutions that don't work well in factory environments. We're differentiated by our edge-first architecture and code generation capabilities."

### 10. What's your growth strategy?
**Answer**: "Bottom-up adoption through equipment vendors and maintenance contractors. We're partnering with PLC manufacturers like Allen-Bradley and Siemens to bundle our solution with new equipment sales. Word-of-mouth in manufacturing communities is extremely powerful - one success story can generate 5-10 referrals."

### 11. How do customers find you?
**Answer**: "Direct sales through industry conferences, partnerships with equipment OEMs, and referrals from existing customers. We also target maintenance managers on LinkedIn who post about downtime issues. Our CEO has 20 years in manufacturing and strong industry relationships."

### 12. What are your unit economics?
**Answer**: "Customer acquisition cost is $1,500 through direct sales, $500 through partners. Average contract value is $5,000 annually with 95% gross margins after hardware costs. Payback period is 3 months, lifetime value is $25K based on 5-year average retention in manufacturing."

### 13. Why will you win?
**Answer**: "We understand manufacturing operations better than tech companies, and we understand AI better than traditional industrial companies. Our founder spent 20 years in factory operations before building AI systems. We're also the only team combining edge AI with automatic code generation."

### 14. What's your biggest risk?
**Answer**: "Integration complexity - every factory has different equipment brands and protocols. We're mitigating this by focusing on the most common PLCs (Allen-Bradley, Siemens) and building a library of pre-built connectors. We've already solved integration for 15 different equipment types."

### 15. How technical are your customers?
**Answer**: "Maintenance managers typically have trade school education, not CS degrees. That's why our code generation approach works - we translate AI insights into simple scripts they can understand and execute. We provide extensive training and support during onboarding."

### 16. What surprised you about customer behavior?
**Answer**: "Customers care more about avoiding one catastrophic failure than optimizing overall efficiency. A single unplanned shutdown can cost $50K in lost production. They'll pay $5K annually to avoid that risk, even if the ROI isn't perfect on paper."

### 17. How do you handle data privacy/security?
**Answer**: "Everything runs locally by design. Customer data never leaves their facility unless they explicitly opt into cloud features. This is critical for manufacturers with proprietary processes. Our edge devices use military-grade encryption for any external communications."

### 18. What's your 5-year vision?
**Answer**: "To become the operating system for industrial maintenance. Every piece of factory equipment will have an AI agent that predicts failures, schedules repairs, and orders parts automatically. We want to turn reactive maintenance into predictive, autonomous maintenance."

### 19. How do you hire talent?
**Answer**: "We target engineers with both industrial and AI backgrounds - former Tesla factory engineers, ex-GE Digital, people who've worked at the intersection. It's a rare skillset, but we're building a reputation as the place to apply AI to real-world manufacturing problems."

### 20. What would you do with YC funding?
**Answer**: "Hire 3 sales engineers to accelerate customer acquisition and 2 AI engineers to expand our equipment compatibility library. We'd also invest in partnerships with major PLC vendors to embed our solution in their products. Target is 50 customers by demo day."

---

## DIFFICULT QUESTIONS TO PRACTICE

### Technical Depth Questions
- **"Walk me through your AI architecture."**
  - Practice explaining edge AI, model compression, offline inference capabilities
  - Emphasize the hierarchical approach: Pi → Local GPU → Cloud

- **"How do you handle different equipment protocols?"**
  - Discuss OPC-UA, Modbus, Ethernet/IP standards
  - Explain your adapter/connector library approach

- **"What happens when your AI makes wrong predictions?"**
  - Acknowledge false positive/negative rates
  - Explain human oversight and feedback loops
  - Discuss gradual confidence building with customers

### Business Model Challenges
- **"Why won't customers just build this internally?"**
  - SMEs lack AI talent and time
  - Our solution costs less than one engineer's salary
  - Faster time to value than internal development

- **"How do you scale support for complex integrations?"**
  - Partner ecosystem strategy
  - Pre-built connector library
  - Tiered support model

- **"What if a big player like GE copies you?"**
  - They're focused on enterprise customers
  - We have deeper SME relationships and understanding
  - Speed advantage in product iteration

### Market Validation
- **"How do you know SMEs will actually pay for this?"**
  - Point to current pilot revenue
  - Reference pain point validation from 50+ customer interviews
  - Cite industry studies on downtime costs

- **"Is this a vitamin or painkiller?"**
  - Definitively a painkiller - one equipment failure can cost $50K
  - Customers are actively seeking solutions, not being sold
  - High willingness to pay for downtime prevention

### Founder/Team Questions
- **"Why are you the right team for this?"**
  - 20 years manufacturing operations experience
  - Built AI systems at scale
  - Deep understanding of both factory operations and modern AI

- **"What if your key founder/engineer leaves?"**
  - Cross-training and documentation
  - Stock options and vesting schedule aligned
  - Growing team reduces single points of failure

---

## RED FLAGS TO AVOID

### Critical Mistakes That Kill Interviews

#### 1. **Technical Overconfidence**
- ❌ Don't claim 100% accuracy or promise impossible results
- ❌ Don't dismiss concerns about AI reliability in critical systems
- ✅ **Do**: Acknowledge limitations and explain safeguards

#### 2. **Market Size Exaggeration**
- ❌ Don't claim you're addressing a trillion-dollar market
- ❌ Don't ignore the complexity of manufacturing sales cycles
- ✅ **Do**: Focus on realistic TAM and show clear path to first $10M ARR

#### 3. **Underestimating Integration Complexity**
- ❌ Don't say "it's just an API call" when discussing equipment integration
- ❌ Don't ignore the reality of legacy systems in factories
- ✅ **Do**: Show deep understanding of industrial protocols and connectivity challenges

#### 4. **Dismissing Enterprise Competition**
- ❌ Don't say "IBM/GE/Siemens are too slow to compete"
- ❌ Don't ignore their deep customer relationships
- ✅ **Do**: Acknowledge their strengths but clearly differentiate on SME focus and deployment speed

#### 5. **Founder Ego/Conflict**
- ❌ Don't disagree with co-founders in front of partners
- ❌ Don't take all the credit for technical achievements
- ✅ **Do**: Show collaborative decision-making and mutual respect

#### 6. **Overselling the Demo**
- ❌ Don't show fake data or unrealistic scenarios
- ❌ Don't claim your prototype is production-ready
- ✅ **Do**: Be honest about current capabilities and development roadmap

#### 7. **Ignoring Safety Concerns**
- ❌ Don't brush off questions about AI failures in critical systems
- ❌ Don't minimize the importance of human oversight
- ✅ **Do**: Emphasize safety-first design and gradual confidence building

### Behavioral Red Flags

#### Team Dynamics
- Interrupting or contradicting co-founders
- Unclear role division or decision-making authority
- Different vision for company direction

#### Communication Style
- Using excessive jargon without explanation
- Defensiveness when challenged on assumptions
- Inability to simplify complex technical concepts

#### Business Understanding
- Vague understanding of customer needs
- Unrealistic timelines or growth projections
- Lack of clarity on competitive positioning

---

## INDUSTRIAL AI SPECIFIC TALKING POINTS

### Key Industry Context to Reference

#### Manufacturing Labor Crisis
- 2.1M unfilled manufacturing jobs by 2025
- Average factory worker age is 56
- Knowledge transfer crisis as experienced workers retire

#### Technology Adoption in Manufacturing
- 70% of SME manufacturers still use paper-based maintenance
- Average factory equipment is 20+ years old
- IT/OT convergence creating new opportunities

#### Predictive Maintenance ROI
- 25-30% reduction in maintenance costs (industry standard)
- 70-75% reduction in equipment breakdowns
- 35-45% reduction in downtime

### Technical Credibility Builders

#### Edge AI Capabilities
- "We run optimized models on $100 Raspberry Pi devices"
- "Inference happens in <100ms for real-time alerts"
- "No cloud dependency means it works in air-gapped factories"

#### Industrial Integration
- "We support 15 different PLC protocols out of the box"
- "Our system integrates with existing SCADA infrastructure"
- "We've deployed on everything from 1980s equipment to brand new machinery"

#### AI/Manufacturing Intersection
- "We convert sensor anomalies into maintenance work orders"
- "Our models learn each machine's unique failure patterns"
- "We generate Python scripts that factory workers can execute"

---

## DEMO PREPARATION

### 2-Minute Demo Flow

#### 1. **Real Factory Setup** (30 seconds)
- Show actual PLC data streaming from partner factory
- Emphasize this is live production equipment

#### 2. **Predictive Alert** (45 seconds)
- Trigger a real anomaly detection
- Show the AI reasoning and confidence level
- Display automatically generated maintenance recommendation

#### 3. **Code Generation** (30 seconds)
- Show the system generating a Python script
- Explain how this gets executed by factory workers
- Highlight the "intelligence flowing downward" concept

#### 4. **Business Impact** (15 seconds)
- Quick metrics on downtime reduction
- Cost savings calculation

### Demo Talking Points
- "This is live data from a metal fabrication shop in Ohio"
- "The AI detected this bearing failure 3 days before it would have caused shutdown"
- "The generated script guides the technician through exact repair steps"
- "This prevented $23,000 in lost production"

---

## FINAL PREPARATION CHECKLIST

### 24 Hours Before Interview
- [ ] Review all customer metrics and have them memorized
- [ ] Test demo setup and have backup scenarios ready
- [ ] Practice the "What are you working on?" answer until perfect
- [ ] Confirm all co-founders know their role assignments
- [ ] Prepare 3 specific customer success stories

### Day of Interview
- [ ] Start timer at beginning (know you have 10 minutes)
- [ ] Have metrics document open for quick reference
- [ ] Demo loaded and ready to screenshare
- [ ] Calm, confident energy focused on the problem you're solving

### Success Metrics
- **Clarity**: Can explain the business to someone's grandmother
- **Specificity**: Every claim backed by real data or customer examples
- **Confidence**: Excited to tackle the hardest questions about your space
- **Authenticity**: Genuine passion for solving manufacturing problems

---

## REMEMBER THE YC PHILOSOPHY

YC partners want to see:
1. **Smart founders** solving **real problems**
2. **Evidence of customer demand** (even if small)
3. **Ability to iterate and learn** quickly
4. **Technical insights** others don't have
5. **Passion** for the specific problem you're solving

You're not trying to be perfect. You're trying to convince smart investors that you're building something that matters and that you have unique advantages to make it succeed.

**Most importantly**: They're looking for founders who will succeed with or without YC. Show them FactoryLM is inevitable - you just want to get there faster with their help.

---

*Created: February 2026*  
*Last Updated: Feb 6, 2026*  
*Target Batch: YC S26*