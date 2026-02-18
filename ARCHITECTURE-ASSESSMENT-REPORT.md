# Documentation Generation Architecture Assessment & Recommendation Request

**Date:** January 16, 2026  
**Project:** EVA Foundation - Documentation Generator  
**Author:** GitHub Copilot (AI Assistant)  
**Audience:** Technical Leadership, Solutions Architects, AI/ML Engineers

---

## 1. Problem Statement

### 1.1 The Challenge

We need to generate **28 technical documentation files** (architecture, ConOps, security, operational) for the EVA Foundation project. These documents must:

- **Reflect actual codebase implementation** (not speculative or aspirational)
- **Maintain consistency** across multiple generation runs (deterministic output)
- **Pass validation** (YAML frontmatter, requirement traceability, structure)
- **Be AI-consumable** (structured tables, explicit references, command examples)

### 1.2 Core Problem: Low Consistency

**Current Performance:**
- **Run J (Baseline):** 28/28 files, 100% validation pass, 11m 20s
- **Run K (Retest):** 25/28 files, 57.16% consistency vs Run J
- **Critical Issue:** At temperature 0.3, identical inputs produce significantly different outputs

**Consistency Breakdown (Run K vs Run J):**
```
Identical files:        0 / 28 (0%)
Similar (>80%):         1 / 28 (4%)
Different (<80%):      24 / 28 (96%)
Missing:                3 / 28 (files failed generation)
```

**Root Cause Hypothesis:** Template-based generation without grounding in actual codebase creates hallucination and variance.

---

## 2. What We Have: Source Materials

### 2.1 One-Year-Old Baseline Documents

**Source:** `docs/Information Assistant - Architecture Document v1.0.pdf` (1 year old)

**Canonical v0.2 Extracted Requirements:**
- Located: `docs/eva-foundation/source-materials/requirements-v0.2/*.md`
- Files:
  - `00_source_summary.md` - Technical Design & ConOps summary
  - `01_scope_and_context.md` - System boundaries and context
  - `02_architecture_principles.md` - Design principles
  - `03_eva_chat_requirements.md` - EVA Chat component requirements
  - `04_eva_da_requirements.md` - EVA Domain Assistant requirements
  - `05_security_audit_ops.md` - Security, audit, operational requirements
  - `06_testing_prioritization.md` - Testing strategies

**Content:** These define **architectural intent** from original design, NOT current implementation.

**Example Requirement IDs:**
- `INF01`, `INF02` - Information architecture requirements
- `ACC01`, `ACC02` - Accessibility requirements
- `IT01-DA`, `IT02-DA` - Security access control for Domain Assistant
- `IOP01`, `IOP02` - Operational requirements

**Authority:** Approved by Enterprise Architecture Review Board (EARB) January 29, 2025.

### 2.2 Actual Repository (Source of Truth)

**Implementation Reality:**
- **Backend:** Python/Quart async API (`app/backend/`)
  - RAG implementation: `approaches/chatreadretrieveread.py`
  - Authentication: `auth/` with Entra ID OAuth 2.0
  - Azure integrations: OpenAI, AI Services, Cognitive Search, Cosmos DB
- **Frontend:** React/TypeScript (`app/frontend/`)
- **Document Pipeline:** Azure Functions (`functions/`)
- **Infrastructure:** Terraform (`infra/`)

**Key Pattern Found:** Production RAG approach uses:
1. `optimize_query()` - GPT rewrites query with language detection
2. `hybrid_search()` - Vector + keyword search via Azure Cognitive Search
3. `generate()` - Streaming GPT response with citations
4. **Fallback flags:** `OPTIMIZED_KEYWORD_SEARCH_OPTIONAL`, `ENRICHMENT_OPTIONAL`

**Gap:** v0.2 PDF describes design intent; actual repo has evolved significantly over 1 year.

---

## 3. What We Tested: Template-Based Generator

### 3.1 Architecture (Original Approach)

**Implementation:** `docs/eva-foundation/projects/01-documentation-generator/src/generator.py`

**Workflow:**
```
1. Load system prompt (docs/eva-foundation/README.md)
2. Load exemplar document (prompts/example-architecture-doc.md)
3. Parse file specifications (workspace-notes/file-generation-oneliner.md)
4. For each file:
   a. Build prompt: system_prompt + exemplar + one-line instruction
   b. Call Azure OpenAI (gpt-4.1-mini, temp 0.3)
   c. Validate output (validators.py)
   d. Retry up to 3 times if validation fails
5. Track evidence (evidence.py)
```

**Key Components:**

- **System Prompt:** 1,500+ line document defining role, constraints, output format
- **Exemplar:** Example document showing exact YAML frontmatter + markdown structure
- **Validators:**
  - YAML frontmatter (document_type, phase, audience, traceability)
  - Requirement IDs (regex: `[A-Za-z0-9\-]+`)
  - Traceability anchors (accepts `#INF01`, `#IT01-DA`, `#Backup-&-Recovery`)
  - Structure (headings, sections)

**LLM Configuration:**
```python
temperature: 0.3        # Low for consistency
max_tokens: 4000
model: gpt-4.1-mini
timeout: 300 seconds
```

**Actual Azure OpenAI API Request Payload:**
```json
{
  "messages": [
    {
      "role": "system",
      "content": "<1500+ line system prompt from README.md>"
    },
    {
      "role": "user",
      "content": "Source files for reference:\n\n<v0.2 source context>\n\nConfirm..."
    },
    {
      "role": "assistant",
      "content": "Ready"
    },
    {
      "role": "user",
      "content": "You MUST follow this EXACT format:\n\n---BEGIN EXEMPLAR---\n<example-architecture-doc.md>\n---END EXEMPLAR---\n\nHARD FORMAT RULES...\n\nNow generate: security-architecture.md\n\nPrompt: <one-line instruction>\n\nPhase: 4\n\nSource files for reference:\n<v0.2 source context>"
    }
  ],
  "temperature": 0.3,
  "max_tokens": 4000,
  "timeout": 300,
  "request_timeout": 300
}
```

**Fields Currently Used:**
- ✅ `messages` - Conversation history (system + user)
- ✅ `temperature` - 0.3 (low variance)
- ✅ `max_tokens` - 4000 (response limit)
- ✅ `timeout` / `request_timeout` - 300s (VPN stability)

**Fields NOT Currently Used (Could Improve Repeatability):**
- ❌ `seed` - Deterministic sampling (OpenAI supports this)
- ❌ `top_p` - Nucleus sampling parameter (defaults to 1.0)
- ❌ `frequency_penalty` - Reduce token repetition (defaults to 0.0)
- ❌ `presence_penalty` - Encourage topic diversity (defaults to 0.0)
- ❌ `n` - Number of completions (defaults to 1)
- ❌ `stream` - Streaming mode (could add progress visibility)

**Note:** LangChain's `AzureChatOpenAI` wrapper abstracts the actual HTTP request to Azure OpenAI's REST API at:
```
POST https://<REDACTED>.openai.azure.com/openai/deployments/gpt-4.1-mini/chat/completions?api-version=2024-02-15-preview
Authorization: Bearer <REDACTED>
Content-Type: application/json
```

### 3.2 Test Results

**Run J (Success Baseline):**
```
Files:              28/28 (100%)
Duration:           11m 20s
Validation:         All passed
Fixes applied:      10 (exemplar alignment, deduplication, validation improvements)
Status:             First error-free run
```

**Run K (Consistency Test):**
```
Files:              25/28 (89%)
Consistency vs J:   57.16%
Identical:          0/28 (0%)
Similar (>80%):     1/28 (4%)
Different (<80%):   24/28 (96%)
Status:             NOT production-ready (<70% threshold)
```

**Content Similarity Samples:**
| File | Overall | Structural | Content | Status |
|------|---------|-----------|---------|--------|
| audit-and-logging.md | 82.3% | 100% | 64.6% | Similar |
| physical-architecture.md | 79.1% | 100% | 58.2% | Different |
| security-architecture.md | 64.7% | 75% | 44.5% | Different |
| executive-summary.md | 39.7% | 65% | 40.4% | Different |
| change-and-release.md | 33.3% | 48.5% | 37.6% | Different |

**Analysis:** Even at temperature 0.3, template-based generation produces significant variance. YAML frontmatter and structure mostly consistent, but **content differs substantially**.

---

## 4. What We Created: Agent Skills Framework Approach

### 4.1 New Architecture (Skills-Based)

**Hypothesis:** Grounding generation in **actual codebase evidence** will reduce hallucination and improve consistency.

**Implementation:** `docs/eva-foundation/projects/02-poc-agent-skills/`

**Three-Skill Workflow:**

```
┌─────────────────────────────┐
│  RepoResearcherSkill        │
│  - Searches codebase        │
│  - Finds evidence files     │
│  - Extracts config values   │
└──────────┬──────────────────┘
           │ Evidence Dict
           ▼
┌─────────────────────────────┐
│  DeltaGeneratorSkill        │
│  - Loads baseline v0.2      │
│  - Compares to evidence     │
│  - Updates ONLY changed     │
└──────────┬──────────────────┘
           │ Generated Doc
           ▼
┌─────────────────────────────┐
│  ValidationOrchestratorSkill│
│  - Runs validators          │
│  - Retries with feedback    │
│  - Max 3 attempts           │
└─────────────────────────────┘
```

**Orchestration:** `orchestrator/documentation_workflow.py` chains all three skills with state persistence.

### 4.2 Component Details

#### 4.2.1 RepoResearcherSkill

**Purpose:** Find code evidence relevant to documentation topic.

**Configuration:** `skill-manifests/repo-researcher.yaml`
```yaml
search_paths:
  - app/backend
  - app/frontend
  - functions
  - infra
excluded_paths:
  - "**/node_modules"
  - "**/.venv"
  - "**/test_data"
search_strategy:
  semantic_search_weight: 0.4
  file_search_weight: 0.3
  grep_search_weight: 0.3
```

**Methods:**
- `_semantic_search()` - Conceptual understanding [**PLACEHOLDER - NOT IMPLEMENTED**]
- `_file_search()` - File pattern matching [Uses `Path.glob()`]
- `_grep_search()` - Text pattern search [**PLACEHOLDER - NOT IMPLEMENTED**]
- `_extract_config_values()` - Parse JSON/YAML/.env files

**Output:**
```python
{
  "files_found": ["app/backend/auth/auth.py", ...],
  "config_values": {"AZURE_OPENAI_ENDPOINT": "...", ...},
  "search_summary": "Found 15 files related to authentication",
  "confidence_score": 0.85  # ⚠️ PROBLEM: Calculated in researcher
}
```

**Issues Identified:**
1. ❌ Tool methods are **placeholders** (not real implementations)
2. ❌ Calculates **confidence score** (should be generator's responsibility)
3. ❌ Role confusion: researcher should find, not judge relevance

#### 4.2.2 DeltaGeneratorSkill

**Purpose:** Generate documentation using baseline v0.2 + repo evidence.

**Configuration:** `skill-manifests/delta-generator.yaml`
```yaml
baseline_dir: "../../01-documentation-generator/source-docs-v0.2"  # ⚠️ Path not found
output_dir: "../../01-documentation-generator/generated-output-skills"
temperature: 0.3
max_tokens: 4000
```

**Workflow:**
1. `_load_baseline_document()` - Load v0.2 source file
2. `_parse_sections()` - Split markdown by headings
3. `_analyze_section_relevance()` - Compare section to evidence
4. `_generate_updated_section()` - Call Azure OpenAI for updates
5. `_build_delta_prompt()` - Create context-aware prompt

**Delta Logic:**
```python
for section in baseline["sections"]:
    relevance = _analyze_section_relevance(section, evidence)
    if relevance["needs_update"]:
        updated = _generate_updated_section(section, evidence, relevance)
        mark_as("UPDATED")
    else:
        mark_as("UNCHANGED")
```

**Issues Identified:**
1. ⚠️ Baseline path `source-docs-v0.2/` **does not exist** (no v0.2 markdown files found)
2. ⚠️ Calculates relevance (correct role) but relies on researcher's confidence (wrong)

#### 4.2.3 ValidationOrchestratorSkill

**Purpose:** Validate generated docs with retry logic.

**Configuration:** `skill-manifests/validation-orchestrator.yaml`
```yaml
max_retries: 3
strict_mode: true
enabled_validators:
  - frontmatter
  - requirement_ids
  - traceability
  - structure
```

**Implementation:**
- Imports from `../../01-documentation-generator/src/validators.py`
- `execute_with_retry()` - 3-attempt loop with regeneration callback
- Provides detailed feedback for corrections

**Issues Identified:**
1. ⚠️ `VALIDATORS_AVAILABLE` may be False if import path incorrect
2. ✅ Retry logic correctly implemented

### 4.3 What Would Feed the Workflow

**Inputs:**
```bash
python orchestrator/documentation_workflow.py \
    --file security-architecture.md \
    --topic "security architecture authentication authorization" \
    --scope backend \
    --search-terms OAuth PKCE "Entra ID" azure_credential
```

**Search Sources:**
- **Codebase files:** `app/backend/**/*.py`, `app/frontend/**/*.tsx`
- **Configuration:** `backend.env`, `local.settings.json`, Terraform `*.tf`
- **Infrastructure:** `infra/**/*.tf` (VNet, private endpoints, RBAC)
- **Baseline v0.2:** `source-materials/requirements-v0.2/*.md` (architectural intent)

**Expected Evidence:**
```python
{
  "files_found": [
    "app/backend/auth/auth.py",
    "app/backend/auth/auth_utils.py",
    "app/backend/approaches/chatreadretrieveread.py",
    "infra/core/security/keyvault.tf",
    "backend.env"
  ],
  "config_values": {
    "AZURE_OPENAI_ENDPOINT": "https://<name>.openai.azure.com",
    "AZURE_TENANT_ID": "<guid>",
    "USE_AUTHENTICATION": "true"
  },
  "code_snippets": [
    "# File: app/backend/auth/auth.py:45-60",
    "async def get_authenticated_user_details(...):"
  ]
}
```

**Delta Generation:**
- Load baseline: `source-docs-v0.2/security-architecture.md` [**❌ DOES NOT EXIST**]
- Compare: Baseline section "Authentication" vs evidence from `auth/auth.py`
- Generate: If mismatch (e.g., baseline says "OAuth 2.0" but code shows "Entra ID + PKCE"), update section
- Preserve: If match (e.g., baseline says "Private endpoints" and `infra/` confirms), keep unchanged

---

## 5. Critical Issues Discovered

### 5.1 Implementation Problems

1. **❌ Missing Baseline Documents**
   - Path: `source-docs-v0.2/` referenced in config
   - Reality: Directory does not exist
   - Impact: DeltaGeneratorSkill cannot load baseline

2. **❌ Tool Placeholders Not Implemented**
   - `_semantic_search()`: Returns empty list
   - `_grep_search()`: Returns empty list
   - Impact: RepoResearcherSkill cannot find evidence

3. **❌ Role Separation Violation**
   - RepoResearcherSkill calculates confidence score
   - Should be: Researcher finds, Generator decides relevance
   - Impact: Violates single-responsibility principle

4. **❌ No Research of Best Practices**
   - Agent invented workflow without validating against industry patterns
   - Did not adapt existing `ChatReadRetrieveReadApproach` from codebase
   - Did not research GitHub documentation generation workflows
   - Impact: Architecture may not follow proven patterns

5. **❌ Dry-Run Support Missing**
   - User requested `--dry-run` flag to preview workflow
   - Not implemented in any skill
   - Impact: Cannot test without LLM calls

### 5.2 Not Tested Yet

The Agent Skills Framework implementation (~2,500 lines) has **NOT been tested**:
- ❌ No end-to-end workflow execution
- ❌ No file successfully generated
- ❌ No consistency comparison performed
- ❌ No validation against Run J baseline

---

## 6. Recommendation Request

### 6.1 Architecture Questions

**A. Multi-Agent Workflow Design**

We implemented a **3-skill sequential workflow** (Researcher → Generator → Validator). Questions:

1. Is this pattern validated in industry? (e.g., LangChain, LangGraph, AutoGPT)
2. Should we use **ReAct** (Reasoning + Acting) pattern instead?
3. Should we use **Plan-Execute-Reflect** with iterative refinement?
4. Is **3-agent** the right number, or should we decompose further?
5. Should skills run **sequentially** or support **parallel branches**?

**B. RAG Adaptation**

Our codebase has a production RAG pattern (`chatreadretrieveread.py`):
```python
optimized_query = optimize_query(user_query)  # GPT rewrites query
embedding = generate_embedding(optimized_query)  # Vector embedding
results = hybrid_search(embedding, keywords)  # Vector + keyword search
response = generate(results)  # GPT with sources
```

Questions:
1. Should we **adapt this pattern** for documentation generation?
2. Replace `hybrid_search()` with `repo_search()`?
3. Replace `generate()` with `delta_generate(baseline, evidence)`?
4. Keep the **fallback flags** pattern for robustness?

**C. Baseline Source**

We have two potential baselines:
- **Option 1:** v0.2 PDF-extracted markdown files (architectural intent from 1 year ago)
- **Option 2:** Run J output (28 generated files, validated, but may contain hallucinations)

Questions:
1. Which should be the authoritative baseline?
2. Should we create a **hybrid baseline** (v0.2 intent + Run J structure)?
3. How to handle **implementation drift** (code evolved beyond v0.2)?

### 6.2 Quality Metrics & Assessment

**Current Comparison Methodology:**
```python
# compare_outputs.py uses:
structural_score = compare_yaml_frontmatter() * 0.3  # 30% weight
content_score = difflib.SequenceMatcher(a, b).ratio() * 0.5  # 50% weight
traceability_score = compare_requirement_refs() * 0.2  # 20% weight
overall_score = structural_score + content_score + traceability_score
```

**Thresholds:**
- Identical: ≥95%
- Similar: 80-95%
- Different: <80%
- Production-ready: ≥70% consistency

**Questions:**

1. **Are these metrics appropriate?**
   - Is 70% consistency threshold valid for technical documentation?
   - Should we weight content similarity higher than 50%?
   - Should we measure **semantic similarity** (embeddings) instead of character-level?

2. **What metrics are missing?**
   - **Factual accuracy:** How to verify claims match actual code?
   - **Completeness:** How to measure coverage of all requirements?
   - **Traceability coverage:** Percentage of requirements with evidence?
   - **Readability:** Flesch-Kincaid, Gunning Fog Index?
   - **AI consumability:** Do tables have headers? Code blocks have language tags?

3. **How to assess hallucination?**
   - Should we run **fact-checking LLM calls** against codebase?
   - Should we implement **chain-of-thought verification**?
   - Should we require **citations for every claim**?

4. **Industry benchmarks?**
   - What consistency scores do production doc generators achieve?
   - Are there published benchmarks for RAG-based documentation?

5. **Comparison methodology?**
   - Should we compare **N runs against each other** (all-pairs)?
   - Or compare **all runs against single baseline** (Run J)?
   - Should we use **Levenshtein distance** instead of `difflib`?
   - Should we implement **structural diff** (AST-level for YAML)?

### 6.3 Validation & Testing Strategy

**Questions:**

1. **What should we test first?**
   - Single file end-to-end workflow?
   - Individual skill in isolation?
   - Comparison against Run J baseline?

2. **How many runs to establish consistency?**
   - Current: 2 runs (J vs K)
   - Recommended: 3? 5? 10?

3. **Should we implement unit tests?**
   - Test each skill's `execute()` method independently?
   - Mock LLM responses for deterministic testing?

4. **How to validate evidence quality?**
   - Is 15 files enough? Too many?
   - Should we have minimum/maximum evidence thresholds?
   - Should we score evidence **relevance** before generation?

---

## 7. Immediate Next Steps (Pending Recommendations)

**Option A: Fix Current Implementation**
1. Research GitHub multi-agent documentation patterns
2. Implement real tool integration (not placeholders)
3. Create baseline v0.2 markdown files from source materials
4. Fix role separation (move confidence to generator)
5. Add dry-run support
6. Test end-to-end with security-architecture.md
7. Compare 2 runs for consistency

**Option B: Redesign Based on RAG Pattern**
1. Adapt `chatreadretrieveread.py` approach
2. Create `DocumentationRAGApproach` class
3. Implement `repo_search()` replacing `hybrid_search()`
4. Implement `delta_generate()` with baseline + evidence
5. Keep fallback flags pattern
6. Test with Run J as baseline

**Option C: Research-First Approach**
1. Fetch GitHub repos for multi-agent doc generation
2. Analyze LangGraph, CrewAI, AutoGPT patterns
3. Document best practices
4. Redesign architecture based on findings
5. Implement with proven patterns
6. Test against industry benchmarks

---

## 8. Questions for Expert Review

1. **Have you seen similar documentation generation challenges?** What patterns worked?

2. **Is the 3-skill workflow (Researcher → Generator → Validator) standard?** Or should we use different decomposition?

3. **How to measure documentation quality objectively?** Beyond consistency, what metrics matter?

4. **Should we prioritize consistency or accuracy?** If v0.2 baseline is wrong, should we preserve it (consistent) or fix it (accurate)?

5. **How to handle 1-year implementation drift?** Code evolved beyond v0.2 design - document as-is or align to original intent?

6. **What tools exist for this?** Should we use existing frameworks (Docusaurus, MkDocs, Sphinx with AI plugins) instead of building custom?

7. **Is LLM-based generation the right approach?** Or should we use **extraction** (parse code → generate docs from AST)?

---

**Status:** Awaiting recommendations before proceeding with testing or redesign.

**Contact:** This report generated by GitHub Copilot AI Assistant in conversation with user.
