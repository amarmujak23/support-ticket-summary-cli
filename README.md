# Ticket Summary App

## What the project does
This project provides a small ticket summary system with two separate components:
- `server.py` runs a local Flask mock API and serves ticket data from `fake_tickets.json`
- `ticket_summary.py` runs a CLI app that fetches tickets from the mock API and displays ticket analytics

## Fake data only
The project uses only fake data stored in `fake_tickets.json`. It is designed for testing and demonstration, not for production use.

## How to run the mock API
1. Open a terminal and navigate to the project root:
   ```bash
   cd "c:\Users\mujak\OneDrive\Desktop\Coding\ticket summary"
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the Flask API server:
   ```bash
   python server.py
   ```

## How to run the CLI
1. In a separate terminal, navigate to the same project folder:
   ```bash
   cd "c:\Users\mujak\OneDrive\Desktop\Coding\ticket summary"
   ```
2. Run the CLI app:
   ```bash
   python ticket_summary.py
   ```

## What `/tickets` does
The `/tickets` endpoint is served by `server.py` and returns the full ticket dataset from `fake_tickets.json` as JSON. The CLI fetches this endpoint to load ticket data for reporting.

## How to export the Markdown report
From the CLI menu, choose option `7` to export the current ticket summary to `ticket_snapshot.md`.

## Future goal
Possible approved Intercom metadata integration could be added later to enrich ticket details and support analytics using real customer support metadata.
