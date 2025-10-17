# Placenta Database Frontend

## Overview
This is the front-end design and implementation for the NIH CGRH Placenta Database Initiative. It's a static website that provides a user interface for searching and viewing placenta research data.

## Project Structure
- `index.html` - Main homepage with database search interface
- `about.html` - About page
- `contact.html` - Contact page
- `style.css` - Styling for all pages
- `images/` - Contains NIH logo and other assets
- `server.py` - Python HTTP server for serving the static files

## Technology Stack
- HTML5
- CSS3
- Python 3.11 (for local server)
- Google Fonts (Open Sans)

## Setup in Replit
The project is configured to run on port 5000 using Python's built-in HTTP server. The server includes cache-control headers to ensure changes are visible immediately during development.

## Running the Project
The workflow "Server" is configured to automatically run `python server.py` on port 5000. The website will be accessible through the Replit webview.

## Features
- Responsive navigation menu
- Database search form with multiple filters:
  - Organism selection
  - Data type selection
  - Extracted molecule checkboxes
  - Superseries radio buttons
- Updates section
- Database trends section
- NIH branding and footer

## Recent Changes
- **2025-10-17**: Initial setup in Replit environment
  - Added Python server with cache control headers
  - Configured workflow for port 5000
  - Added .gitignore for Python files
  - Created project documentation
  
- **2025-10-17**: Added Flask API backend with SQLite database
  - Created placenta study database model with test data (10 studies)
  - Implemented REST API endpoints:
    - `/api/studies` - Search studies with filters (organism, data_type, extracted_molecule, superseries)
    - `/api/stats` - Get database statistics
  - Added JavaScript integration for frontend search form
  - Implemented database trends visualization
  - Fixed security vulnerability: blocked access to .db and .py files
  - Fixed multi-molecule search to use OR logic correctly
