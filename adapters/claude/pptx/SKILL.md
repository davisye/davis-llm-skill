---
name: pptx
description: This skill should be used when the user asks to create PowerPoint presentations, edit .pptx files, modify slides, work with PPTX layouts, add speaker notes, or analyze presentation content. Use for any .pptx file operations.
allowed-tools: [Read, Write, Bash]
---

# PPTX Creation, Editing, and Analysis

## Overview

A user may ask you to create, edit, or analyze the contents of a .pptx file. A .pptx file is essentially a ZIP archive containing XML files and other resources that you can read or edit. You have different tools and workflows available for different tasks.

## Reading and Analyzing Content

### Text extraction
If you just need to read the text contents of a presentation, convert the document to markdown:

```bash
python -m markitdown path-to-file.pptx
```

### Raw XML access
You need raw XML access for: comments, speaker notes, slide layouts, animations, design elements, and complex formatting. For any of these features, you'll need to unpack a presentation and read its raw XML contents.

#### Key file structures
* `ppt/presentation.xml` - Main presentation metadata and slide references
* `ppt/slides/slide{N}.xml` - Individual slide contents
* `ppt/notesSlides/notesSlide{N}.xml` - Speaker notes for each slide
* `ppt/comments/modernComment_*.xml` - Comments for specific slides
* `ppt/slideLayouts/` - Layout templates for slides
* `ppt/slideMasters/` - Master slide templates
* `ppt/theme/` - Theme and styling information
* `ppt/media/` - Images and other media files

## Creating a New Presentation (without a template)

When creating a new PowerPoint presentation from scratch, use the **html2pptx** workflow to convert HTML slides to PowerPoint with accurate positioning.

### Design Principles

**CRITICAL**: Before creating any presentation, analyze the content and choose appropriate design elements:
1. Consider the subject matter, tone, industry, and mood
2. Check for branding if a company is mentioned
3. Match palette to content
4. State your design approach before writing code

### Workflow
1. Read the html2pptx reference for detailed syntax and formatting rules
2. Create an HTML file for each slide with proper dimensions (e.g., 720pt × 405pt for 16:9)
3. Create and run a JavaScript file using the html2pptx.js library to convert HTML slides to PowerPoint
4. Visual validation: Generate thumbnails and inspect for layout issues

## Editing an Existing Presentation

When editing slides in an existing PowerPoint presentation, work with the raw Office Open XML (OOXML) format.

### Workflow
1. Read the ooxml reference for detailed guidance on OOXML structure
2. Unpack the presentation: `python ooxml/scripts/unpack.py <office_file> <output_dir>`
3. Edit the XML files (primarily `ppt/slides/slide{N}.xml` and related files)
4. Validate immediately after each edit: `python ooxml/scripts/validate.py <dir> --original <file>`
5. Pack the final presentation: `python ooxml/scripts/pack.py <input_directory> <office_file>`

## Creating a New Presentation (using a template)

When you need to create a presentation that follows an existing template's design.

### Workflow
1. Extract template text AND create visual thumbnail grid
2. Analyze template and save inventory to a file
3. Create presentation outline based on template inventory
4. Duplicate, reorder, and delete slides using `rearrange.py`
5. Extract ALL text using the `inventory.py` script
6. Generate replacement text and save to JSON
7. Apply replacements using the `replace.py` script

## Dependencies

- **markitdown**: `pip install "markitdown[pptx]"`
- **pptxgenjs**: `npm install -g pptxgenjs`
- **playwright**: `npm install -g playwright`
- **react-icons**: `npm install -g react-icons react react-dom`
- **sharp**: `npm install -g sharp`
- **LibreOffice**: `sudo apt-get install libreoffice`
- **Poppler**: `sudo apt-get install poppler-utils`
- **defusedxml**: `pip install defusedxml`
