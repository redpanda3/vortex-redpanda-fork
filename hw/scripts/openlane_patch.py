#!/usr/bin/env python3

##patch file for openlane:
##  vortex synthesis in yosys, by yuda(redpanda3)

import os
import argparse
import re
import glob


def directory_reader(input_dir):
    sv_files = []
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.sv'):
                sv_files.append(os.path.join(root, file))
    if not sv_files:
        print(f"No .sv files found in {input_dir}")
        return
    return sv_files


def file_reader(file_path):
    # Read the input system Verilog file
    try:
        with open(file_path, 'r') as file:
            code = file.read()
            return code
    except FileNotFoundError:
        print(f"Error: The input file {file_path} was not found.")
        return
    except Exception as e:
        print(f"An error occurred while reading the input file: {e}")
        return


def file_writer(code, file_path):
    # Write the transformed code to the output file
    try:
        with open(file_path, 'w') as file:
            file.write(code)
    except Exception as e:
        print(f"Error writing output file: {e}")
        return


def patch_sformatf_verilog_code(file_path, patterns):
    code = file_reader(file_path)
    # Perform the replacement using re.sub

    # For logging pattern matches
    total_substitutions = 0

    # Perform transformations
    for pattern, replacement in patterns:
        # Use re.subn to get the count of substitutions
        new_code, num_subs = re.subn(pattern, replacement, code, flags=re.DOTALL)
        if num_subs > 0:
            print(f"Pattern '{pattern}' matched {num_subs} time(s) in {file_path}")
            total_substitutions += num_subs
        code = new_code  # Update the code with the substitutions

    if total_substitutions > 0:
        print(f"Total substitutions made in {file_path}: {total_substitutions}")
    else:
        print(f"No substitutions made in {file_path}")

    # Write the transformed code to the output file
    file_writer(code, file_path)

def comment_fatal_blocks(input_file, output_file):
    with open(input_file, 'r') as infile:
        lines = infile.readlines()
    
    # Stack to keep track of 'initial begin' blocks and nesting
    block_stack = []
    # List to keep track of blocks to comment (start and end line numbers)
    fatal_blocks = []
    
    # First pass: Identify blocks containing '$fatal'
    for line_no, line in enumerate(lines):
        stripped_line = line.strip()
        
        # Detect 'initial begin' (supports variations in spacing)
        if stripped_line.startswith('initial begin'):
            # Start a new block
            block = {
                'start_line_no': line_no,
                'needs_comment': False
            }
            block_stack.append(block)
        elif stripped_line == 'end' or stripped_line.startswith('end '):
            # End of a block
            if block_stack:
                block = block_stack.pop()
                block['end_line_no'] = line_no
                if block['needs_comment']:
                    # Mark the block for commenting
                    fatal_blocks.append((block['start_line_no'], block['end_line_no']))
            else:
                # Mismatched 'end', ignore or handle error as needed
                pass
        else:
            # Check for '$fatal' in the line
            if '$fatal' in line:
                if block_stack:
                    # Mark the current block as needing comment
                    block_stack[-1]['needs_comment'] = True
                else:
                    # '$fatal' outside any 'initial begin ... end' block
                    pass  # Handle as needed
    
    # Create a set of line numbers that need to be commented
    lines_to_comment = set()
    for start_line_no, end_line_no in fatal_blocks:
        lines_to_comment.update(range(start_line_no, end_line_no + 1))
    
    # Second pass: Write out the lines, commenting as needed
    with open(output_file, 'w') as outfile:
        for line_no, line in enumerate(lines):
            if line_no in lines_to_comment:
                outfile.write('// ' + line)
            else:
                outfile.write(line)

# def patch_mixed_blocking_assignment_verilog_code(file_path):

#     code = file_reader(file_path)

#     # Regex pattern to match 'assign' statements starting with 'inp*'
#     pattern = r'^(\s*)assign\s+(inp\w+\[\d+\])\s*=\s*(\w+);\s*$'

#     # Initialize variables
#     new_assignments = ''
#     lines_to_remove = []
#     insert_pos = None

#     # Split the code into lines for processing
#     code_lines = code.split('\n')

#     # Iterate over the lines to find matches and collect their indices
#     for idx, line in enumerate(code_lines):
#         match = re.match(pattern, line)
#         if match:
#             indentation, lhs, rhs = match.groups()
#             # Build the new assignment with non-blocking assignment
#             new_assignments += f'{indentation}    {lhs} <= {rhs};\n'
#             lines_to_remove.append(idx)
#             # Record the insert position at the first match
#             if insert_pos is None:
#                 insert_pos = idx

#     # Only proceed if there are matches
#     if new_assignments:
#         # Remove the matched lines from the original code
#         # We iterate in reverse order to avoid index shifting
#         for idx in reversed(lines_to_remove):
#             del code_lines[idx]

#         # Create the 'always @(*)' block
#         indentation = code_lines[insert_pos] if insert_pos < len(code_lines) else ''
#         always_block = f'{new_assignments}{indentation}end'

#         # Insert the 'always @(*)' block
#         code_lines.insert(insert_pos, f'{indentation}always @(*) begin')
#         code_lines.insert(insert_pos + 1, always_block)
#     else:
#         # If there are no matches, do not modify the code
#         return code

#     # Reconstruct the code
#     transformed_code = '\n'.join(code_lines)

#     # Clean up any extra blank lines
#     transformed_code = re.sub(r'\n\s*\n', '\n\n', transformed_code)

#     # Write the transformed code to the output file
#     file_writer(code, file_path)


def main():
    parser = argparse.ArgumentParser(description='Patch Verilog code for synthesis.')
    parser.add_argument('input_dir', help='Path to the directory containing .sv files')
    # Add more arguments as needed

    args = parser.parse_args()
    input_dir = args.input_dir  

    # Get all .sv files in the input directory recursively  
    sv_files = directory_reader(input_dir)
    
    pattern_list = [
        (r'\$sformatf\(\s*"[^"]*?%0d"\s*,\s*(\w+)\s*\)', r'\1'),
        (r'\$sformatf\(\s*(?:/\*.*?\*/\s*)*"core"\s*\)', r'CORE_ID'),
        (r'\$sformatf\(\s*"core"\s*\)', r'CORE_ID'),
        (r'\$sformatf\(\s*"%s-\w+"\s*,\s*(\w+)\s*\)', r'\1'),
        (r'\$sformatf\(\s*"%s%0d"\s*,\s*\w+\s*,\s*(\w+)\s*\)', r'\1'),
        (r'\$sformatf\(\s*"%s-\w+%0?d"\s*,\s*[\$\w]+\s*,\s*([\$\w]+)\s*\)', r'\1')

    ]

    # Process each file and overwrite it
    for file_path in sv_files:
        patch_sformatf_verilog_code(file_path, pattern_list)
        comment_fatal_blocks(file_path, file_path)


    # # Process each file and overwrite it
    # for file_path in sv_files:
    #     patch_mixed_blocking_assignment_verilog_code(file_path)
        

    print("Transformation complete.")

# Example usage:
if __name__ == "__main__":
    main()


