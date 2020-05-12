# GRIB2

This repository manages the GRIB2 structured content for the WMO Manual on Codes.

## The Change Work Flow

1. A proposer creates an issue to discuss a piece of work within a team.
1. The proposer makes a Pull Request detailing the changes to the CSV format files in the main repository directory:
    * include the text `closes #{I}` where `{I}` is the issue number;
    * CI tests will run to validate that the change can be parsed and to highlight that the Codes Registry updates would be needed.
1. The team agree the content of the Pull Request is semantically correct.
    * Content is uploaded to the test system.
1. A registry maintainer confirms that Pull Request is syntactically valid.
1. The registry maintainer assigns the Pull Request to themselves and conducts an update to the production Codes Registry
    * Only one PR can be assigned and altering the production Codes Registry at any time.
1. The registry maintainer re-runs the CI tests to confirm all are passing.
1. If all tests pass, the Pull Request is merged.
    * CI tests will rerun to validate the merge, and to commit updated registry content in turtle (.ttl) format to the repository.
