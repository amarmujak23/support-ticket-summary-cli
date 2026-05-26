# Ticket Summary App

## What the app does
This app reads a sample ticket dataset from `fake_tickets.json` and prints a support ticket summary to the console. It counts total tickets, open tickets, snoozed tickets, and priority-set tickets, and it also lists the assignees for all open tickets.

## Why it uses fake data
The app uses fake data so the project is easy to test and safe to share without exposing real customer information. The sample dataset demonstrates expected ticket fields like `status`, `assignee`, `priority`, and `hospice`, while keeping the data lightweight and controlled.

## Features
- Count total tickets in the dataset
- Count open and snoozed tickets
- Count priority-set tickets
- Display open ticket assignees alongside ticket IDs
- Use ANSI color codes for readable console output

## How to run
1. Open a terminal and navigate to the project root:
   ```bash
   cd "c:\Users\Amar Mujak\OneDrive\Desktop\Code"
   ```
2. Run the script:
   ```bash
   python "ticket summary\ticket_summary.py"
   ```

## Future improvements
- Add command-line arguments to filter by ticket status, hospice, or assignee
- Convert the script into a reusable module with functions that return values instead of printing directly
- Add validation for missing or malformed ticket fields
- Support CSV input or database-backed ticket data
- Add unit tests for the counting and filtering functions
- Add SLA compliance analytics if the data source provides reliable first-response, resolution, and SLA policy fields
- Add agent performance metrics once a workflow data source includes clean resolution and ticket assignment metadata
