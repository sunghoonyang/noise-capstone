# Overview

At a client meeting on 2019-07-19, DEP expressed interest in obtaining Department of Transportation (DOT) permits, which allow noise from certain road-related activity.

The current process for obtaining this information is as follows:
1. Go to https://nycstreets.net/public/permit/search
2. Change the parameters for the search in the right sidebar.
3. Search and select a green polygon overlaid on a street block.
4. Click Details to see information about the permit (example: https://nycstreets.net/Public/Permit/Details/M012019193A39)
5. Click Permits PDF to see the permit PDF (https://nycstreets.net/Public/Document/ViewPermitPDF/?id=M012019193A39)
6. Manually parse the PDF for the information desired (including the dates for work)

This tool is not actually a scraper; it's a short instruction on how to obtain this data for a CSV report

# How to Use
The DOT has an API (https://nycstreets.net/Public/Permit/SearchPermits/) that returns a JSON object with permit information for the query parameters provided.

There is an alternative endpoint (https://nycstreets.net/Public/Permit/SearchPermits/) that returns a CSV-formatted text with the permit information.

Searches on the website are limited to the current search radius. The API request query parameters can be manipulated to return all permits for a given period of time.

You can modify the permit issue date range with the *PermitIssueDateFrom* and *PermitIssueDateTo* parameters.

Parameters are HTML encoded with the date format `MM DD YYYY`. For example, to search from July 1, 2019, use: `07%2F01%2F2019`.

You can hit the resulting endpoint in your web browser. Running three weeks of data took about 9 minutes in my testing. The resulting can be saved to CSV.

Sample URL for two days in July (7/17-7/19):
https://nycstreets.net/Public/Permit/SearchPermitsCSV/?PermitIssueDateFrom=07%2F17%2F2019&PermitIssueDateTo=07%2F19%2F2019&page=1&rows=100&sidx=PermitIssueDateFrom&sord=desc&LocationSearchType=5
