# Version 4.0 - 2026-06-02
# Support Ticket Snapshot CLI - Active Ticket Reporting
# Fetches tickets from Flask mock API at http://127.0.0.1:5000/tickets

import json
import os
import requests
from datetime import datetime, timezone
from collections import Counter, defaultdict
import time

API_URL = "http://127.0.0.1:5000/tickets"

def get_tickets_from_api():
    """Fetch tickets from the Flask mock API."""
    try:
        response = requests.get(API_URL, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to Flask server at http://127.0.0.1:5000")
        print("Please run 'python server.py' first.")
        exit(1)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching tickets: {e}")
        exit(1)

data = get_tickets_from_api()

def clear():
    # 'nt' is for Windows, others are usually 'posix' (Linux, macOS)
    os.system('cls' if os.name == 'nt' else 'clear')

# This tool reads ticket data from the local Flask mock API to generate an active workload summary.

#Returns the total number of open and snoozed tickets

def total_ticket_count():
    """Return the total number of tickets."""
    open_snoozed_count = 0
    for ticket in data:
        if ticket['status'] == "open" or ticket['status'] == "snoozed" and ticket['status'] != "closed":
            open_snoozed_count += 1
    return open_snoozed_count

def open_ticket_count():
    """Return the number of open tickets."""
    open_tickets = 0
    for ticket in data:
        if ticket['status'] == 'open':
            open_tickets += 1
    return open_tickets


def snoozed_ticket_count():
    """Return the number of snoozed tickets."""
    snoozed_tickets = 0
    for ticket in data:
        if ticket['status'] == 'snoozed':
            snoozed_tickets += 1
    return snoozed_tickets


def get_open_ticket_assignees():
    """Return a list of (assignee, ticket_id) tuples for open tickets."""
    open_list = []
    for ticket in data:
        if ticket['status'] == 'open':
            open_list.append((ticket['assignee'], ticket['ticket_id']))
    return open_list


# ============================================================================
# REPORTING & ANALYTICS FUNCTIONS
# ============================================================================

def hospice_analytics():
    """Return ticket analytics grouped by hospice facility."""
    hospices = defaultdict(lambda: {'total': 0, 'open': 0, 'snoozed': 0, 'priority_set': 0})
    
    for ticket in data:
        status = ticket.get('status', '').lower()
        if status not in ('open', 'snoozed'):
            continue

        hospice = ticket.get('hospice', 'Unknown')
        hospices[hospice]['total'] += 1
        
        if status == 'open':
            hospices[hospice]['open'] += 1
        elif status == 'snoozed':
            hospices[hospice]['snoozed'] += 1

        if ticket.get('priority') is True:
            hospices[hospice]['priority_set'] += 1
    
    return dict(hospices)


def parse_ticket_timestamp(timestamp):
    if not timestamp:
        return None

    try:
        return datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
    except ValueError:
        return None


def format_report_datetime(dt):
    if not dt:
        return "N/A"

    report_ts = dt.astimezone(timezone.utc)
    formatted = report_ts.strftime("%Y-%m-%d %I:%M %p")
    return formatted.replace(" 0", " ")


def ticket_updated_today(ticket):
    """Return True when ticket.updated_at is today."""
    updated_at = ticket.get('updated_at')
    if not updated_at:
        return False

    try:
        updated = datetime.fromisoformat(updated_at.replace('Z', '+00:00'))
    except ValueError:
        return False

    return updated.date() == datetime.now().date()


def format_priority(priority):
    """Return a user-friendly Priority label."""
    return "Yes" if priority is True else "No"


def get_last_updated_ticket():
    latest_ticket = None
    latest_timestamp = None

    for ticket in data:
        updated = parse_ticket_timestamp(ticket.get('updated_at'))
        if not updated:
            updated = parse_ticket_timestamp(ticket.get('resolved_at'))
        if not updated:
            updated = parse_ticket_timestamp(ticket.get('first_response_at'))
        if not updated:
            updated = parse_ticket_timestamp(ticket.get('created_at'))

        if updated is None:
            continue

        if latest_timestamp is None or updated > latest_timestamp:
            latest_timestamp = updated
            latest_ticket = ticket

    return latest_ticket, latest_timestamp


def workload_by_assignee():
    workloads = defaultdict(lambda: {'open': 0, 'snoozed': 0, 'priority': 0})

    for ticket in data:
        status = ticket.get('status', '').lower()
        if status not in ('open', 'snoozed'):
            continue

        assignee = ticket.get('assignee', 'Unassigned')
        if assignee.lower() == 'unassigned':
            continue

        if status == 'open':
            workloads[assignee]['open'] += 1
        elif status == 'snoozed':
            workloads[assignee]['snoozed'] += 1

        if ticket.get('priority') is True:
            workloads[assignee]['priority'] += 1

    return dict(sorted(workloads.items()))


def most_common_active_categories():
    counts = Counter()
    for ticket in data:
        if ticket.get('status', '').lower() in ('open', 'snoozed'):
            category = ticket.get('category', 'Unknown').title()
            counts[category] += 1

    return counts.most_common()


def hospice_snapshot():
    facilities = defaultdict(lambda: {'open': 0, 'snoozed': 0, 'priority_set': 0})

    for ticket in data:
        status = ticket.get('status', '').lower()
        if status not in ('open', 'snoozed'):
            continue

        hospice = ticket.get('hospice', 'Unknown')
        if status == 'open':
            facilities[hospice]['open'] += 1
        elif status == 'snoozed':
            facilities[hospice]['snoozed'] += 1

        if ticket.get('priority') is True:
            facilities[hospice]['priority_set'] += 1

    return dict(sorted(facilities.items()))


def tickets_needing_attention():
    attention = []

    for ticket in data:
        status = ticket.get('status', '').lower()
        if status == 'open' and ticket.get('priority') is True:
            attention.append((ticket, 'Priority set'))
        elif status == 'snoozed':
            attention.append((ticket, 'Snoozed / On Hold'))

    return attention

# Markdown summary export function
def export_markdown_summary(filename="ticket_snapshot.md"):
    report_time = datetime.now(timezone.utc)
    last_updated_ticket, last_updated_timestamp = get_last_updated_ticket()
    assignee_workload = workload_by_assignee()
    categories = most_common_active_categories()
    hospice_data = hospice_snapshot()
    attention_rows = tickets_needing_attention()

    active_open = sum(1 for ticket in data if ticket.get('status', '').lower() == 'open')
    active_snoozed = sum(1 for ticket in data if ticket.get('status', '').lower() == 'snoozed')
    active_priority = sum(
        1
        for ticket in data
        if ticket.get('status', '').lower() in ('open', 'snoozed') and ticket.get('priority') is True
    )
    last_updated_line = 'N/A'
    if last_updated_ticket and last_updated_timestamp:
        last_updated_line = f"{last_updated_ticket['ticket_id']} at {format_report_datetime(last_updated_timestamp)}"

    lines = []
    lines.append('# Support Ticket Snapshot')
    lines.append('')
    lines.append(f"Generated: {format_report_datetime(report_time)}")
    lines.append('')
    lines.append('## Active Summary')
    lines.append('')
    lines.append(f"- Open tickets: {active_open}")
    lines.append(f"- Snoozed / On Hold tickets: {active_snoozed}")
    lines.append(f"- Priority set: {active_priority}")
    lines.append(f"- Last updated ticket: {last_updated_line}")
    lines.append('')
    lines.append('## Workload by Assignee')
    lines.append('')
    lines.append('| Assignee | Open | Snoozed | Priority Set |')
    lines.append('|---|---:|---:|---:|')
    for assignee, counts in assignee_workload.items():
        lines.append(f"| {assignee} | {counts['open']} | {counts['snoozed']} | {counts['priority']} |")
    if not assignee_workload:
        lines.append('| None | 0 | 0 | 0 |')
    lines.append('')
    lines.append('## Most Common Active Issue Categories')
    lines.append('')
    lines.append('| Category | Count |')
    lines.append('|---|---:|')
    for category, count in categories:
        lines.append(f"| {category} | {count} |")
    if not categories:
        lines.append('| None | 0 |')
    lines.append('')
    lines.append('## Hospice-Level Snapshot')
    lines.append('')
    lines.append('| Hospice | Open | Snoozed | Priority Set |')
    lines.append('|---|---:|---:|---:|')
    for hospice, counts in hospice_data.items():
        lines.append(f"| {hospice} | {counts['open']} | {counts['snoozed']} | {counts['priority_set']} |")
    if not hospice_data:
        lines.append('| None | 0 | 0 | 0 |')
    lines.append('')
    lines.append('## Tickets Needing Attention')
    lines.append('')
    if attention_rows:
        for ticket, reason in attention_rows:
            last_updated = (
                parse_ticket_timestamp(ticket.get('updated_at'))
                or parse_ticket_timestamp(ticket.get('resolved_at'))
                or parse_ticket_timestamp(ticket.get('first_response_at'))
                or parse_ticket_timestamp(ticket.get('created_at'))
            )
            age_text = ''
            if last_updated:
                age_days = (datetime.now(timezone.utc) - last_updated).days
                age_text = f" — Last updated {age_days} days ago"
            lines.append(
                f"- {ticket['ticket_id']} — {ticket['status'].capitalize()} — {reason} — Assigned to {ticket['assignee']}{age_text}"
            )
    else:
        lines.append('- None')
    lines.append('')
    lines.append('## Notes')
    lines.append('')
    lines.append('This report uses fake ticket data for portfolio/demo purposes.')
    lines.append('')
    lines.append('')

    with open(filename, 'w', encoding='utf-8') as output_file:
        output_file.write('\n'.join(lines))

    return filename

# ============================================================================
# SUPPORT TICKET SUMMARY OUTPUT
# ============================================================================

print("\n" + "="*50)
print("SUPPORT TICKET SUMMARY")
print("="*50)

todays_date = datetime.now().strftime("%Y-%m-%d")
print(f"Date: {todays_date}")


print()

print(f"Total open and snoozed tickets: \033[32m{total_ticket_count()}\033[0m")
print("-------------------------")
print()
print(f"Number of \033[32mOpen\033[0m tickets: \033[32m{open_ticket_count()}\033[0m")
print(f"Number of \033[33mSnoozed / On Hold\033[0m tickets: \033[33m{snoozed_ticket_count()}\033[0m")
# Print number of unassigned tickets
print()

print("Open Tickets and their Assignees:")
print("===============================")
for assignee, ticket_id in get_open_ticket_assignees():
    print(f"Assignee: \033[32m{assignee}\033[0m Ticket ID: {ticket_id}")  #Add hospice name
print()



# ============================================================================
# FUTURE ANALYTICS
# ============================================================================
# SLA and agent performance analytics are intentionally removed from the main app.
# These capabilities can be re-added later once the data source provides clean
# first-response, resolution, and workflow metadata.

# Hospice Analytics
print(f"\n\033[36mHospice-Level Snapshot:\033[0m")
hospice_data = hospice_analytics()
for hospice, stats in sorted(hospice_data.items()):
    print(f"  {hospice}:")
    print(f"    - Total Tickets: {stats['total']}")
    print(f"    - Open: {stats['open']}")
    print(f"    - Snoozed: {stats['snoozed']}")
    print(f"    - Priority Set: \033[31m{stats['priority_set']}\033[0m")


while True:
    print("\nMenu:")
    print("1. Show certain assignee tickets")
    print("2. Show only open tickets")
    print("3. Show only priority-set tickets")
    print("4. Show only snoozed tickets for assignees")
    print("5. Show open or snoozed tickets updated today")
    print("6. Show tickets older than 7 days")
    print("7. Export markdown summary")
    print("8. Exit")

    print()
    try:
        user_input = int(input("Input (1-8): "))
    except ValueError:
        clear()
        time.sleep(1)
        print("Invalid input. Please enter a number between 1 and 8.")
        continue

    if user_input not in range(1, 9):
        clear()
        time.sleep(1)
        print("Invalid input. Please enter a number between 1 and 8.")
        continue

    assignees = set()
    for ticket in data:
        if ticket["assignee"] and ticket["assignee"].lower() != "unassigned":
            assignees.add(ticket["assignee"])


    #Show certain assignee tickets
    
    if user_input == 1:
        while True:
            for i, name in enumerate(sorted(assignees), start=1):
                print(f"{i}. {name}")

            name_input = input("Type user's name: ")
            if name_input.lower() not in [assignee.lower() for assignee in assignees]:
                clear()
                print("Assignee not found.")
                continue

            for ticket in data:
                if ticket["assignee"] and ticket["assignee"].lower() == name_input.lower():
                    if ticket["status"].lower() in ("open", "snoozed"):
                            print(
                                f"Ticket ID: {ticket['ticket_id']} - Status: {ticket['status']} - Priority: {format_priority(ticket['priority'])}"
                            )
            find_other = input("Find other assignees? (y/n): ").strip().lower()
            if find_other != 'y':
                clear()
                break  

    #Show only open tickets
    if user_input == 2:
        clear()
        for ticket in data:
            if ticket["status"].lower() == "open":
                print(
                    f"Ticket ID: {ticket['ticket_id']} - Assignee: {ticket['assignee']} - Priority set: {format_priority(ticket['priority'])}"
                )
        print("There is a total of " + str(open_ticket_count()) + " open tickets.")

    #Show only priority-set tickets
    if user_input == 3:
        clear()
        for ticket in data:
            if ticket.get("priority") is True and ticket.get("status", "").lower() in ("open", "snoozed"):
                print(
                    f"Ticket ID: {ticket['ticket_id']} - Assignee: {ticket['assignee']} - Status: {ticket['status']} - Priority set: {format_priority(ticket['priority'])} - {ticket['hospice']}"
                )

    #Show only snoozed tickets for assignees
    if user_input == 4:
        while True:
            for i, name in enumerate(sorted(assignees), start=1):
                print(f"{i}. {name}")
            name_input = input("Type user's name: ")
            if name_input.lower() not in [assignee.lower() for assignee in assignees]:
                clear()
                print("Assignee not found.")
                continue
            for ticket in data:
                if ticket["assignee"] and ticket["assignee"].lower() == name_input.lower() and ticket["status"].lower() == "snoozed":
                    print(
                        f"Ticket ID: {ticket['ticket_id']} - Status: {ticket['status']} - Priority set: {format_priority(ticket['priority'])}"
                    )
            find_other = input("Find other assignees? (y/n): ").strip().lower()
            if find_other != 'y':
                break   
    
    if user_input == 5:
        while True:
            for i, name in enumerate(sorted(assignees), start=1):
                print(f"{i}. {name}")
            name_input = input("Type user's name: ")
            if name_input.lower() not in [assignee.lower() for assignee in assignees]:
                clear()
                print("Assignee not found.")
                continue

            updated_today_count = 0
            for ticket in data:
                if (
                    ticket["assignee"]
                    and ticket["assignee"].lower() == name_input.lower()
                    and ticket["status"].lower() in ("open", "snoozed")
                    and ticket_updated_today(ticket)
                ):
                    print(
                        f"Ticket ID: {ticket['ticket_id']} - Status: {ticket['status']} - Priority set: {format_priority(ticket['priority'])} - Updated At: {ticket['updated_at']}"
                    )
                    updated_today_count += 1

            if updated_today_count == 0:
                print("No open or snoozed tickets updated today for that assignee.")

            find_other = input("Find other assignees? (y/n): ").strip().lower()
            if find_other != 'y':
                break

     #Shows open tickets older than 7 days           
    if user_input == 6:
        clear()
        print()
        for ticket in data:
            if ticket["status"].lower() == "open":
                created_at = datetime.fromisoformat(ticket['created_at'].replace('Z', '+00:00'))
                if (datetime.now(timezone.utc) - created_at).days > 7:
                        print(
                            f"Ticket ID: {ticket['ticket_id']} - Assignee: {ticket['assignee']} - Status: {ticket['status']} - Created At: {ticket['created_at']} - Priority set: {format_priority(ticket['priority'])}"
                        )
    if user_input == 7:
        clear()
        filename = export_markdown_summary("ticket_snapshot.md")
        print(f"Markdown summary exported to {filename}")

    elif user_input == 8:
        print("Exiting menu.")
        break
    