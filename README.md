# AnaEE Interface (WIP)

AnaEE is an experimental interface for exploring and managing environmental experiment data for the AnaEE research infrastructure.

The goal of this project is to provide researchers with a clean, desktop-friendly UI to:
- Load and inspect experimental datasets
- Browse metadata and time series
- Prepare data for further analysis in external tools

> ⚠️ This project is a work in progress. The current version focuses on the basic application structure and core UI flow.

## Tech stack

- **React** – Component-based UI
- **Electron** – Desktop wrapper around the React app
- **JavaScript/TypeScript** – Application logic
- **HTML/CSS/SCSS** – Layout and styling
- (Optional: add anything else you actually use: charts library, state management, etc.)

## Getting started

```bash
# Install dependencies
npm install

# Start the React dev server
npm start

# In another terminal, start the Electron shell (if you have a script for that)
npm run electron
