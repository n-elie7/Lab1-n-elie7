#!/bin/bash

# Define directories and files
ARCHIVE_DIR="archive"
LOG_FILE="organizer.log"

# Function to log messages
log_message() {
    echo "$1" | tee -a "$LOG_FILE"
}

# Function to get timestamp in format YYYYMMDD-HHMMSS
get_timestamp() {
    date +"%Y%m%d-%H%M%S"
}

# Main script
echo "=================================="
echo "    CSV File Organizer"
echo "=================================="
echo ""

# Step 1: Check if archive directory exists, create if not
if [ ! -d "$ARCHIVE_DIR" ]; then
    echo "Creating archive directory..."
    mkdir "$ARCHIVE_DIR"
    log_message "[$(date '+%Y-%m-%d %H:%M:%S')] Created archive directory: $ARCHIVE_DIR"
else
    echo "Archive directory already exists."
fi

echo ""

# Step 2: Find all CSV files in current directory
csv_files=(*.csv)

# Check if any CSV files exist
if [ ! -e "${csv_files[0]}" ]; then
    echo "No CSV files found in current directory."
    log_message "[$(date '+%Y-%m-%d %H:%M:%S')] No CSV files found to archive."
    exit 0
fi

# Step 3: Process each CSV file
csv_count=0
for csv_file in "${csv_files[@]}"; do
    # Skip if it's actually a pattern (no match)
    if [ ! -f "$csv_file" ]; then
        continue
    fi
    
    # Generate timestamp
    timestamp=$(get_timestamp)
    
    # Extract filename without extension
    filename="${csv_file%.csv}"
    
    # Create new filename with timestamp
    new_filename="${filename}-${timestamp}.csv"
    new_filepath="${ARCHIVE_DIR}/${new_filename}"
    
    echo "Processing: $csv_file"
    
    # Log the archiving action
    {
        echo ""
        echo "=========================================="
        echo "Archived: $(date '+%Y-%m-%d %H:%M:%S')"
        echo "Original: $csv_file"
        echo "New Name: $new_filename"
        echo "Location: $ARCHIVE_DIR"
        echo "=========================================="
        echo ""
        echo "File Contents:"
        echo "------------------------------------------"
        cat "$csv_file"
        echo "------------------------------------------"
        echo ""
    } >> "$LOG_FILE"
    
    # Move and rename the file
    mv "$csv_file" "$new_filepath"
    
    if [ $? -eq 0 ]; then
        echo "Successfully archived as: $new_filename"
        ((csv_count++))
    else
        echo "Failed to archive: $csv_file"
        log_message "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: Failed to archive $csv_file"
    fi
    
    echo ""
done

# Summary
echo "=================================="
echo "Archive Complete!"
echo "Files archived: $csv_count"
echo "Log file: $LOG_FILE"
echo "=================================="

log_message "[$(date '+%Y-%m-%d %H:%M:%S')] Archiving session complete. Total files: $csv_count"
