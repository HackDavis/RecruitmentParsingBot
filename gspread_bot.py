import gspread  # Google Sheets API

# Authenticate using the service account
gc = gspread.service_account(filename="credentials.json")

# Open the specific Google Spreadsheet
gsheet = gc.open("FQ2024 - Director Recruitment 2025")
test_sheet = gsheet.worksheet("Bot Parsing Copy")

# Get all records from the sheet
expected_headers = [
    "First Name",
    "Last name",
    "UC Davis Email Address",
    "Major",
    "Graduation Date?",
    "Have you attended HackDavis?",
    "Why do you want to join the HackDavis team? (150 words max)",
    "What does \"social good\" mean to you? (150 words max)",
    "What is a hackathon? (150 words max)",
    "What are your time commitments for the 2024-2025 school year?",
    "Tell us something special about *YOU*!",
    "What team(s) are you interested in joining? ",
    "What elevant experience & skills do you bring to the teams you've selected that make you a strong candidate? (150 words max)",
    "Please provide a copy of your resume",
    "LinkedIn?",
    "GitHub?",
    "Personal Website/Portfolio?",
    "utm_source",
    "Submitted At",
    "Token",
]

category_column = "What team(s) are you interested in joining? "

records = test_sheet.get_all_records(expected_headers=expected_headers)

# Process records to filter based on top 3 teams interested in joining
teams_dict = {
    # "Technical": [],
    "Operations": [],
    "Sponsorship": [],
    "Design": [],
    # "Marketing": [],
    # "Finance": [],
    # "External": [],
}

for record in records:
    teams = record[category_column].split(", ")
    top_teams = teams[:3]
    for team in top_teams:
        if team in teams_dict:
            teams_dict[team].append(record)

# Create or update sheets for each team
for team, records in teams_dict.items():
    try:
        # Try to access the sheet, if it exists
        team_sheet = gsheet.worksheet(team)
        gsheet.del_worksheet(team_sheet)  # Delete if exists to refresh data
    except gspread.WorksheetNotFound:
        # If not found, no action needed
        pass

    # Create a new sheet for the team
    team_sheet = gsheet.add_worksheet(title=team, rows="100", cols="25")

    # Update the new sheet with records
    if records:
        team_sheet.update(
            [list(records[0].keys())] + [list(record.values()) for record in records]
        )

print("Sheets updated with filtered team records.")
