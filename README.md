# Structure Creator Plugin for IDA Pro

## Overview
The Structure Creator Plugin is a powerful utility for IDA Pro that enables users to create and edit data structures directly within the IDA Pro interface. Developed by Cynic, this plugin streamlines the process of structure manipulation with an intuitive form-based interface.

## Features
- Create new structures with a user-friendly form interface
- Edit existing structures by selecting them in the disassembly view
- Support for multiple structure definitions in a single input
- Automatic semicolon handling for structure fields
- Comment removal functionality
- Intelligent structure parsing and validation
- Support for complex nested structures

## Hotkey
The plugin is accessible via the hotkey combination: `Ctrl-Alt-S`

## Technical Details
### Core Components
1. **StructureCreatorFormClass**: Handles the UI form for structure input
2. **Type Information Processing**:
   - `get_tid()`: Retrieves type information at a specific address
   - `get_struc()`: Obtains structure information from type ID
   - `remove_comments()`: Cleans up structure definitions by removing comments
   - `process_structure_definition()`: Ensures proper syntax with semicolons
   - `split_multiple_structures()`: Handles multiple structure definitions

### Processing Flow
1. Captures current cursor position
2. Checks for existing structure at cursor location
3. Displays input form with current structure (if any)
4. Processes user input:
   - Removes comments
   - Adds necessary semicolons
   - Splits multiple structures
   - Validates and creates/updates structures

## Usage
1. Position cursor on an existing structure (optional)
2. Press `Ctrl-Alt-S` to open the Structure Creator form
3. Enter or modify structure definition
4. Submit to create/update the structure

## Installation:
   - Place the plugin file in IDA Pro's plugins directory

## Example Structure Definition
```c
struct example_struct {
    int field1;
    char field2[32];
    void* ptr_field;
};
