<img width="1445" height="530" alt="Screenshot 2026-06-03 155836" src="https://github.com/user-attachments/assets/e0cd3a4e-5b38-4bd4-a9e7-6619b920ad8d" />
# Ticket Summary App

## What the project does
This project provides a small ticket summary system with two separate components:
- `server.py` runs a local Flask mock API and serves ticket data from `fake_tickets.json`
- `ticket_summary.py` runs a CLI app that fetches tickets from the mock API and displays ticket analytics

## Fake data only
**⚠️ Important:** This project uses only fake, synthetic data stored in `fake_tickets.json`. It is designed for testing and demonstration purposes only, not for production use. All ticket information, assignees, hospice names, and metadata are randomly generated.

---

## Installation

### Requirements
Before running either component, install the required Python dependencies:

```bash
pip install -r requirements.txt
```

The project requires:
- Flask (for the mock API server)
- Requests (for the CLI to fetch from the API)

---

## How to run the mock API server

The Flask API server must be running before you start the CLI.

1. Open a terminal and navigate to the project root:
   ```bash
   cd support-ticket-summary-cli
   ```

2. Install dependencies (if not already done):
   ```bash
   pip install -r requirements.txt
   ```

3. Start the Flask API server:
   ```bash
   python server.py
   ```
   
   You should see output like:
   ```
   Starting Flask mock API on http://127.0.0.1:5000
   Endpoint: GET /tickets
   ```

### API Endpoints
- **GET `/tickets`** — Returns the full ticket dataset from `fake_tickets.json` as JSON
- **GET `/health`** — Health check endpoint; returns `{"status": "API Running"}` if the server is alive

---

## How to run the CLI

The Flask mock API server must be running before you start the CLI (see instructions above).

1. In a separate terminal, navigate to the project folder:
   ```bash
   cd support-ticket-summary-cli 
   ```

2. Run the CLI app:
   ```bash
   python ticket_summary.py
   ```

3. Follow the menu prompts to view ticket analytics, filter by assignee, priority, status, and more.

### Menu Options
1. Show certain assignee tickets
2. Show only open tickets
3. Show only priority-set tickets
4. Show only snoozed tickets for assignees
5. Show open or snoozed tickets updated today
6. Show tickets older than 7 days
7. Export markdown summary
8. Exit

---

## How to export a Markdown report

From the CLI menu, select option `7` to generate and export the current ticket summary to `ticket_snapshot.md`. This file includes:
- Active ticket counts (open, snoozed, priority-set)
- Workload breakdown by assignee
- Most common issue categories
- Hospice-level snapshot
- Tickets requiring attention

### Sample Report
See [`examples_folder/ticket_snapshot_sample.md`](examples/ticket_snapshot_sample.md) for an example of what the generated report looks like.

---

## Future enhancements
Possible approved Intercom metadata integration could be added later to enrich ticket details and support analytics using real customer support metadata.
