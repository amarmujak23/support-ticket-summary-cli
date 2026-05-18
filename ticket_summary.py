# Version 1.0.0

import json

with open('ticket summary/fake_tickets.json', 'r') as file:
    data = json.load(file)


def total_ticket_count():
    """Return the total number of tickets."""
    return len(data)


def open_ticket_count():
    """Return the number of open tickets."""
    open_tickets = 0
    for ticket in data:
        if ticket['status'] == 'open':
            open_tickets += 1
    return open_tickets


def closed_ticket_count():
    """Return the number of closed tickets."""
    closed_tickets = 0
    for ticket in data:
        if ticket['status'] == 'closed':
            closed_tickets += 1
    return closed_tickets


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


def high_priority_tickets():
    """Return the number of high-priority tickets."""
    high_priority = 0
    for ticket in data:
        if ticket['priority'] == 'high':
            high_priority += 1
    return high_priority


def escalated_tickets():
    """Return the number of escalated tickets."""
    escalated = 0
    for ticket in data:
        if ticket['escalated'] is True:
            escalated += 1
    return escalated


print("Support Ticket Summary")
print("======================")

print(f"Total number of tickets: \033[32m{total_ticket_count()}\033[0m")
print()
print(f"Number of \033[32mOpen\033[0m tickets: \033[32m{open_ticket_count()}\033[0m")
print(f"Number of \033[31mClosed\033[0m tickets: \033[31m{closed_ticket_count()}\033[0m")
print(f"Number of \033[33mSnoozed / On Hold\033[0m tickets: \033[33m{snoozed_ticket_count()}\033[0m")
print()

print("Open Tickets and their Assignees:")
print("===============================")
for assignee, ticket_id in get_open_ticket_assignees():
    print(f"Assignee: \033[32m{assignee}\033[0m Ticket ID: {ticket_id}")
print()
print(f"Number of \033[31mHigh Priority\033[0m tickets: \033[31m{high_priority_tickets()}\033[0m")
print(f"Number of \033[31mEscalated\033[0m tickets: \033[31m{escalated_tickets()}\033[0m")