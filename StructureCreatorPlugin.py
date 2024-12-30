import ida_kernwin
import ida_idaapi
import ida_typeinf
import idaapi

class StructureCreatorFormClass(ida_kernwin.Form):
    def __init__(self, struct_def=""):
        F = ida_kernwin.Form
        super().__init__(
            """STARTITEM 1
Create/Edit Structure

<Structure definition:{text}>
""",
            {
                'text': F.MultiLineTextControl(text=struct_def, width=80, flags=ida_kernwin.Form.MultiLineTextControl.TXTF_FIXEDFONT)
            }
        )
def get_tid(ea):
    # Gets type id by ea 
    tif = ida_typeinf.tinfo_t()
    success = ida_typeinf.guess_tinfo(tif, ea)
    if success:
        return tif.get_type_name()
    else:
        return None

def get_struc(struct_tid):
    # Gets structure information by type ID
    tif = ida_typeinf.tinfo_t()
    if tif.deserialize(None, struct_tid):
        if tif.is_struct():
            return tif
    return ida_idaapi.BADADDR
    
def remove_comments(text):
    # Remove single-line comments
    lines = text.split('\n')
    processed_lines = []
    for line in lines:
        comment_pos = line.find('//')
        if comment_pos != -1:
            line = line[:comment_pos].rstrip()
        if line:
            processed_lines.append(line)
    return '\n'.join(processed_lines)

def process_structure_definition(text):
    # Add semicolons to structure fields
    lines = text.split('\n')
    processed_lines = []
    in_struct = False
    
    for line in lines:
        line = line.strip()
        if not line:
            processed_lines.append('')
            continue
            
        if '{' in line:
            in_struct = True
            processed_lines.append(line)
        elif '}' in line:
            in_struct = False
            processed_lines.append(line)
        elif in_struct and line and not line.endswith(';'):
            if not any(char in line for char in ['{', '}', ';']):
                line += ';'
            processed_lines.append(line)
        else:
            processed_lines.append(line)
            
    return '\n'.join(processed_lines)

def split_multiple_structures(text):
    # Split text into separate structures based on empty lines
    structures = []
    current_structure = []
    
    for line in text.split('\n'):
        if line.strip():
            current_structure.append(line)
        elif current_structure:
            structures.append('\n'.join(current_structure))
            current_structure = []
    
    if current_structure:
        structures.append('\n'.join(current_structure))
    
    return structures

def create_or_edit_structure():
    # Get current cursor and check if it's on a structure
    current_struct_def = ""
    
    cursor = ida_kernwin.get_screen_ea()
    
    # Get type id at cursor
    tid = get_tid(cursor)
    if tid is not None:
        # Try to get structure info
        tinfo = get_struc(tid)
        if tinfo != ida_idaapi.BADADDR:
            # If cursor is on an existing structure, get its definition
            current_struct_name = tinfo.get_type_name()
            current_struct_def = idaapi.print_tinfo(None, tinfo, '', idaapi.PRTYPE_MULTI | idaapi.PRTYPE_TYPE)

    # Create and show form
    form = StructureCreatorFormClass(current_struct_def)
    form.Compile()
    if form.Execute() != 1:
        form.Free()
        return
    
    struct_def = form.text.value
    
    form.Free()

    if not struct_def:
        ida_kernwin.warning("Structure name and definition cannot be empty!")
        return
    
    try:
        til = ida_typeinf.get_idati()
        # Remove comments
        struct_def = remove_comments(struct_def)
        # Remove semicolons from the structure definition
        struct_def = process_structure_definition(struct_def)
        
        # Split into multiple structures if present
        structures = split_multiple_structures(struct_def)
        
        # Process structures in reverse order (bottom to top)
        for struct in reversed(structures):
            # Parse the structure definition
            result = ida_typeinf.idc_parse_types(struct, 0)
            
            if result != 0:
                ida_kernwin.warning(f"Error parsing structure definition:\n{struct}")
                continue
            else:
                print(f"Structure successfully created/updated:\n{struct}\n")
            
    except Exception as e:
        ida_kernwin.warning(f"Error creating structure: {str(e)}")

class StructureCreatorPlugin(idaapi.plugin_t):
    flags = idaapi.PLUGIN_UNL
    comment = "Structure Creator Plugin By Cynic"
    help = "Creates or edits structures"
    wanted_name = "Structure Creator"
    wanted_hotkey = "Ctrl-Alt-S"
    
    def init(self):
        # Show notification about successful plugin loading
        ida_kernwin.msg("Structure Creator Plugin by Cynic has been successfully loaded!\n")
        return idaapi.PLUGIN_OK
    
    def run(self, arg):
        create_or_edit_structure()
        
    def term(self):
        pass

def PLUGIN_ENTRY():
    return StructureCreatorPlugin()
