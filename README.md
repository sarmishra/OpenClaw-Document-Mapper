# OpenClaw Tax Document Mapper

A learning project exploring **OpenClaw** — the open-source autonomous AI agent platform — to understand agentic AI patterns and validate architecture decisions for building AI-powered business automation systems.

This project demonstrates how OpenClaw connects to Claude (via AWS Bedrock) to perform intelligent tax document analysis: identifying document types, extracting fields, and mapping them to the correct IRS Form 1040 lines — all through natural language interaction.

---

## What Is OpenClaw?

[OpenClaw](https://openclaw.ai) is a free, open-source autonomous AI agent platform that runs on your own infrastructure. It connects to AI models (Claude, GPT, or local models) and executes real-world tasks through messaging platforms and a web dashboard.

Key characteristics:
- Self-hosted — your data stays on your infrastructure
- Model-agnostic — works with Anthropic Claude, OpenAI GPT, or local models via Ollama
- Skills platform — extend capabilities with custom or community skills
- Multi-channel — accessible via WhatsApp, Telegram, Slack, Discord, or web chat
- Cron jobs — schedule recurring autonomous tasks
- Open source (MIT license) — 310k+ GitHub stars

---

## Project Overview

This project uses OpenClaw connected to **Claude via AWS Bedrock** to:

1. Accept a tax document (W2, 1099-INT, 1099-DIV, or IRS Schedules A/B/C/D)
2. Identify the document type automatically
3. Extract all labeled fields and their values
4. Map each field to the correct destination line on IRS Form 1040
5. Return a structured result with confidence rating and notes

The goal was to validate two things:
- How well OpenClaw handles document understanding tasks through its chat interface
- Where OpenClaw fits (and doesn't fit) in a production B2B architecture

---

## Architecture

```
User (web chat or messaging app)
        ↓
OpenClaw Gateway (self-hosted on AWS Lightsail)
        ↓
Claude via AWS Bedrock (claude-sonnet-4-6)
        ↓
Agent reasoning loop
  → Identifies document type
  → Extracts all fields
  → Maps fields to Form 1040 lines
        ↓
Structured JSON response returned to user
```

---

## Setup

### Prerequisites

- AWS account with Bedrock access enabled
- Claude Sonnet model access approved in Bedrock
- AWS Lightsail access (or any Linux VPS)

### Step 1 — Create the Lightsail Instance

```bash
aws lightsail create-instances \
  --instance-names openclaw-tax-mapper \
  --availability-zone us-east-1a \
  --blueprint-id openclaw \
  --bundle-id medium_3_0
```

Wait until the instance status shows `running`:

```bash
aws lightsail get-instance-state \
  --instance-name openclaw-tax-mapper
```

### Step 2 — Enable Bedrock Access

Create an IAM role allowing the Lightsail instance to call Bedrock:

```bash
# Create the role
aws iam create-role \
  --role-name OpenClawBedrockRole \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Principal": { "Service": "lightsail.amazonaws.com" },
      "Action": "sts:AssumeRole"
    }]
  }'

# Attach Bedrock access policy
aws iam put-role-policy \
  --role-name OpenClawBedrockRole \
  --policy-name BedrockAccess \
  --policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream",
        "bedrock:ListFoundationModels",
        "bedrock:GetFoundationModel"
      ],
      "Resource": "*"
    }]
  }'
```

Then attach the role to your Lightsail instance via the AWS Console:
- Lightsail → Instance → Getting started tab → Enable Amazon Bedrock → run the provided CloudShell script

### Step 3 — Pair Your Browser

1. SSH into the instance via Lightsail console
2. Note the dashboard URL and pairing token from the welcome message
3. Open the dashboard URL in your browser
4. Enter the pairing token
5. You are now connected to the OpenClaw dashboard

### Step 4 — Verify the Connection

In the OpenClaw chat, type:

```
What model are you running on and what AWS region are you in?
```

Expected response: confirms Claude via Amazon Bedrock and your configured region.

---

## Usage — Tax Document Mapping

### Method 1 — Image Input (Paste Screenshot)

Take a screenshot of your tax document PDF and paste it directly into the chat input box. Then ask:

```
This is a tax document. Identify the type, list every 
field and value you can see, and tell me which line 
on Form 1040 each field maps to.
```

### Method 2 — Text Input (Extract and Paste)

Extract text from your PDF locally:

```python
import pdfplumber

with pdfplumber.open("your_document.pdf") as pdf:
    for page in pdf.pages:
        print(page.extract_text())
```

Paste the extracted text into the chat:

```
Below is text extracted from a tax document PDF.
Identify the document type, extract every field 
and value, then map each field to the correct 
Form 1040 line:

[paste extracted text here]
```

### Supported Document Types

| Document | Maps To |
|---|---|
| W2 | Form 1040 Line 1a, 25a, Schedule 2 |
| 1099-INT | Form 1040 Line 2b, Schedule B |
| 1099-DIV | Form 1040 Line 3a/3b, Schedule B |
| Schedule A | Form 1040 Line 12a |
| Schedule B | Form 1040 Lines 2b, 3b |
| Schedule C | Form 1040 Line 8, Schedule SE |
| Schedule D | Form 1040 Line 7 |

---

## Example Output

Input: W2 document screenshot

Output from Claude via OpenClaw:

```
Document Type: W-2 (Wage and Tax Statement)
Tax Year: 2025

Field Mappings:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Box 1  Wages ($72,500)    → Form 1040 Line 1a
Box 2  Fed Tax ($11,200)  → Form 1040 Line 25a
Box 3  SS Wages ($72,500) → SSA verification only
Box 4  SS Tax ($4,495)    → Schedule 3 Line 11
Box 5  Medicare ($72,500) → Form 8959 if applicable
Box 6  Med Tax ($1,051)   → Informational
Box 12 Code E ($2,500)    → SIMPLE IRA — informational
Box 12 Code DD ($6,200)   → Health coverage — informational
Box 17 State Tax ($0)     → TX has no state income tax

Confidence: HIGH
Notes:
- All numeric extractions internally consistent
- Texas has no state income tax — Box 17 correctly zero
- Code E 401k deferral below 2025 limit of $13,500
```

---

## Experiments and Learnings

### Experiment 1 — Setup Verification
Confirmed model, region, and available tools. Internet access is blocked in the Lightsail sandbox by default — Claude answers from training data only.

### Experiment 2 — Document Understanding
Claude correctly identified W2 document type, extracted all fields, and mapped them to Form 1040 lines from a screenshot. Quality comparable to a structured Lambda implementation.

### Experiment 3 — Multi-Step Reasoning
Tested sequential step-by-step processing with user confirmation between steps. OpenClaw handles multi-step tasks well — relevant for chaining business workflow components.

### Experiment 4 — Skill Creation
Explored OpenClaw's skill structure. Skills define inputs, outputs, and logic — conceptually equivalent to Lambda function tools in a Bedrock agent setup.

### Experiment 5 — Scheduled Tasks
OpenClaw's Cron Jobs feature supports recurring autonomous tasks — useful for future document monitoring automation (e.g. check client inbox daily, process new documents automatically).

### Experiment 6 — Security / Prompt Injection
Tested prompt injection via document content. Claude correctly identified and ignored embedded instructions, treating all document content as data only. Behavior is model-dependent — explicit system prompt rules improve consistency.

---

## Key Findings

### What OpenClaw Does Well
- Fast experimentation with agent patterns — no code required
- Natural language task definition — describe what you want, agent figures out how
- Scheduled background tasks out of the box
- Multi-channel — same agent accessible from Telegram, Slack, or web
- Good for personal automation and single-user business tasks

### Limitations for B2B Production Use
- No native multi-tenancy — one agent instance per user/team
- Known security vulnerabilities (CVE-2026-25253) — not suitable for sensitive client data without additional hardening
- File upload in web chat UI limited by version — PDF handling requires workarounds
- Community skill marketplace has reported malicious skills — only use internally verified skills
- Internet access blocked in Lightsail sandbox by default

### Architecture Recommendation
| Use Case | Recommended Approach |
|---|---|
| Personal productivity automation | OpenClaw — fast, zero-code |
| Team internal workflows | OpenClaw with private skills |
| B2B SaaS with client data | Lambda as agent (Bedrock tool_use) |
| Document intake pipeline | S3 trigger → Lambda → DynamoDB |
| Client-facing interaction | Custom web app or Claude Cowork |

---

## Form Field Mapping Reference

A complete field-level mapping spreadsheet covering all 7 document types is included in this repo at `reference/form_mappings.xlsx`.

| Sheet | Coverage |
|---|---|
| W2 | All 20 boxes → Form 1040 destination |
| 1099-INT | All 17 boxes including tax-exempt interest and AMT |
| 1099-DIV | All boxes including Section 199A and collectibles |
| Schedule A | All deduction lines with SALT cap note |
| Schedule B | Interest and dividend totals with FBAR note |
| Schedule C | Business income with Schedule SE flow |
| Schedule D | Capital gain/loss with 1040 Line 7 routing |

---

## Project Structure

```
/
├── README.md                          ← this file
├── reference/
│   └── form_mappings.xlsx             ← complete field mapping reference
├── samples/
│   ├── sample_w2.pdf                  ← synthetic W2 test document
│   └── sample_1099_int.pdf            ← synthetic 1099-INT test document
└── scripts/
    └── generate_test_docs.py          ← generates synthetic test PDFs
```

---

## Generating Synthetic Test Documents

To generate your own synthetic test PDFs for experimentation:

```bash
pip install reportlab
python scripts/generate_test_docs.py
```

Generates:
- `sample_w2.pdf` — clean W2 with no VOID flag, realistic field values
- `sample_1099_int.pdf` — 1099-INT with non-zero interest, backup withholding, and tax-exempt interest

All documents are clearly marked as synthetic test data — not real taxpayer information.

---

## Cost

| Resource | Cost |
|---|---|
| Lightsail 4GB instance | ~$20/month |
| Bedrock Claude Sonnet | ~$3-15 per million tokens |
| Typical document mapping | ~3,000-5,000 tokens (~$0.01-0.03 per document) |

**Tip:** Stop the Lightsail instance when not in use to avoid unnecessary charges. The instance retains all configuration when restarted.

```bash
aws lightsail stop-instance --instance-name openclaw-tax-mapper
aws lightsail start-instance --instance-name openclaw-tax-mapper
```

---

## Related Resources

- [OpenClaw Official Site](https://openclaw.ai)
- [OpenClaw GitHub](https://github.com/openclaw/openclaw)
- [OpenClaw Docs](https://docs.openclaw.ai)
- [AWS Lightsail OpenClaw Guide](https://docs.aws.amazon.com/lightsail/latest/userguide/amazon-lightsail-quick-start-guide-openclaw.html)
- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock)
- [IRS Form 1040 Instructions](https://www.irs.gov/forms-pubs/about-form-1040)

---

## License

MIT — feel free to use, adapt, and share.

---

*Built as a learning project to explore agentic AI patterns and validate architecture decisions for AI-powered business automation.*
