## `populate_district_coordinators`
The command takes the path of an `.xlsx` file.
You can use the `-b` `--bypass` flag to bypass all the checks (there are lots).
You can use the `-d` `--dry-run` flag to do a dry-run.

`settings/base.py` contains some constants to keep in mind:
`EXPECTED_WORKBOOK_SHEETS` is a set of sheet names used to validate the sheet names present on the incoming spreadsheet (after they are lower-cased and trimmed of outer and inner whitespace)
`EXPECTED_COORDINATOR_HEADERS` and `EXPECTED_DISTRICT_HEADERS` are not used for validation, but rather are used to confirm with a user (who is not using the `--bypass` flag) that the header mappings are correct before proceeding.
