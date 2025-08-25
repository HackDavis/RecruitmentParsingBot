import gspread  # Google Sheets API

# Authenticate using the service account
gc = gspread.service_account()

# Open the specific Google Spreadsheet
gsheet = gc.open("2026 Director Applications Typeform")
test_sheet = gsheet.worksheet("Bot Parsing Copy")

# Get all records from the sheet
expected_headers = [
    "First Name",
    "Last name",
    "UC Davis Email Address",
    "Major",
    "Graduation Date?",
    "Why do you want to join HackDavis?",
    "Have you attended HackDavis before?",
    "What is a hackathon?",
    "What are your time commitments (current and potential new ones) for the 2025-2026 school year?",
    "Tell us something special about *YOU*!",
    "What team(s) are you interested in joining? ",
    "Why are you interested in joining the team(s) you selected?"
    "[TECHNICAL] Describe in detail a project you have worked on. If it was a team project, specify your contribution."
    "[TECHNICAL] Describe your experience with React.js and/or Next.js. What features of these tools do you like or not like?",
    "[OPERATIONS] Suppose a food vendor reaches out 2 weeks before the HackDavis hackathon, wanting to offer their services. This new vendor has a cheaper per person cost than at least one of the already selected and agreed upon vendors. What do you do?"
    "[MARKETING] What are some new and innovative ways for HD to market and build presence amongst the community?",
    "[SPONSORSHIP] How would you go about reaching out to potential sponsorships for HackDavis?",
    "[SPONSORSHIP] How would you pitch HackDavis to a potential sponsor?",
    "[FINANCE] What is your experience with budgeting, expense tracking, or filing taxes?",
    "[FINANCE] Do you have any experience in grant writing? How would you go about finding grants to apply to?",
    "[EXTERNAL] How would you go about planning a workshop?",
    "[EXTERNAL] HackDavis invites industry professionals to judge the hackathon. How would you go about vetting judges in a timely manner?",
    "[DESIGN] What realm of design are you interested in?",
    "[DESIGN] Why are you interested in the realm(s) of design you chose in the previous question?",
    "[DESIGN] Please provide a link to your portfolio.",
    "Please provide a copy of your resume",
    "LinkedIn?",
    "GitHub?",
    "Personal website?"
    "utm_source",
    "Submitted At",
    "Token",
]

category_column = "What team(s) are you interested in joining? "

records = test_sheet.get_all_records()

# Process records to filter based on top 3 teams interested in joining
teams_dict = {
    "Technical": [],
    "Operations": [],
    "Sponsorship": [],
    "Design": [],
    "Marketing": [],
    "Finance": [],
    "External": [],
}

for record in records:
    teams = record[category_column].split(", ")
    top_teams = teams[:3]
    for team in top_teams:
        if team in teams_dict:
            teams_dict[team].append(record)
        elif team == "Design (Graphic Designer roles only)":
            teams_dict["Design"].append(record)
            

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
print(f"Found {len(records)} records")
print(records[0] if records else "No data found.")
