# Agent Skills Framework - Documentation Generator Implementation

## Overview

This is a **working implementation** of the repo-aware delta generation approach using the Agent Skills Framework. It demonstrates how to solve the documentation generator consistency problem by:

1. **Research**: Finding code evidence in the repository
2. **Generate**: Creating documentation using baseline (v0.2) + evidence
3. **Validate**: Ensuring quality with retry logic

## Architecture

```
agent-skills/
├── base/
│   └── agent_skill_base.py          # Base class with Azure OpenAI, state, logging
├── skills/
│   ├── repo_researcher_skill.py     # Step 1: Find code evidence
│   ├── delta_generator_skill.py     # Step 2: Generate with baseline + evidence
│   └── validation_orchestrator_skill.py  # Step 3: Validate with retry

orchestrator/
└── documentation_workflow.py         # Chains all three skills

skill-manifests/
├── repo-researcher.yaml              # Configuration for researcher
├── delta-generator.yaml              # Configuration for generator
└── validation-orchestrator.yaml      # Configuration for validator
```

## Key Innovation: Repo-Aware Delta Generation

**Problem**: Original generator produces inconsistent results (57% consistency at temp 0.3)

**Root Cause**: Template-based generation without grounding in actual codebase

**Solution**: Three-step workflow that grounds generation in repo evidence:

1. **RepoResearcherSkill**: Search codebase for evidence
   - Semantic search for conceptual understanding
   - File search for relevant files
   - Text search for specific terms
   - Configuration extraction
   - Returns structured evidence with confidence scores

2. **DeltaGeneratorSkill**: Generate using baseline + evidence
   - Loads source v0.2 document as authoritative baseline
   - Analyzes each section for relevance to evidence
   - Only updates sections where evidence indicates changes
   - Preserves original content when no changes detected
   - Marks changes as UPDATED, UNCHANGED, or ERROR

3. **ValidationOrchestratorSkill**: Validate with retry
   - Runs existing validators (frontmatter, requirement IDs, traceability, structure)
   - Provides detailed feedback for corrections
   - Automatically retries with regeneration (max 3 attempts)
   - Tracks validation history

## Benefits Over Original Generator

| Feature | Original Generator | Skills-Based Approach |
|---------|-------------------|-----------------------|
| Grounding | Template only | Baseline + repo evidence |
| Consistency | 57% at temp 0.3 | **Expected: 80%+** (anchored to source) |
| Hallucination | High risk | Low risk (evidence-driven) |
| Traceability | Template-based | Evidence audit trail |
| Adaptability | Hardcoded | Pluggable skills |
| Debugging | Monolithic | Per-skill state tracking |

## Quick Start

### Prerequisites

```bash
# Ensure virtual environment is activated
cd docs/eva-foundation/projects/01-documentation-generator
.venv\Scripts\Activate.ps1

# Install dependencies (if not already installed)
pip install langchain-openai python-dotenv rich azure-identity pyyaml
```

### Test with One File

```powershell
# Navigate to POC directory
cd docs\eva-foundation\projects\02-poc-agent-skills

# Run workflow for security-architecture.md
python orchestrator\documentation_workflow.py `
    --file security-architecture.md `
    --topic "security architecture authentication authorization" `
    --scope backend `
    --search-terms OAuth PKCE "Entra ID" "Azure AD" azure_credential
```

### Output

The workflow will:
1. ✅ Research: Find ~10-30 code files related to security/auth
2. ✅ Generate: Create document in `generated-output-skills/security-architecture.md`
3. ✅ Validate: Check quality with up to 3 retry attempts
4. 📊 Display summary: Updated sections, validation results, duration
5. 💾 Save state: Workflow state in `logs/doc-gen-*.json`

## Configuration

### Baseline Directory

Edit [skill-manifests/delta-generator.yaml](skill-manifests/delta-generator.yaml):

```yaml
configuration:
  baseline_dir: "../../01-documentation-generator/source-docs-v0.2"
  output_dir: "../../01-documentation-generator/generated-output-skills"
  temperature: 0.3
```

### Search Paths

Edit [skill-manifests/repo-researcher.yaml](skill-manifests/repo-researcher.yaml):

```yaml
configuration:
  search_paths:
    - "app/backend"
    - "app/frontend"
    - "functions"
    - "infra"
  
  excluded_paths:
    - "__pycache__"
    - "node_modules"
    - ".venv"
```

### Validators

Edit [skill-manifests/validation-orchestrator.yaml](skill-manifests/validation-orchestrator.yaml):

```yaml
configuration:
  max_retries: 3
  strict_mode: true
  
  enabled_validators:
    - frontmatter
    - requirement_ids
    - traceability
    - structure
```

## Testing Plan

### Phase 1: Single File Test

```powershell
# Test security-architecture.md (has known validation issues)
python orchestrator\documentation_workflow.py `
    --file security-architecture.md `
    --topic "security architecture" `
    --scope backend
```

**Success Criteria**:
- ✅ Workflow completes without errors
- ✅ All validation passes (or passes after retry)
- ✅ Output file exists in `generated-output-skills/`
- ✅ State file saved in `logs/`

### Phase 2: Consistency Test

Run the same file 3 times and compare:

```powershell
# Run A
python orchestrator\documentation_workflow.py --file security-architecture.md --topic "security" --scope backend

# Run B
python orchestrator\documentation_workflow.py --file security-architecture.md --topic "security" --scope backend

# Run C
python orchestrator\documentation_workflow.py --file security-architecture.md --topic "security" --scope backend

# Compare
python ../01-documentation-generator/src/compare_outputs.py `
    --original generated-output-skills/run-a `
    --new generated-output-skills/run-b `
    --output comparison-runs-ab.md
```

**Success Criteria**:
- ✅ Consistency > 80% (vs 57% baseline)
- ✅ Identical files > 0 (vs 0 baseline)
- ✅ Similar files (>80% match) > 50%

### Phase 3: Full Suite Test

Run all 28 files:

```powershell
# TODO: Create batch script to run all files
# Compare against Run J baseline
```

**Success Criteria**:
- ✅ All 28 files generate successfully
- ✅ Validation pass rate > 90%
- ✅ Average consistency > 80%

## Comparison to Run J Baseline

| Metric | Run J (Original) | Skills-Based | Target |
|--------|------------------|--------------|--------|
| Files completed | 28/28 | TBD | 28/28 |
| Validation pass rate | 100% | TBD | 100% |
| Consistency (inter-run) | 57.16% | TBD | **>80%** |
| Identical files | 0/28 | TBD | **>5/28** |
| Similar files (>80%) | 1/28 | TBD | **>15/28** |
| Duration | 11m 20s | TBD | <15m |

## Debugging

### View Workflow State

```powershell
# Find latest workflow state
Get-Content logs\doc-gen-*.json | ConvertFrom-Json | Format-List
```

### View Skill Logs

```powershell
# View researcher log
Get-Content logs\reporesearcherskill.log -Tail 50

# View generator log
Get-Content logs\deltageneratorskill.log -Tail 50

# View validator log
Get-Content logs\validationorchestratorskill.log -Tail 50
```

### Common Issues

**Issue**: `FileNotFoundError: Baseline document not found`
- **Fix**: Update `baseline_dir` in `delta-generator.yaml` to point to correct source docs

**Issue**: `Validators not available - validation will be limited`
- **Fix**: Ensure `01-documentation-generator/src/validators.py` exists and is accessible

**Issue**: `Azure OpenAI initialization failed`
- **Fix**: Check environment variables (`AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_API_KEY`) in `backend.env`

## Next Steps

1. ✅ **Test Single File**: Validate workflow works end-to-end
2. ✅ **Measure Consistency**: Run 3x and compare
3. ✅ **Compare to Run J**: Evaluate improvement
4. 🔄 **Iterate**: Adjust prompts, evidence weighting, validation rules
5. 🚀 **Scale**: Run full 28-file suite
6. 📊 **Analyze**: Compare consistency, accuracy, duration
7. 🎯 **Optimize**: Tune for production (caching, parallelization, cost reduction)

## Integration with GitHub Copilot Skills

This implementation can be packaged as GitHub Copilot skills:

```
.copilot/skills/eva-doc-generator/
├── SKILL.md                          # Master skill manifest
├── personas/
│   ├── researcher/SKILL.md           # @eva-researcher skill
│   ├── generator/SKILL.md            # @eva-generator skill
│   └── validator/SKILL.md            # @eva-validator skill
└── workflows/
    └── doc-generation.yaml           # Workflow definition
```

Then use as: `@eva-doc-generator generate security-architecture.md`

## Contributing

See [AGENT-SKILLS-IMPLEMENTATION-PLAN.md](AGENT-SKILLS-IMPLEMENTATION-PLAN.md) for full architecture.

## License

Same as parent project (EVA Foundation)
