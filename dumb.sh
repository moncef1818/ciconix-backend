#!/bin/bash

# dump_project_files.sh - Dump all git-tracked files content into single file
# Usage: ./dump_project_files.sh [output_file]

OUTPUT_FILE="${1:-project_files_dump.txt}"

echo "🚀 Dumping all $(git ls-files | wc -l) git-tracked files into '$OUTPUT_FILE'..."
echo "📅 Generated: $(date)"
echo "📂 Project: $(basename $(pwd))"
echo "═══════════════════════════════════════════════════════════════════════════════"
echo

# Clear output file
> "$OUTPUT_FILE"

# Function to add file content with separator
add_file() {
    local file="$1"
    local rel_path=$(git ls-files --full-name "$file" 2>/dev/null || echo "$file")
    
    echo "📄 FILE: $rel_path" >> "$OUTPUT_FILE"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" >> "$OUTPUT_FILE"
    echo "Lines: $(wc -l < "$file") | Size: $(du -h "$file" | cut -f1)" >> "$OUTPUT_FILE"
    echo >> "$OUTPUT_FILE"
    
    # Escape special characters and handle binary files
    if file "$file" | grep -q "text"; then
        cat "$file" >> "$OUTPUT_FILE"
    else
        echo "[BINARY/NON-TEXT FILE - $(file "$file")]" >> "$OUTPUT_FILE"
    fi
    
    echo >> "$OUTPUT_FILE"
    echo "───────────────────────────────────────────────────────────────────────────────" >> "$OUTPUT_FILE"
    echo >> "$OUTPUT_FILE"
}

# Process all git-tracked files
export -f add_file
git ls-files | while read -r file; do
    if [[ -f "$file" ]]; then
        add_file "$file"
    fi
done

# Add summary
echo "✅ Dump completed!" >> "$OUTPUT_FILE"
echo "📊 Total files: $(git ls-files | wc -l)" >> "$OUTPUT_FILE"
echo "💾 Output file: $OUTPUT_FILE ($(du -h "$OUTPUT_FILE" | cut -f1))" >> "$OUTPUT_FILE"

echo "✅ Done! Check '$OUTPUT_FILE'"
echo "📏 File size: $(du -h "$OUTPUT_FILE" | cut -f1)"
echo "📊 Total files processed: $(git ls-files | wc -l)"
