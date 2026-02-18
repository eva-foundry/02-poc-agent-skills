"""
Documentation Generation Workflow
Orchestrates RepoResearcher → DeltaGenerator → ValidationOrchestrator

This workflow demonstrates the Agent Skills Framework by chaining three skills
to implement repo-aware delta generation for documentation.

Workflow Steps:
1. RepoResearcherSkill: Find code evidence for documentation topic
2. DeltaGeneratorSkill: Generate doc using baseline + evidence
3. ValidationOrchestratorSkill: Validate output with retry logic

Usage:
    python orchestrator/documentation_workflow.py \
        --file security-architecture.md \
        --topic "security architecture authentication" \
        --scope backend
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent / "agent-skills" / "base"))
sys.path.insert(0, str(Path(__file__).parent.parent / "agent-skills" / "skills"))

from agent_skill_base import AgentSkillBase
from repo_researcher_skill import RepoResearcherSkill
from delta_generator_skill import DeltaGeneratorSkill
from validation_orchestrator_skill import ValidationOrchestratorSkill

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn


class DocumentationWorkflow:
    """
    Orchestrates multi-skill workflow for documentation generation.
    
    Implements the repo-aware delta generation pattern using:
    - RepoResearcherSkill for evidence collection
    - DeltaGeneratorSkill for content generation
    - ValidationOrchestratorSkill for quality assurance
    """
    
    def __init__(
        self,
        workspace_root: Path,
        skill_manifests_dir: Path,
        state_file: Optional[Path] = None
    ):
        """
        Initialize workflow orchestrator.
        
        Args:
            workspace_root: Root directory of workspace
            skill_manifests_dir: Directory containing skill YAML configs
            state_file: Optional path to workflow state file
        """
        self.workspace_root = workspace_root
        self.skill_manifests_dir = skill_manifests_dir
        self.console = Console()
        
        # Initialize state
        self.state = {
            "workflow_id": f"doc-gen-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            "started_at": None,
            "completed_at": None,
            "status": "initialized",
            "steps": {}
        }
        
        self.state_file = state_file or (workspace_root / "logs" / f"{self.state['workflow_id']}.json")
        
        # Initialize skills
        self.researcher: Optional[RepoResearcherSkill] = None
        self.generator: Optional[DeltaGeneratorSkill] = None
        self.validator: Optional[ValidationOrchestratorSkill] = None
    
    def _init_skills(self) -> None:
        """Initialize all skills with their configurations"""
        self.console.print("[cyan]Initializing skills...[/cyan]")
        
        try:
            # Initialize RepoResearcherSkill
            researcher_config = self.skill_manifests_dir / "repo-researcher.yaml"
            self.researcher = RepoResearcherSkill(
                workspace_root=self.workspace_root,
                config_path=researcher_config,
                log_level="INFO"
            )
            self.console.print("[green]✅ RepoResearcherSkill initialized[/green]")
            
            # Initialize DeltaGeneratorSkill
            generator_config = self.skill_manifests_dir / "delta-generator.yaml"
            self.generator = DeltaGeneratorSkill(
                workspace_root=self.workspace_root,
                config_path=generator_config,
                log_level="INFO"
            )
            self.console.print("[green]✅ DeltaGeneratorSkill initialized[/green]")
            
            # Initialize ValidationOrchestratorSkill
            validator_config = self.skill_manifests_dir / "validation-orchestrator.yaml"
            self.validator = ValidationOrchestratorSkill(
                workspace_root=self.workspace_root,
                config_path=validator_config,
                log_level="INFO"
            )
            self.console.print("[green]✅ ValidationOrchestratorSkill initialized[/green]")
            
        except Exception as e:
            self.console.print(f"[red]❌ Skill initialization failed: {e}[/red]")
            raise
    
    def _save_state(self) -> None:
        """Save workflow state to file"""
        try:
            self.state_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(self.state, f, indent=2)
        except Exception as e:
            self.console.print(f"[yellow]⚠️  Failed to save state: {e}[/yellow]")
    
    def execute(
        self,
        file_name: str,
        topic: str,
        scope: Optional[str] = None,
        search_terms: Optional[list] = None,
        max_validation_retries: int = 3
    ) -> Dict[str, Any]:
        """
        Execute complete workflow for one document.
        
        Args:
            file_name: Name of document to generate
            topic: Main topic for research
            scope: Optional scope (backend, frontend, etc.)
            search_terms: Optional specific terms to search
            max_validation_retries: Max retries for validation failures
            
        Returns:
            Workflow result with output from all steps
        """
        self.state["started_at"] = datetime.now().isoformat()
        self.state["status"] = "running"
        self.state["input"] = {
            "file_name": file_name,
            "topic": topic,
            "scope": scope,
            "search_terms": search_terms
        }
        
        self.console.print(Panel.fit(
            f"[bold cyan]Documentation Generation Workflow[/bold cyan]\n"
            f"File: {file_name}\n"
            f"Topic: {topic}\n"
            f"Scope: {scope or 'all'}",
            border_style="cyan"
        ))
        
        # Initialize skills
        self._init_skills()
        
        try:
            # STEP 1: Research - Find code evidence
            self.console.print("\n[bold]Step 1: Research[/bold] - Finding code evidence")
            
            evidence = self.researcher.execute(
                topic=topic,
                scope=scope,
                search_terms=search_terms
            )
            
            self.state["steps"]["research"] = {
                "status": "completed",
                "completed_at": datetime.now().isoformat(),
                "summary": evidence["summary"]
            }
            self._save_state()
            
            # STEP 2: Generate - Create document using baseline + evidence
            self.console.print("\n[bold]Step 2: Generate[/bold] - Creating document from baseline + evidence")
            
            generation_result = self.generator.execute(
                file_name=file_name,
                evidence=evidence,
                save_output=True
            )
            
            self.state["steps"]["generation"] = {
                "status": "completed",
                "completed_at": datetime.now().isoformat(),
                "summary": generation_result["summary"],
                "output_path": generation_result["output_path"]
            }
            self._save_state()
            
            # STEP 3: Validate - Check quality with retry logic
            self.console.print("\n[bold]Step 3: Validate[/bold] - Checking quality")
            
            # Define regeneration function for retry logic
            def regenerate_with_feedback(feedback: str) -> str:
                """Regenerate document with validation feedback"""
                self.console.print(f"[yellow]Regenerating with corrections...[/yellow]")
                
                # Add feedback to evidence for next iteration
                evidence["validation_feedback"] = feedback
                
                result = self.generator.execute(
                    file_name=file_name,
                    evidence=evidence,
                    save_output=True
                )
                
                return result["content"]
            
            # Execute validation with retry
            validation_result = self.validator.execute_with_retry(
                content=generation_result["content"],
                file_name=file_name,
                regenerate_func=regenerate_with_feedback,
                max_retries=max_validation_retries
            )
            
            self.state["steps"]["validation"] = {
                "status": "completed" if validation_result["passed"] else "failed",
                "completed_at": datetime.now().isoformat(),
                "summary": validation_result["summary"],
                "retry_history": validation_result.get("retry_history", [])
            }
            self._save_state()
            
            # Determine overall workflow status
            workflow_passed = validation_result["passed"]
            self.state["status"] = "completed" if workflow_passed else "failed"
            self.state["completed_at"] = datetime.now().isoformat()
            
            # Calculate total duration
            start = datetime.fromisoformat(self.state["started_at"])
            end = datetime.fromisoformat(self.state["completed_at"])
            duration = (end - start).total_seconds()
            self.state["duration_seconds"] = duration
            
            self._save_state()
            
            # Display summary
            self._display_summary(workflow_passed)
            
            return {
                "workflow_id": self.state["workflow_id"],
                "passed": workflow_passed,
                "evidence": evidence,
                "generation": generation_result,
                "validation": validation_result,
                "state": self.state
            }
            
        except Exception as e:
            self.state["status"] = "error"
            self.state["error"] = str(e)
            self.state["completed_at"] = datetime.now().isoformat()
            self._save_state()
            
            self.console.print(f"\n[red]❌ Workflow failed: {e}[/red]")
            raise
    
    def _display_summary(self, passed: bool) -> None:
        """Display workflow execution summary"""
        status_emoji = "✅" if passed else "❌"
        status_color = "green" if passed else "red"
        status_text = "PASSED" if passed else "FAILED"
        
        research_summary = self.state["steps"]["research"]["summary"]
        generation_summary = self.state["steps"]["generation"]["summary"]
        validation_summary = self.state["steps"]["validation"]["summary"]
        
        summary_text = f"""
[bold {status_color}]{status_emoji} Workflow {status_text}[/bold {status_color}]

[bold]Duration:[/bold] {self.state['duration_seconds']:.1f}s

[bold]Step 1: Research[/bold]
  • Files found: {research_summary['total_files']}
  • Evidence pieces: {research_summary['total_matches']}
  • Confidence: {research_summary['confidence']}

[bold]Step 2: Generation[/bold]
  • Total sections: {generation_summary['total']}
  • Updated: {generation_summary['updated']}
  • Unchanged: {generation_summary['unchanged']}
  • Errors: {generation_summary['errors']}

[bold]Step 3: Validation[/bold]
  • Validators run: {validation_summary['total_validators']}
  • Passed: {validation_summary['passed_validators']}
  • Failed: {validation_summary['failed_validators']}
  • Total errors: {validation_summary['total_errors']}
  • Total warnings: {validation_summary['total_warnings']}
"""
        
        if "retry_history" in self.state["steps"]["validation"]:
            retry_count = len(self.state["steps"]["validation"]["retry_history"])
            summary_text += f"  • Retry attempts: {retry_count}\n"
        
        summary_text += f"\n[bold]Output:[/bold] {self.state['steps']['generation']['output_path']}"
        summary_text += f"\n[bold]State saved:[/bold] {self.state_file}"
        
        self.console.print(Panel(summary_text, border_style="cyan", title="Workflow Summary"))


def main():
    """CLI entry point for workflow"""
    parser = argparse.ArgumentParser(description="Documentation generation workflow")
    
    parser.add_argument(
        "--file",
        required=True,
        help="Name of document to generate (e.g., security-architecture.md)"
    )
    
    parser.add_argument(
        "--topic",
        required=True,
        help="Main topic for research (e.g., 'security architecture authentication')"
    )
    
    parser.add_argument(
        "--scope",
        default=None,
        help="Scope to narrow search (e.g., backend, frontend, functions)"
    )
    
    parser.add_argument(
        "--search-terms",
        nargs="+",
        default=None,
        help="Specific terms to search for (e.g., OAuth PKCE 'Entra ID')"
    )
    
    parser.add_argument(
        "--max-retries",
        type=int,
        default=3,
        help="Maximum validation retry attempts (default: 3)"
    )
    
    parser.add_argument(
        "--workspace-root",
        type=Path,
        default=Path(__file__).parents[5],
        help="Workspace root directory"
    )
    
    args = parser.parse_args()
    
    # Setup paths
    workspace_root = args.workspace_root
    skill_manifests_dir = workspace_root / "docs" / "eva-foundation" / "projects" / "02-poc-agent-skills" / "skill-manifests"
    
    # Initialize workflow
    workflow = DocumentationWorkflow(
        workspace_root=workspace_root,
        skill_manifests_dir=skill_manifests_dir
    )
    
    # Execute
    try:
        result = workflow.execute(
            file_name=args.file,
            topic=args.topic,
            scope=args.scope,
            search_terms=args.search_terms,
            max_validation_retries=args.max_retries
        )
        
        sys.exit(0 if result["passed"] else 1)
        
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
