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

print_error() {
    echo -e "${RED}ERROR: $1${NC}"
}

# Initialize commit message variable
commit_message=""

# Parse command line arguments
while getopts ":m:" opt; do
  case $opt in
    m)
      commit_message="$OPTARG"
      ;;
    \?)
      print_error "Invalid option: -$OPTARG"
      exit 1
      ;;
    :)
      print_error "Option -$OPTARG requires an argument."
      exit 1
      ;;
  esac
done

# Check if there are any changes to commit
if [ -z "$(git status --porcelain)" ]; then
    echo -e "${GREEN}Nothing to commit. Working tree clean.${NC}"
    exit 0
fi

# Show current status
print_status "Current git status:"
git status

# Add all changes
print_status "Adding all changes..."
git add .

# If no commit message provided via flag, prompt for one
if [ -z "$commit_message" ]; then
    echo -e "${YELLOW}Enter commit message:${NC}"
    read commit_message
    
    # If still empty, use default
    if [ -z "$commit_message" ]; then
        commit_message="Update: $(date '+%Y-%m-%d %H:%M:%S')"
    fi
fi

# Commit changes
print_status "Committing changes..."
git commit -m "$commit_message"

# Pull latest changes
print_status "Pulling latest changes..."
git pull origin main

# Push changes
print_status "Pushing changes..."
git push origin main

echo -e "${GREEN}Done! All changes have been pushed to the repository.${NC}" 