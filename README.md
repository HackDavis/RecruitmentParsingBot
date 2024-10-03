# RecruitmentParsingBot
 
Bot to parse entries in a google sheet and divide them into sub-worksheets so each individual team can look only at the people who aplied to their team.

## Get credentials

You need to generate a credentials on [Google Developer Console](https://console.cloud.google.com/)

Follow the instructions from the [gspread documentation](https://docs.gspread.org/en/latest/oauth2.html#enable-api-access-for-a-project) to enable functionality of the bot.
Once you download the credentials JSON file from the Google Developer Console, share the recruitment sheet with the email in the field `client_email` of the credentials JSON. Rename this to `credentials.json` to use with the script.

## Changes needed on the Google Sheets.
 Then change the name of the worksheet in the next line to the name of the worksheet with all the entries. Make a copy of the worksheet where all the entries from Typeform are coming in, rename the copy to "Bot Parsing Copy".

## Code changes needed 

1. Modify the `expected_headers`variable with changed questions. (remember to check for whitespace)
2. Also, un-comment the entries in `teams_dict` based on which teams are being recruited for.
3. Set the name of the file in the `gsheet = gc.open("Sheet File Name")` to the same as the name of the Google Sheets file.
4. Change the `category_column` variable to the 