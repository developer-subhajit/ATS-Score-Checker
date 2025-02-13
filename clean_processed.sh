#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Print with color
print_status() {
    echo -e "${YELLOW}>>> $1${NC}"
}

print_success() {
    echo -e "${GREEN}$1${NC}"
}

print_error() {
    echo -e "${RED}ERROR: $1${NC}"
}

# Directories to clean
DIRS=(
    "data/processed"
    "data/jobs"
    "data/raw"
)

# Function to clean a directory
clean_directory() {
    local dir=$1
    
    # Check if directory exists
    if [ ! -d "$dir" ]; then
        print_error "Directory $dir does not exist"
        return 1
    fi
    
    print_status "Cleaning directory: $dir"
    
    # Remove all files except .gitkeep
    find "$dir" -type f ! -name '.gitkeep' -exec rm -f {} +
    
    if [ $? -eq 0 ]; then
        print_success "Successfully cleaned $dir"
    else
        print_error "Failed to clean $dir"
        return 1
    fi
}

# Main execution
print_status "Starting cleanup process..."

# Process each directory
for dir in "${DIRS[@]}"; do
    clean_directory "$dir"
done

print_success "Cleanup complete!" 