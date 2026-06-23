import os
from pathlib import Path
from OmniPhysiBoSS.utils.logger import get_custom_logger

# Initialize logger for the generation process
logger = get_custom_logger(__name__)

def generate_toc():
    """
    Generates a structured Markdown Table of Contents for the 'explanations' 
    directory, using README.md files as section headers.
    """
    # Define the base directory as the current working directory
    base_dir = Path.cwd()
    #TODO - set base directory for documentation 
    target_dir = base_dir / "docs/explanations"

    # Validate target directory existence
    if not target_dir.is_dir():
        logger.error("Target directory %s not found in current path %s", target_dir, base_dir)
        print(f"Error: 'explanations' directory not found in {base_dir}")
        return

    toc_lines = ["## Table of Contents", ""]
    
    # Walk through the directory structure
    for root, dirs, files in sorted(os.walk(target_dir)):
        ## Calculate relative path for structure mapping
        rel_root = Path(root).relative_to(target_dir)
        if rel_root == Path("."):
            continue
            
        # Identify the README file for the current directory
        readme_path = Path(root) / "README.md"
        
        # Prepare section header using README link
        section_name = os.path.basename(root).replace("_", " ").title()
        relative_readme = readme_path.relative_to(base_dir)
        toc_lines.append(f"- **[{section_name}]({relative_readme})**")
        
        # Add non-README file links as sub-items
        for file in sorted(files):
            if file.endswith(".md") and file != "README.md":
                file_path = Path(root) / file
                name = file.replace(".md", "").replace("_", " ").title()
                
                # Create link relative to the base directory
                relative_link = file_path.relative_to(base_dir)
                toc_lines.append(f"  - [{name}]({relative_link})")

    # Final output generation
    print("\n".join(toc_lines))

if __name__ == "__main__":
    generate_toc()