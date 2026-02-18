"""
Quick test script for Agent Skills Framework implementation

This script tests the documentation workflow on a single file
to validate the implementation before running full suite.
"""

import sys
from pathlib import Path

# Add orchestrator to path
sys.path.insert(0, str(Path(__file__).parent))

from orchestrator.documentation_workflow import DocumentationWorkflow
from rich.console import Console

console = Console()

def test_security_architecture():
    """Test workflow on security-architecture.md"""
    
    console.print("\n[bold cyan]═══════════════════════════════════════════[/bold cyan]")
    console.print("[bold cyan]  Agent Skills Framework - Quick Test[/bold cyan]")
    console.print("[bold cyan]═══════════════════════════════════════════[/bold cyan]\n")
    
    # Setup paths
    workspace_root = Path(__file__).parents[4]
    skill_manifests_dir = Path(__file__).parent / "skill-manifests"
    
    console.print(f"[dim]Workspace: {workspace_root}[/dim]")
    console.print(f"[dim]Manifests: {skill_manifests_dir}[/dim]\n")
    
    # Initialize workflow
    console.print("[cyan]Initializing workflow...[/cyan]")
    workflow = DocumentationWorkflow(
        workspace_root=workspace_root,
        skill_manifests_dir=skill_manifests_dir
    )
    
    # Execute test
    try:
        result = workflow.execute(
            file_name="security-architecture.md",
            topic="security architecture authentication authorization",
            scope="backend",
            search_terms=["OAuth", "PKCE", "Entra ID", "Azure AD", "azure_credential"],
            max_validation_retries=3
        )
        
        # Display result
        console.print("\n[bold green]✅ Test completed successfully![/bold green]")
        
        return result
        
    except Exception as e:
        console.print(f"\n[bold red]❌ Test failed: {e}[/bold red]")
        import traceback
        console.print(f"[dim]{traceback.format_exc()}[/dim]")
        return None


if __name__ == "__main__":
    result = test_security_architecture()
    
    if result and result["passed"]:
        console.print("\n[bold green]🎉 All systems operational![/bold green]")
        sys.exit(0)
    else:
        console.print("\n[bold red]⚠️  Test did not pass validation[/bold red]")
        sys.exit(1)
