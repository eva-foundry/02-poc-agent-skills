# EVA Agile Crew Agent Skills Implementation Plan

**Version**: 1.0.0
**Created**: January 15, 2026
**Status**: 🟡 Ready for Implementation
**Target**: Self-contained bootstrap for fresh Copilot session on new device
**Prerequisites**: None (zero prior EVA knowledge required)

---

## 🎯 MISSION

Implement EVA Agile Crew (P00-P21) as executable GitHub Copilot skills with orchestration layer, enabling AI-assisted development workflows with government-grade governance, traceability, and self-improvement capabilities.

---

## 📋 CONTEXT FOR NEW COPILOT SESSION

### What is EVA Agile Crew?

EVA Agile Crew is a **22-pattern agent system (P00-P21)** that provides specialized development assistance across the software lifecycle:

- **Core Agents (P01-P15)**: Requirements, Scrum, Documentation, Scaffolding, Review, Testing, CI/CD, Security, UX, Onboarding, Metrics, Operations, Orchestration
- **Meta Patterns (P16-P21)**: Awareness Protocol, Swarm Review, Auto-Onboarding, Action Classification, Self-Improvement, Provenance

### Where to Find Information

**Critical Files to Read First:**

1. **Copilot Instructions**: `eva-orchestrator/.github/copilot-instructions.md`
   - EVA Suite context, Canada-First strategy, quality standards

2. **Persona Specifications**: `eva-orchestrator/to upload/EVA Agentic/`
   - `EVA P00 - DevTools Agents spec.md` (master catalog)
   - `EVA P01 - DevTools - Agent Patterns n Toolbox Roadmap.md` (index)
   - `EVA P02 - Requirements Agent.md` through `EVA P15 - Dev Master Orchestrator Agent.md`
   - `EVA Agile Crew Charter.md` (governance principles)

3. **Reference Implementation**: `.copilot/skills/agent-workflow-builder_ai_toolkit/SKILL.md`
   - Example of GitHub Copilot skill format

4. **Existing Tools**: `eva-orchestrator/scripts/p02-*.ps1`
   - 8+ PowerShell scripts showing tool implementation patterns

5. **Memory & Lessons**: `eva-orchestrator/.eva-memory.json`
   - LESSON-013: Context Engineering (4-block prompt pattern)
   - TOOL-004: P16-DMP (Directory Mapping Pattern - 1600x speedup)
   - PATTERN-003: Housekeeping automation

### Key Principles

- ✅ **Human Accountability**: Agents support, humans decide
- ✅ **No Autonomous Merges**: All code changes via PR review
- ✅ **Full Traceability**: P21 provenance on every action
- ✅ **Safety First**: P19 classification (C0-C3 risk levels)
- ✅ **Self-Awareness**: P16 awareness blocks (confidence, reflection, risks)
- ✅ **Continuous Learning**: P20 retrospectives improve the crew

---

## 📐 ARCHITECTURE OVERVIEW

```
.copilot/skills/eva-agile-crew/
├── SKILL.md                    # Master skill with all persona references
├── VERSION                     # Semantic versioning
├── registry.json               # Persona → Skill → Tools mapping
├── README.md                   # Quick start guide
├── IMPLEMENTATION-GUIDE.md     # Detailed architecture
├── VALIDATION-CHECKLIST.md     # 20+ test scenarios
│
├── personas/                   # Individual persona skills
│   ├── P00-PAT/SKILL.md       # Pattern Librarian
│   ├── P02-REQ/SKILL.md       # Requirements Agent
│   ├── P03-SCR/SKILL.md       # Scrum Master
│   ├── P05-SCA/SKILL.md       # Scaffolder
│   ├── P06-REV/SKILL.md       # Review Agent
│   ├── P07-TST/SKILL.md       # Testing Agent
│   ├── P15-DVM/SKILL.md       # Dev Master Orchestrator
│   └── ... (15 more)
│
├── handlers/                   # Tool execution logic
│   ├── index.ts               # Main dispatcher
│   ├── p02-requirements/      # P02 tool handlers
│   │   ├── classify-cdds.ts
│   │   ├── refine-requirements.ts
│   │   └── gap-detection.ts
│   ├── p05-scaffolder/        # P05 tool handlers
│   ├── p15-orchestrator/      # P15 workflow engine
│   └── shared/                # Common utilities
│       ├── awareness.ts       # P16 awareness blocks
│       ├── provenance.ts      # P21 fingerprinting
│       └── classification.ts  # P19 risk classification
│
├── orchestration/              # P15 Dev Master workflow engine
│   ├── DevMasterOrchestrator.ts
│   ├── workflows/
│   │   ├── feature.json       # Feature development flow
│   │   ├── bugfix.json        # Bug fix flow
│   │   ├── review.json        # PR review flow
│   │   └── infra.json         # Infrastructure change flow
│   └── state/
│       └── WorkflowState.ts   # State persistence
│
└── schemas/                    # JSON schemas for tool definitions
    ├── p02-classify-cdds.schema.json
    ├── p02-refine-requirements.schema.json
    └── ... (50+ tool schemas)
```

---

## 🚀 IMPLEMENTATION PHASES

### ⚡ PHASE 0: Bootstrap & Context Loading (Est: 2 hours)

**Goal**: Acquire all necessary context on fresh device with zero prior knowledge.

**Steps:**

1. **Clone Repository**
   ```powershell
   git clone https://github.com/MarcoPolo483/eva-orchestrator.git
   cd eva-orchestrator
   ```

2. **Read Foundational Documents** (in order)
   - [ ] `.github/copilot-instructions.md` (15 min read)
   - [ ] `to upload/EVA Agentic/EVA Agile Crew Charter.md` (10 min)
   - [ ] `to upload/EVA Agentic/EVA P00 - DevTools Agents spec.md` (20 min)
   - [ ] `to upload/EVA Agentic/EVA P01 - DevTools - Agent Patterns n Toolbox Roadmap.md` (15 min)
   - [ ] `.eva-memory.json` (10 min - focus on LESSON-013, TOOL-004, PATTERN-003)

3. **Analyze Reference Implementation**
   - [ ] Read `.copilot/skills/agent-workflow-builder_ai_toolkit/SKILL.md`
   - [ ] Identify skill format: YAML frontmatter + markdown body
   - [ ] Note tool declaration patterns

4. **Survey Existing Tools**
   - [ ] List all `scripts/p02-*.ps1` files (8 scripts)
   - [ ] Read `scripts/p02-004-cdd-classification.ps1` (reference tool)
   - [ ] Extract input/output patterns

5. **Extract Persona Catalog**
   - [ ] Read all `to upload/EVA Agentic/EVA P0*.md` files (P00-P15)
   - [ ] Create working table:
     ```
     | Pattern | Code | Name | Purpose | Tools (inferred) | Pod Scope |
     |---------|------|------|---------|------------------|-----------|
     | P02 | REQ | Requirements | CDD refinement | classify-cdds, refine, gap-detect | All |
     | ... | ... | ... | ... | ... | ... |
     ```

**Deliverable**: Context summary document with persona table and key principles.

**Evidence of Completion**:
- File created: `eva-agile-crew/BOOTSTRAP-CONTEXT.md`
- Contains 22 personas with extracted tools
- Includes key lessons from .eva-memory.json

---

### 🏗️ PHASE 1: Foundation - Skill Registry (Est: 6 hours)

**Goal**: Create skill directory structure and master registry.

**Steps:**

1. **Create Directory Structure**
   ```powershell
   # Navigate to user's Copilot skills directory
   $skillsDir = "$env:USERPROFILE\.copilot\skills"
   New-Item -ItemType Directory -Path "$skillsDir\eva-agile-crew" -Force

   # Create subdirectories
   cd "$skillsDir\eva-agile-crew"
   @('personas', 'handlers', 'orchestration', 'schemas') | ForEach-Object {
       New-Item -ItemType Directory -Path $_ -Force
   }
   ```

2. **Create Master SKILL.md**

   **File**: `.copilot/skills/eva-agile-crew/SKILL.md`

   ```markdown
   ---
   name: eva-agile-crew
   description: EVA Agile Crew (P00-P21) - 22 specialized agent personas for AI-assisted development with government-grade governance, traceability, and self-improvement
   category: development-workflows
   version: 1.0.0
   ---

   # EVA Agile Crew - Agent Personas (P00-P21)

   The EVA Agile Crew is a 22-pattern agent system providing specialized assistance across the SDLC.

   ## Core Agents

   - **@eva-p02-requirements** - CDD refinement, backlog structuring
   - **@eva-p03-scrum** - Sprint planning, DoR/DoD validation
   - **@eva-p04-librarian** - Documentation hygiene, ADR tracking
   - **@eva-p05-scaffolder** - Repo/module bootstrapping
   - **@eva-p06-review** - PR first-pass review
   - **@eva-p07-testing** - Test generation, failure analysis
   - **@eva-p08-cicd** - Pipeline optimization
   - **@eva-p09-runbook** - Operations documentation
   - **@eva-p10-metrics** - Analytics and insights
   - **@eva-p11-security** - Security and compliance
   - **@eva-p12-ux** - UX, accessibility, i18n
   - **@eva-p13-onboarding** - Developer onboarding
   - **@eva-p14-liveops** - Production operations
   - **@eva-p15-orchestrator** - Workflow coordination

   ## Meta Patterns

   - **P16 - Awareness Protocol**: Self-awareness metadata (confidence, reflection, risks)
   - **P17 - Swarm Review**: Parallel micro-agent PR reviews
   - **P18 - Auto-Onboarding**: Tool/API integration automation
   - **P19 - Action Classification**: C0-C3 risk-based safety gates
   - **P20 - Self-Improvement**: Retrospective learning
   - **P21 - Provenance**: Complete audit trails

   ## Usage

   Invoke agents by persona:
   - "**@eva-p02-requirements** classify CDDs in this workspace"
   - "**@eva-p15-orchestrator** execute feature workflow for story #123"
   - "**@eva-p06-review** perform swarm review on PR #45"
   ```

3. **Create Registry Catalog**

   **File**: `.copilot/skills/eva-agile-crew/registry.json`

   ```json
   {
     "version": "1.0.0",
     "lastUpdated": "2026-01-15T00:00:00Z",
     "personas": [
       {
         "pattern": "P02",
         "code": "REQ",
         "name": "Requirements Agent",
         "skillPath": "personas/P02-REQ/SKILL.md",
         "podScope": ["POD-F", "POD-X", "POD-O", "POD-S"],
         "lifecyclePhases": [0, 1, 2, 4],
         "tools": [
           {
             "name": "p02-classify_cdds",
             "description": "Classify CDD files by heuristics",
             "schemaPath": "schemas/p02-classify-cdds.schema.json",
             "handlerPath": "handlers/p02-requirements/classify-cdds.ts"
           },
           {
             "name": "p02-refine_requirements",
             "description": "Recursively refine requirements",
             "schemaPath": "schemas/p02-refine-requirements.schema.json",
             "handlerPath": "handlers/p02-requirements/refine-requirements.ts"
           },
           {
             "name": "p02-gap_detection",
             "description": "Detect CDD coverage gaps",
             "schemaPath": "schemas/p02-gap-detection.schema.json",
             "handlerPath": "handlers/p02-requirements/gap-detection.ts"
           }
         ]
       },
       {
         "pattern": "P15",
         "code": "DVM",
         "name": "Dev Master Orchestrator",
         "skillPath": "personas/P15-DVM/SKILL.md",
         "podScope": ["POD-F"],
         "lifecyclePhases": [0, 1, 2, 3, 4, 5, 6],
         "tools": [
           {
             "name": "p15-execute_workflow",
             "description": "Orchestrate multi-agent workflow",
             "schemaPath": "schemas/p15-execute-workflow.schema.json",
             "handlerPath": "orchestration/DevMasterOrchestrator.ts"
           }
         ]
       }
     ]
   }
   ```

4. **Create VERSION File**

   **File**: `.copilot/skills/eva-agile-crew/VERSION`

   ```
   1.0.0
   ```

**Deliverable**: Functional skill directory with master SKILL.md and registry.

**Evidence of Completion**:
- Directory exists: `$env:USERPROFILE\.copilot\skills\eva-agile-crew`
- Files created: `SKILL.md`, `registry.json`, `VERSION`
- VS Code Copilot recognizes `@eva-agile-crew` skill (test by typing in chat)

---

### 🧩 PHASE 2: Convert Personas to Skills (Est: 12 hours)

**Goal**: Create individual SKILL.md files for priority personas (P02, P05, P15, P06, P07).

**Priority Order**: P02 → P15 → P05 → P06 → P07

#### 2.1 P02 - Requirements Agent

**Steps:**

1. **Read Source**: `eva-orchestrator/to upload/EVA Agentic/EVA P02 - Requirements Agent.md`

2. **Extract Tool Definitions** from responsibilities:
   - CDD classification → `p02-classify_cdds`
   - Requirements refinement → `p02-refine_requirements`
   - Gap detection → `p02-gap_detection`
   - Dependency graphing → `p02-dependency_graph`
   - Backlog structuring → `p02-structure_backlog`

3. **Create Persona Skill**

   **File**: `.copilot/skills/eva-agile-crew/personas/P02-REQ/SKILL.md`

   ```markdown
   ---
   name: eva-p02-requirements-agent
   description: Recursively refine ideas into CDDs, epics, stories. CDD classification, gap detection, backlog structuring.
   category: agile-crew
   persona: P02-REQ
   code: REQ
   pod_scope: [POD-F, POD-X, POD-O, POD-S]
   lifecycle_phases: [0, 1, 2, 4]
   ---

   # P02 - Requirements Agent (REQ)

   ## Core Responsibilities

   1. **CDD Management**: Classify, track, and maintain Component Design Documents
   2. **Requirements Refinement**: Recursive refinement from idea → canvas → epic → story → CDD
   3. **Gap Detection**: Identify missing or incomplete requirements
   4. **Dependency Mapping**: Generate dependency graphs between components
   5. **Backlog Structuring**: Organize and prioritize work items

   ## Tools

   ### p02-classify_cdds

   Classifies EVA Suite CDD files based on naming heuristics and content patterns.

   **Inputs:**
   - `treeFile` (string, required): Path to workspace tree snapshot
   - `evaSuiteRoot` (string, required): Root path to EVA Suite workspace
   - `outputFormat` (string, optional): "markdown" | "json" | "both" (default: "both")

   **Outputs:**
   - `classificationSummary` (string): Markdown summary table
   - `classificationData` (object): JSON structure with classifications
   - `awareness` (object): P16 awareness block (confidence, reflection, risks)

   **Example:**
   ```
   @eva-p02-requirements classify CDDs in workspace at C:\eva-suite
   ```

   ### p02-refine_requirements

   Recursively refines requirements using AI assistance with context engineering.

   **Inputs:**
   - `requirementDoc` (string, required): Path to requirement document
   - `refinementLevel` (number, optional): Depth 1-5 (default: 3)
   - `targetFormat` (string, optional): "cdd" | "epic" | "story" (default: "cdd")

   **Outputs:**
   - `refinedDocument` (string): Path to refined output
   - `gapAnalysis` (object): Identified gaps and missing details
   - `suggestedTasks` (array): Recommended follow-up tasks
   - `awareness` (object): P16 awareness block

   ### p02-gap_detection

   Detects coverage gaps in CDD documentation across the workspace.

   **Inputs:**
   - `scopePath` (string, required): Path to scan (workspace or repo)
   - `criteriaSet` (string, optional): "minimal" | "standard" | "comprehensive" (default: "standard")

   **Outputs:**
   - `gapReport` (string): Markdown report of gaps
   - `missingCDDs` (array): Components without CDDs
   - `incompleteCDDs` (array): CDDs missing required sections
   - `awareness` (object): P16 awareness block

   ### p02-dependency_graph

   Generates dependency graph between components based on CDDs.

   **Inputs:**
   - `cddDirectory` (string, required): Directory containing CDDs
   - `outputFormat` (string, optional): "mermaid" | "dot" | "json" (default: "mermaid")

   **Outputs:**
   - `dependencyGraph` (string): Visual graph in requested format
   - `criticalPath` (array): Critical dependency chain
   - `cyclicDependencies` (array): Detected cycles
   - `awareness` (object): P16 awareness block

   ## Governance

   - **Autonomy Level**: Advisory/Assistive
   - **Action Classification**: C0-C1 (read, create docs, no merges)
   - **Human Approval**: Required for C2+ actions
   - **Provenance**: P21 logging on all actions

   ## Pod Assignments

   - **POD-F**: Foundation requirements
   - **POD-X**: UX/UI component requirements
   - **POD-O**: Operations requirements
   - **POD-S**: Solution-specific requirements
   ```

4. **Create JSON Schemas**

   **File**: `.copilot/skills/eva-agile-crew/schemas/p02-classify-cdds.schema.json`

   ```json
   {
     "$schema": "http://json-schema.org/draft-07/schema#",
     "$id": "https://eva-suite.gc.ca/schemas/p02-classify-cdds.json",
     "title": "P02 Classify CDDs Tool Schema",
     "type": "object",
     "required": ["treeFile", "evaSuiteRoot"],
     "properties": {
       "treeFile": {
         "type": "string",
         "description": "Path to workspace tree snapshot file",
         "pattern": "^.*\\.txt$"
       },
       "evaSuiteRoot": {
         "type": "string",
         "description": "Root path to EVA Suite workspace"
       },
       "outputFormat": {
         "type": "string",
         "enum": ["markdown", "json", "both"],
         "default": "both"
       }
     },
     "additionalProperties": false
   }
   ```

**Repeat for P15, P05, P06, P07** with similar structure.

**Deliverable**: 5 persona skills with 15+ tools defined.

**Evidence of Completion**:
- 5 SKILL.md files created in personas/ subdirectories
- 15+ JSON schemas in schemas/ directory
- Test invocation: `@eva-p02-requirements` autocompletes in Copilot chat

---

### ⚙️ PHASE 3: Implement Tool Handlers (Est: 16 hours)

**Goal**: Create executable tool handlers with P16 awareness and P21 provenance.

**Technology Stack**: TypeScript + Node.js (cross-platform)

#### 3.1 Setup Handler Infrastructure

**Steps:**

1. **Initialize Node.js Project**
   ```powershell
   cd $env:USERPROFILE\.copilot\skills\eva-agile-crew\handlers
   npm init -y
   npm install --save typescript @types/node
   npm install --save-dev ts-node
   ```

2. **Create tsconfig.json**

   **File**: `handlers/tsconfig.json`

   ```json
   {
     "compilerOptions": {
       "target": "ES2022",
       "module": "commonjs",
       "lib": ["ES2022"],
       "outDir": "./dist",
       "rootDir": "./",
       "strict": true,
       "esModuleInterop": true,
       "skipLibCheck": true,
       "forceConsistentCasingInFileNames": true,
       "resolveJsonModule": true
     },
     "include": ["**/*.ts"],
     "exclude": ["node_modules", "dist"]
   }
   ```

3. **Create Handler Dispatcher**

   **File**: `handlers/index.ts`

   ```typescript
   import * as fs from 'fs';
   import * as path from 'path';
   import { AwarenessBlock, ProvenanceBlock, ToolResult } from './shared/types';
   import { createAwarenessBlock } from './shared/awareness';
   import { createProvenanceBlock } from './shared/provenance';

   interface ToolHandler {
     (args: any): Promise<ToolResult>;
   }

   const handlers = new Map<string, ToolHandler>();

   // Register P02 handlers
   import { classifyCDDs } from './p02-requirements/classify-cdds';
   import { refineRequirements } from './p02-requirements/refine-requirements';
   import { detectGaps } from './p02-requirements/gap-detection';

   handlers.set('p02-classify_cdds', classifyCDDs);
   handlers.set('p02-refine_requirements', refineRequirements);
   handlers.set('p02-gap_detection', detectGaps);

   export async function invokeTool(
     toolName: string,
     args: any
   ): Promise<ToolResult> {
     const handler = handlers.get(toolName);

     if (!handler) {
       throw new Error(`Tool handler not found: ${toolName}`);
     }

     const startTime = Date.now();

     try {
       const result = await handler(args);

       // Ensure P16 awareness and P21 provenance
       if (!result.awareness) {
         result.awareness = createAwarenessBlock(0.5, 'No awareness provided by handler');
       }

       if (!result.provenance) {
         result.provenance = createProvenanceBlock(toolName, args);
       }

       result.provenance.executionTime = Date.now() - startTime;

       return result;
     } catch (error) {
       return {
         success: false,
         error: error.message,
         awareness: createAwarenessBlock(0.0, `Tool execution failed: ${error.message}`),
         provenance: createProvenanceBlock(toolName, args)
       };
     }
   }
   ```

4. **Create Shared Types**

   **File**: `handlers/shared/types.ts`

   ```typescript
   export interface AwarenessBlock {
     confidence: number; // 0-1
     reflection: string;
     risks: string[];
     suggestedActions: string[];
   }

   export interface ProvenanceBlock {
     agentFingerprint: {
       agentId: string;
       version: string;
       pod: string;
       repo: string;
       environment: string;
     };
     taskContext: {
       workItemId?: string;
       sprintId?: string;
       projectId?: string;
     };
     provenance: {
       promptRef?: string;
       contextSources: string[];
       modelDetails?: {
         provider: string;
         model: string;
         temperature?: number;
       };
     };
     changeSummary: {
       actionClass: 'C0' | 'C1' | 'C2' | 'C3';
       operation: string;
       filesTouched: string[];
     };
     executionTime?: number;
     timestamp: string;
   }

   export interface ToolResult {
     success: boolean;
     data?: any;
     error?: string;
     awareness: AwarenessBlock;
     provenance: ProvenanceBlock;
   }
   ```

5. **Create Awareness Helper**

   **File**: `handlers/shared/awareness.ts`

   ```typescript
   import { AwarenessBlock } from './types';

   export function createAwarenessBlock(
     confidence: number,
     reflection: string,
     risks: string[] = [],
     suggestedActions: string[] = []
   ): AwarenessBlock {
     // Validate confidence
     if (confidence < 0 || confidence > 1) {
       throw new Error('Confidence must be between 0 and 1');
     }

     return {
       confidence,
       reflection,
       risks,
       suggestedActions
     };
   }

   export function shouldEscalateToHuman(awareness: AwarenessBlock): boolean {
     return awareness.confidence < 0.7 || awareness.risks.length > 0;
   }
   ```

6. **Create Provenance Helper**

   **File**: `handlers/shared/provenance.ts`

   ```typescript
   import { ProvenanceBlock } from './types';
   import * as os from 'os';

   export function createProvenanceBlock(
     toolName: string,
     args: any
   ): ProvenanceBlock {
     return {
       agentFingerprint: {
         agentId: toolName,
         version: '1.0.0',
         pod: 'eva-agile-crew',
         repo: 'eva-agile-crew-skills',
         environment: process.env.NODE_ENV || 'development'
       },
       taskContext: {
         workItemId: args.workItemId,
         sprintId: args.sprintId,
         projectId: args.projectId
       },
       provenance: {
         contextSources: [],
         modelDetails: {
           provider: 'github-copilot',
           model: 'gpt-4'
         }
       },
       changeSummary: {
         actionClass: 'C0',
         operation: toolName,
         filesTouched: []
       },
       timestamp: new Date().toISOString()
     };
   }
   ```

#### 3.2 Implement P02 Tool: classify-cdds

**File**: `handlers/p02-requirements/classify-cdds.ts`

```typescript
import * as fs from 'fs';
import * as path from 'path';
import { ToolResult } from '../shared/types';
import { createAwarenessBlock } from '../shared/awareness';
import { createProvenanceBlock } from '../shared/provenance';

interface ClassifyCDDsArgs {
  treeFile: string;
  evaSuiteRoot: string;
  outputFormat?: 'markdown' | 'json' | 'both';
}

export async function classifyCDDs(
  args: ClassifyCDDsArgs
): Promise<ToolResult> {
  // Validate inputs
  if (!fs.existsSync(args.treeFile)) {
    return {
      success: false,
      error: `Tree file not found: ${args.treeFile}`,
      awareness: createAwarenessBlock(
        0.0,
        'Input validation failed',
        ['File not found'],
        ['Verify tree file path', 'Run tree generation script']
      ),
      provenance: createProvenanceBlock('p02-classify_cdds', args)
    };
  }

  // Read tree file
  const treeContent = fs.readFileSync(args.treeFile, 'utf-8');
  const lines = treeContent.split('\n');

  // Classification heuristics (from p02-004-cdd-classification.ps1)
  const classifications = {
    'Component Design Document': [] as string[],
    'Architecture Decision Record': [] as string[],
    'User Story': [] as string[],
    'Technical Specification': [] as string[],
    'Unclassified': [] as string[]
  };

  let confidence = 0.8;
  const risks: string[] = [];

  // Parse tree and classify
  for (const line of lines) {
    // Match CDD pattern: *-CDD-*.md, ADR-*.md, US-*.md, etc.
    if (line.match(/CDD-\d+/i)) {
      classifications['Component Design Document'].push(line.trim());
    } else if (line.match(/ADR-\d+/i)) {
      classifications['Architecture Decision Record'].push(line.trim());
    } else if (line.match(/US-\d+/i)) {
      classifications['User Story'].push(line.trim());
    } else if (line.match(/SPEC-\d+/i)) {
      classifications['Technical Specification'].push(line.trim());
    } else if (line.match(/\.md$/i) && line.match(/docs\//)) {
      classifications['Unclassified'].push(line.trim());
    }
  }

  // Calculate confidence based on classification success
  const totalClassified = Object.values(classifications)
    .reduce((sum, arr) => sum + arr.length, 0);

  if (totalClassified === 0) {
    confidence = 0.3;
    risks.push('No documents classified - tree file may be invalid');
  } else if (classifications['Unclassified'].length > totalClassified * 0.3) {
    confidence = 0.6;
    risks.push('High percentage of unclassified documents');
  }

  // Generate output
  const markdownSummary = generateMarkdownSummary(classifications);
  const jsonData = {
    classifications,
    summary: {
      total: totalClassified,
      byType: Object.entries(classifications).map(([type, docs]) => ({
        type,
        count: docs.length
      }))
    }
  };

  // Create provenance with file touches
  const provenance = createProvenanceBlock('p02-classify_cdds', args);
  provenance.provenance.contextSources.push(args.treeFile);
  provenance.changeSummary.filesTouched.push(args.treeFile);

  return {
    success: true,
    data: {
      markdownSummary,
      jsonData
    },
    awareness: createAwarenessBlock(
      confidence,
      `Classified ${totalClassified} documents across ${Object.keys(classifications).length} categories`,
      risks,
      risks.length > 0 ? ['Review unclassified documents', 'Refine classification heuristics'] : []
    ),
    provenance
  };
}

function generateMarkdownSummary(classifications: Record<string, string[]>): string {
  let md = '# CDD Classification Summary\n\n';
  md += '| Type | Count | Files |\n';
  md += '|------|-------|-------|\n';

  for (const [type, docs] of Object.entries(classifications)) {
    md += `| ${type} | ${docs.length} | ${docs.slice(0, 3).join(', ')}${docs.length > 3 ? '...' : ''} |\n`;
  }

  return md;
}
```

**Deliverable**: 3 P02 tools implemented + shared infrastructure.

**Evidence of Completion**:
- Files created: `handlers/index.ts`, `shared/*.ts`, `p02-requirements/*.ts`
- TypeScript compiles: `npm run build` succeeds
- Test invocation: `node dist/index.js p02-classify_cdds '{"treeFile":"test.txt","evaSuiteRoot":"."}'`
- Output includes awareness block with confidence score
- Output includes provenance block with agent fingerprint

---

### 🔀 PHASE 4: Orchestration Layer (Est: 10 hours)

**Goal**: Implement P15 Dev Master Orchestrator with workflow execution.

#### 4.1 Create DevMasterOrchestrator

**File**: `orchestration/DevMasterOrchestrator.ts`

```typescript
import * as fs from 'fs';
import * as path from 'path';
import { invokeTool } from '../handlers';
import { ToolResult, AwarenessBlock } from '../handlers/shared/types';
import { shouldEscalateToHuman } from '../handlers/shared/awareness';

interface WorkflowStep {
  persona: string;
  tool: string;
  inputs: any;
  requiresApproval?: boolean;
}

interface Workflow {
  name: string;
  description: string;
  steps: WorkflowStep[];
}

interface WorkflowState {
  workflowName: string;
  currentStep: number;
  stepResults: ToolResult[];
  status: 'running' | 'paused' | 'completed' | 'failed';
  pauseReason?: string;
}

export class DevMasterOrchestrator {
  private workflows = new Map<string, Workflow>();
  private state: WorkflowState | null = null;

  constructor(private workflowsDir: string) {
    this.loadWorkflows();
  }

  private loadWorkflows() {
    const workflowFiles = fs.readdirSync(this.workflowsDir)
      .filter(f => f.endsWith('.json'));

    for (const file of workflowFiles) {
      const filePath = path.join(this.workflowsDir, file);
      const workflow = JSON.parse(fs.readFileSync(filePath, 'utf-8')) as Workflow;
      this.workflows.set(workflow.name, workflow);
    }

    console.log(`Loaded ${this.workflows.size} workflows`);
  }

  async executeWorkflow(
    workflowName: string,
    context: any
  ): Promise<WorkflowState> {
    const workflow = this.workflows.get(workflowName);

    if (!workflow) {
      throw new Error(`Workflow not found: ${workflowName}`);
    }

    this.state = {
      workflowName,
      currentStep: 0,
      stepResults: [],
      status: 'running'
    };

    console.log(`Starting workflow: ${workflow.name}`);
    console.log(`Description: ${workflow.description}`);

    for (let i = 0; i < workflow.steps.length; i++) {
      const step = workflow.steps[i];
      this.state.currentStep = i;

      console.log(`\nStep ${i + 1}/${workflow.steps.length}: ${step.persona} - ${step.tool}`);

      // Merge context into step inputs
      const inputs = { ...step.inputs, ...context };

      // Invoke tool
      const result = await invokeTool(step.tool, inputs);
      this.state.stepResults.push(result);

      // Check if failed
      if (!result.success) {
        this.state.status = 'failed';
        console.error(`Step failed: ${result.error}`);
        break;
      }

      // Check awareness - escalate if low confidence
      if (shouldEscalateToHuman(result.awareness)) {
        this.state.status = 'paused';
        this.state.pauseReason = 'Low confidence or risks detected';
        console.warn(`\n⚠️  Workflow paused at step ${i + 1}`);
        console.warn(`Reason: ${this.state.pauseReason}`);
        console.warn(`Confidence: ${result.awareness.confidence}`);
        console.warn(`Reflection: ${result.awareness.reflection}`);
        console.warn(`Risks: ${result.awareness.risks.join(', ')}`);
        console.warn(`\nHuman approval required to continue.`);
        break;
      }

      // Check if requires explicit approval
      if (step.requiresApproval) {
        this.state.status = 'paused';
        this.state.pauseReason = 'Explicit approval required';
        console.warn(`\n⚠️  Workflow paused at step ${i + 1}`);
        console.warn(`Reason: ${this.state.pauseReason}`);
        console.warn(`\nHuman approval required to continue.`);
        break;
      }

      console.log(`✓ Step completed (confidence: ${result.awareness.confidence})`);
    }

    if (this.state.status === 'running') {
      this.state.status = 'completed';
      console.log(`\n✓ Workflow completed successfully`);
    }

    return this.state;
  }

  getState(): WorkflowState | null {
    return this.state;
  }

  async resume(approvalGranted: boolean) {
    if (!this.state || this.state.status !== 'paused') {
      throw new Error('No paused workflow to resume');
    }

    if (!approvalGranted) {
      this.state.status = 'failed';
      console.log('Workflow cancelled by user');
      return this.state;
    }

    // Resume from next step
    this.state.status = 'running';
    const workflow = this.workflows.get(this.state.workflowName)!;

    for (let i = this.state.currentStep + 1; i < workflow.steps.length; i++) {
      // ... (same execution logic as above)
    }

    this.state.status = 'completed';
    return this.state;
  }
}
```

#### 4.2 Create Workflow Definitions

**File**: `orchestration/workflows/feature.json`

```json
{
  "name": "feature",
  "description": "Feature development workflow: Requirements → Scaffolding → Implementation → Testing → Review",
  "steps": [
    {
      "persona": "P02-REQ",
      "tool": "p02-refine_requirements",
      "inputs": {
        "requirementDoc": "{{featureSpec}}",
        "refinementLevel": 3,
        "targetFormat": "cdd"
      }
    },
    {
      "persona": "P05-SCA",
      "tool": "p05-scaffold_component",
      "inputs": {
        "componentName": "{{componentName}}",
        "templateType": "feature"
      }
    },
    {
      "persona": "P07-TST",
      "tool": "p07-generate_tests",
      "inputs": {
        "componentPath": "{{componentPath}}",
        "coverageTarget": 80
      }
    },
    {
      "persona": "P06-REV",
      "tool": "p06-swarm_review",
      "inputs": {
        "pullRequestNumber": "{{prNumber}}"
      },
      "requiresApproval": false
    }
  ]
}
```

**Deliverable**: Orchestrator + 3 workflow definitions.

**Evidence of Completion**:
- Files created: `DevMasterOrchestrator.ts`, `workflows/*.json`
- Test execution: `node dist/orchestration/test.js` runs feature workflow
- Workflow pauses at low confidence steps
- State persists between steps

---

### ✅ PHASE 5: Validation & Documentation (Est: 8 hours)

**Goal**: Comprehensive testing and documentation.

#### 5.1 Create Validation Checklist

**File**: `.copilot/skills/eva-agile-crew/VALIDATION-CHECKLIST.md`

```markdown
# EVA Agile Crew Validation Checklist

## Skill Loading

- [ ] VS Code Copilot recognizes `@eva-agile-crew` skill
- [ ] All persona skills autocomplete (`@eva-p02-requirements`, etc.)
- [ ] Skill descriptions appear in Copilot suggestions

## P02 Requirements Agent

- [ ] `p02-classify_cdds` executes with valid tree file
- [ ] Classification output includes markdown summary
- [ ] Classification output includes JSON data
- [ ] Awareness block present with confidence score
- [ ] Provenance block present with agent fingerprint
- [ ] Low confidence triggers human escalation flag

## P15 Dev Master Orchestrator

- [ ] Feature workflow loads from JSON
- [ ] Workflow executes step-by-step
- [ ] Workflow pauses at low confidence (<0.7)
- [ ] Workflow pauses at explicit approval gates
- [ ] State persists between steps
- [ ] Resume functionality works after pause

## P16 Awareness Protocol

- [ ] All tool outputs include awareness block
- [ ] Confidence scores range 0-1
- [ ] Reflection strings are meaningful
- [ ] Risks array populated when applicable
- [ ] Suggested actions provided for low confidence

## P19 Action Classification

- [ ] C0 actions (read-only) execute without approval
- [ ] C1 actions (dev-branch) require PR review
- [ ] C2 actions (governance) require explicit approval
- [ ] C3 actions (production) blocked by default

## P21 Provenance

- [ ] All tool outputs include provenance block
- [ ] Agent fingerprint contains version, pod, repo
- [ ] Task context links to work items
- [ ] Context sources list input files
- [ ] Files touched tracked accurately
- [ ] Timestamps in ISO 8601 format

## Error Handling

- [ ] Invalid inputs return descriptive errors
- [ ] Missing files handled gracefully
- [ ] Malformed JSON schemas rejected
- [ ] Null/undefined inputs validated
```

#### 5.2 Create Implementation Guide

**File**: `.copilot/skills/eva-agile-crew/IMPLEMENTATION-GUIDE.md`

```markdown
# EVA Agile Crew Implementation Guide

## Architecture

### Skill Structure
- **Master Skill**: `SKILL.md` - Entry point for all personas
- **Persona Skills**: `personas/P0X-XXX/SKILL.md` - Individual agent definitions
- **Tool Handlers**: `handlers/` - Executable TypeScript implementations
- **Orchestration**: `orchestration/` - P15 workflow engine
- **Schemas**: `schemas/` - JSON schema definitions for tools

### Execution Flow

1. User invokes agent in Copilot: `@eva-p02-requirements classify CDDs`
2. Copilot routes to skill: `eva-p02-requirements-agent`
3. Skill identifies tool: `p02-classify_cdds`
4. Handler dispatcher invokes: `handlers/p02-requirements/classify-cdds.ts`
5. Tool executes with P16 awareness and P21 provenance
6. Result returned to Copilot with structured output

### P16 Awareness Protocol

Every tool output includes:

```typescript
{
  confidence: 0.8,          // 0-1 scale
  reflection: "...",         // What the agent observed
  risks: ["..."],            // Potential issues
  suggestedActions: ["..."]  // Next steps
}
```

If `confidence < 0.7` OR `risks.length > 0` → escalate to human.

### P19 Action Classification

| Class | Description | Approval Required |
|-------|-------------|-------------------|
| C0 | Read/Analyze only | No |
| C1 | Dev-branch code/config | PR review |
| C2 | Governance/policy | Explicit approval |
| C3 | Production/infra | Blocked + sign-off |

### P21 Provenance

Every action logs:

```typescript
{
  agentFingerprint: { agentId, version, pod, repo, environment },
  taskContext: { workItemId, sprintId, projectId },
  provenance: { contextSources, modelDetails },
  changeSummary: { actionClass, operation, filesTouched },
  timestamp: "2026-01-15T12:00:00Z"
}
```

## Setup Instructions

### Prerequisites

- Node.js ≥20.10.0
- TypeScript ≥5.6.0
- VS Code with GitHub Copilot extension

### Installation

1. Clone repository:
   ```bash
   git clone https://github.com/MarcoPolo483/eva-orchestrator.git
   ```

2. Navigate to skills directory:
   ```bash
   cd ~/.copilot/skills/eva-agile-crew
   ```

3. Install dependencies:
   ```bash
   cd handlers
   npm install
   ```

4. Build TypeScript:
   ```bash
   npm run build
   ```

5. Verify skill loading:
   - Open VS Code
   - Open Copilot chat
   - Type `@eva` and verify autocomplete shows agent personas

### Testing

Run validation suite:
```bash
npm test
```

Manual test P02:
```bash
node dist/index.js p02-classify_cdds '{
  "treeFile": "path/to/tree.txt",
  "evaSuiteRoot": "/path/to/eva-suite"
}'
```

## Troubleshooting

### Skill Not Loading

- Check file location: `~/.copilot/skills/eva-agile-crew/SKILL.md`
- Verify YAML frontmatter is valid
- Restart VS Code

### Tool Execution Fails

- Check handler path in `registry.json`
- Verify TypeScript compiled: `npm run build`
- Check error logs in console

### Low Confidence Scores

- Review awareness reflection for context
- Check risks array for specific issues
- Verify input data quality
```

#### 5.3 Create README

**File**: `.copilot/skills/eva-agile-crew/README.md`

```markdown
# EVA Agile Crew - Agent Skills (P00-P21)

**Version**: 1.0.0
**Status**: ✅ Production Ready
**License**: MIT

## Overview

EVA Agile Crew is a 22-pattern agent system providing specialized AI assistance across the software development lifecycle, designed for government-grade projects with full traceability, governance, and self-improvement capabilities.

## Quick Start

### Installation

```bash
# Install skill
git clone https://github.com/MarcoPolo483/eva-agile-crew-skills.git ~/.copilot/skills/eva-agile-crew

# Install dependencies
cd ~/.copilot/skills/eva-agile-crew/handlers
npm install && npm run build
```

### Usage

Invoke agents in GitHub Copilot chat:

```
@eva-p02-requirements classify CDDs in this workspace
@eva-p15-orchestrator execute feature workflow for story #123
@eva-p06-review perform swarm review on PR #45
```

## Agent Personas

### Core Agents (P01-P15)

| Code | Name | Purpose |
|------|------|---------|
| P02 | Requirements (REQ) | CDD refinement, backlog structuring |
| P03 | Scrum Master (SCR) | Sprint planning, ceremonies |
| P05 | Scaffolder (SCA) | Repo/module bootstrapping |
| P06 | Review (REV) | PR first-pass review |
| P07 | Testing (TST) | Test generation, failure analysis |
| P15 | Dev Master (DVM) | Workflow orchestration |

[Full persona list in IMPLEMENTATION-GUIDE.md]

### Meta Patterns (P16-P21)

- **P16 - Awareness**: Self-awareness metadata (confidence, reflection, risks)
- **P17 - Swarm Review**: Parallel micro-agent PR reviews
- **P19 - Action Classification**: C0-C3 risk-based safety gates
- **P21 - Provenance**: Complete audit trails

## Governance

- ✅ **Human Accountability**: Agents support, humans decide
- ✅ **No Autonomous Merges**: All code changes via PR review
- ✅ **Full Traceability**: P21 provenance on every action
- ✅ **Safety First**: P19 classification (C0-C3 risk levels)

## Documentation

- [Implementation Guide](IMPLEMENTATION-GUIDE.md)
- [Validation Checklist](VALIDATION-CHECKLIST.md)
- [EVA Copilot Instructions](../../eva-orchestrator/.github/copilot-instructions.md)

## Support

- **Issues**: https://github.com/MarcoPolo483/eva-orchestrator/issues
- **Docs**: https://github.com/MarcoPolo483/eva-orchestrator/tree/main/docs

## License

MIT © 2026 Marco Presta + GitHub Copilot
```

**Deliverable**: Complete documentation suite.

**Evidence of Completion**:
- 3 documentation files created
- All validation checklist items pass
- README provides clear quick start
- Implementation guide covers architecture

---

## 🎯 EXECUTION CHECKLIST

Use this checklist to track implementation progress:

### Phase 0: Bootstrap (2 hours)
- [ ] Clone eva-orchestrator repository
- [ ] Read copilot-instructions.md
- [ ] Read EVA Agile Crew Charter
- [ ] Read P00, P01 specifications
- [ ] Extract persona catalog (22 personas)
- [ ] Read .eva-memory.json for key lessons
- [ ] Create BOOTSTRAP-CONTEXT.md summary

### Phase 1: Foundation (6 hours)
- [ ] Create skill directory structure
- [ ] Create master SKILL.md
- [ ] Create registry.json catalog
- [ ] Create VERSION file
- [ ] Verify skill loading in VS Code Copilot

### Phase 2: Convert Personas (12 hours)
- [ ] P02 Requirements Agent → SKILL.md + schemas
- [ ] P15 Dev Master Orchestrator → SKILL.md + schemas
- [ ] P05 Scaffolder → SKILL.md + schemas
- [ ] P06 Review Agent → SKILL.md + schemas
- [ ] P07 Testing Agent → SKILL.md + schemas
- [ ] Test autocomplete for all 5 personas

### Phase 3: Tool Handlers (16 hours)
- [ ] Setup Node.js + TypeScript infrastructure
- [ ] Create handler dispatcher (index.ts)
- [ ] Create shared types (types.ts)
- [ ] Create awareness helper (awareness.ts)
- [ ] Create provenance helper (provenance.ts)
- [ ] Implement p02-classify_cdds
- [ ] Implement p02-refine_requirements
- [ ] Implement p02-gap_detection
- [ ] Test all handlers with sample data

### Phase 4: Orchestration (10 hours)
- [ ] Create DevMasterOrchestrator.ts
- [ ] Create feature.json workflow
- [ ] Create bugfix.json workflow
- [ ] Create review.json workflow
- [ ] Implement state persistence
- [ ] Implement pause/resume logic
- [ ] Test feature workflow end-to-end

### Phase 5: Validation (8 hours)
- [ ] Create VALIDATION-CHECKLIST.md
- [ ] Create IMPLEMENTATION-GUIDE.md
- [ ] Create README.md
- [ ] Run all validation tests (20+ scenarios)
- [ ] Document troubleshooting steps
- [ ] Record demo video (optional)

---

## 📊 SUCCESS METRICS

**Completion Criteria:**

- ✅ All 22 personas documented as skills
- ✅ 5+ priority personas with working handlers
- ✅ P15 orchestrator executes workflows
- ✅ P16 awareness in all outputs (confidence, reflection, risks)
- ✅ P19 classification enforced (C0-C3)
- ✅ P21 provenance logged (agent fingerprint, task context)
- ✅ 20/20 validation tests pass
- ✅ Human escalation triggers at confidence <0.7
- ✅ Documentation complete (README + guides)

**Quality Gates:**

- ⚠️ Zero TypeScript compilation errors
- ⚠️ All JSON schemas validate
- ⚠️ Handler code coverage ≥80%
- ⚠️ Response time <2s for simple tools
- ⚠️ All actions traceable in logs

---

## 🚨 CRITICAL REMINDERS

### For Implementing Copilot

1. **Read FIRST**: `eva-orchestrator/.github/copilot-instructions.md`
   - Contains EVA Suite context and principles
   - LESSON-013: Context Engineering (prevent vibe coding)
   - P16-DMP: Directory Mapping Pattern (1600x speedup)

2. **Always Include**:
   - P16 awareness block in every tool output
   - P21 provenance block in every tool output
   - Input validation before execution
   - Error handling with descriptive messages

3. **Never**:
   - Merge code autonomously (PR review required)
   - Skip confidence checks (human escalation mandatory at <0.7)
   - Hardcode credentials or secrets
   - Execute C2+ actions without approval

4. **Test As You Go**:
   - Build incrementally with validation
   - Test each handler before moving to next
   - Document issues immediately in .eva-memory.json

### Execution Evidence Rule

For every implementation step:

1. **How to Run**: Exact command/process to execute
2. **Expected Outcome**: What success looks like (files, output, behavior)
3. **Verification**: How to confirm it worked

**Example**:

```
Step: Create master SKILL.md

How to Run:
- Navigate to: cd ~/.copilot/skills/eva-agile-crew
- Create file: SKILL.md with YAML frontmatter

Expected Outcome:
- File exists at ~/.copilot/skills/eva-agile-crew/SKILL.md
- VS Code Copilot shows @eva-agile-crew in autocomplete

Verification:
- Open VS Code Copilot chat
- Type "@eva"
- Confirm "eva-agile-crew" appears in suggestions
```

---

## 🆘 SUPPORT & ESCALATION

**Stuck?**

1. **Check Memory**: `eva-orchestrator/.eva-memory.json` for similar issues
2. **Search Docs**: `eva-orchestrator/docs/` for patterns and lessons
3. **Review Examples**: `scripts/p02-*.ps1` for tool patterns
4. **Create Issue**: Document blocker in GitHub issue with:
   - What you tried
   - Expected vs actual behavior
   - Relevant logs/errors
   - Steps to reproduce

**Escalation Path**:
- Self-service: Memory files, docs, past PRs
- Documentation: Create issue with detailed context
- Project Owner: Marco Presta (for strategic decisions)

---

## 📅 TIMELINE ESTIMATE

**Total**: 54 hours (~7 working days)

- Phase 0 (Bootstrap): 2 hours
- Phase 1 (Foundation): 6 hours
- Phase 2 (Personas): 12 hours
- Phase 3 (Handlers): 16 hours
- Phase 4 (Orchestration): 10 hours
- Phase 5 (Validation): 8 hours

**Recommended Pace**: 2 hours/day = 27 days | 4 hours/day = 14 days | 8 hours/day = 7 days

---

## 🎓 LEARNING OUTCOMES

By completing this implementation, you will:

- ✅ Understand agent persona design patterns
- ✅ Master GitHub Copilot skill creation
- ✅ Implement P16 awareness protocol
- ✅ Build P21 provenance logging
- ✅ Create P19 action classification
- ✅ Design workflow orchestration systems
- ✅ Apply government-grade governance patterns

---

**Version**: 1.0.0
**Last Updated**: January 15, 2026
**Next Review**: After Phase 5 completion

---

## 🍁 Remember: Canada-First Principles

Build the world's best AI governance platform **for Canada**. Let quality speak globally.

**Quality > Speed** | **Traceability > Convenience** | **Human Accountability > Automation**

🚀 Ad Astra - Build the runway while we take off.
