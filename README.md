# POC #1: Automated AI Workflow Pattern - Agent Skills Framework

## Overview

This POC demonstrates how to generalize the EVA Foundation documentation generator into a reusable **Agent Skills Framework** that can be applied to diverse AI automation tasks beyond documentation generation.

## Vision

Transform the successful config-driven AI automation pattern into a composable skills framework compatible with:
- **GitHub Copilot Agent Skills** (MCP integration)
- **Azure AI Foundry Agent Orchestration** (future migration path)
- **Standalone Python Agent Framework** (current implementation)

## Core Objectives

1. **Extract Reusable Patterns**: Distill the documentation generator into base classes and interfaces
2. **Create Skill Abstraction**: Define agent skills as pluggable, manifest-driven components
3. **Build Orchestrator**: Implement skill chaining and workflow coordination
4. **Enable Extensibility**: Allow new skills to be added without modifying core framework

## Architecture

```
agent-skills/
├── base/
│   ├── agent_skill_base.py      # Abstract base class for all skills
│   ├── prompt_template.py       # Prompt engineering framework
│   ├── validator_framework.py   # Quality validation abstraction
│   └── evidence_collector.py    # Audit trail system
├── skills/
│   ├── documentation_generator/ # Refactored from generate-docs.py
│   ├── code_generator/          # New skill: AI-powered code generation
│   └── architecture_analyzer/   # New skill: System architecture analysis
└── orchestrator/
    ├── skill_orchestrator.py    # Workflow coordination engine
    └── skill_manifest_loader.py # Dynamic skill loading from YAML

skill-manifests/
├── documentation-generator.yaml  # Skill configuration
├── code-generator.yaml
└── architecture-analyzer.yaml
```

## Key Components

### 1. AgentSkillBase (Abstract Base Class)

Defines the contract for all agent skills:

```python
class AgentSkillBase(ABC):
    @abstractmethod
    async def execute(self, input_data: Dict) -> Dict:
        """Execute the skill's primary function"""
        pass
    
    @abstractmethod
    def validate_input(self, input_data: Dict) -> bool:
        """Validate input before execution"""
        pass
    
    @abstractmethod
    def validate_output(self, output_data: Dict) -> bool:
        """Validate output after execution"""
        pass
    
    @abstractmethod
    def collect_evidence(self) -> Dict:
        """Collect audit trail of execution"""
        pass
```

### 2. Skill Manifest System

YAML-based skill configuration:

```yaml
skill:
  name: "documentation-generator"
  version: "1.0.0"
  description: "Generates technical documentation using AI"
  
  inputs:
    - name: "config_file"
      type: "path"
      required: true
    - name: "phase"
      type: "integer"
      default: null
  
  outputs:
    - name: "generated_files"
      type: "list[path]"
    - name: "validation_report"
      type: "dict"
  
  llm_config:
    provider: "azure_openai"
    deployment: "gpt-4.1-mini"
    timeout: 300
    temperature: 0.7
  
  validators:
    - type: "yaml_validator"
    - type: "requirement_id_validator"
    - type: "traceability_validator"
```

### 3. Skill Orchestrator

Coordinates multi-skill workflows:

```python
orchestrator = SkillOrchestrator()

# Load skills from manifests
orchestrator.load_skill("documentation-generator")
orchestrator.load_skill("diagram-generator")
orchestrator.load_skill("html-builder")

# Execute workflow
workflow = WorkflowBuilder()
    .add_step("generate-docs", inputs={"config": "file-specs.yaml"})
    .add_step("generate-diagrams", depends_on="generate-docs")
    .add_step("build-html", depends_on=["generate-docs", "generate-diagrams"])
    .build()

results = await orchestrator.execute_workflow(workflow)
```

## Proof of Concept Deliverables

### Week 1: Foundation Extraction (5 days)
- Extract AgentSkillBase from generate-docs.py
- Extract PromptTemplate system
- Extract ValidatorFramework
- Extract EvidenceCollector
- Unit tests for base classes

### Week 2: First Skills + Orchestrator (5 days)
- Refactor generate-docs.py as DocumentationGeneratorSkill
- Create skill manifest system
- Build SkillOrchestrator MVP
- Integration tests

### Week 3: Additional Skills + Documentation (5 days)
- Create CodeGeneratorSkill (new capability)
- Create ArchitectureAnalyzerSkill (new capability)
- Demonstrate skill chaining workflow
- Comprehensive documentation

## Success Metrics

- ✅ **Reusability**: Create 3+ skills from same base framework
- ✅ **Extensibility**: Add new skill in <4 hours without modifying core
- ✅ **Compatibility**: Skills work standalone and in orchestrated workflows
- ✅ **Migration Path**: Architecture compatible with Azure AI Foundry patterns

## Integration with POC #2

POC #1 provides the framework, POC #2 provides skills:
- **DocumentationGeneratorSkill**: Existing capability (refactored)
- **DiagramGeneratorSkill**: New capability from POC #2
- **MarkdownEnhancerSkill**: New capability from POC #2
- **MkDocsBuilderSkill**: New capability from POC #2

Workflow chaining:
```
generate-docs → generate-diagrams → enhance-markdown → build-mkdocs
```

## Future Enhancements

- **MCP Integration**: Package skills as Model Context Protocol servers for GitHub Copilot
- **Azure AI Foundry Migration**: Convert to Azure AI Agent Service
- **Skill Marketplace**: Create skill catalog with discovery and installation
- **Multi-Agent Orchestration**: Enable skills to spawn sub-agents
- **Performance Optimization**: Parallel skill execution, caching, incremental updates

## Getting Started

See [PLAN.md](PLAN.md) for detailed 3-week implementation plan.

## Directory Location

This POC is located at: `docs/eva-foundation/projects/02-poc-agent-skills/`
