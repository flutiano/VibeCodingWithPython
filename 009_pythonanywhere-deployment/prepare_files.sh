#!/bin/bash

# Task 009: Prepare files for PythonAnywhere deployment
# This script bundles the Flask application from Task 008 into a ZIP file.

SOURCE_DIR="../008_personal-website-enhanced"
DEST_FILE="website.zip"

echo "Bundling files from $SOURCE_DIR..."

if [ ! -d "$SOURCE_DIR" ]; then
    echo "Error: Source directory $SOURCE_DIR not found!"
    exit 1
fi

# Create a temporary directory to stage files
TEMP_DIR="temp_deploy"
mkdir -p "$TEMP_DIR"

# Copy necessary files
cp "$SOURCE_DIR/app.py" "$TEMP_DIR/"
cp "$SOURCE_DIR/requirements.txt" "$TEMP_DIR/"
cp -r "$SOURCE_DIR/static" "$TEMP_DIR/"
cp -r "$SOURCE_DIR/templates" "$TEMP_DIR/"

# Create ZIP archive
cd "$TEMP_DIR"
zip -r "../$DEST_FILE" .
cd ..

# Cleanup
rm -rf "$TEMP_DIR"

echo "Success! Archive $DEST_FILE has been created."
echo "You can now upload this file to PythonAnywhere."
