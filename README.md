# War-in-Ukraine---in-group-out-group
Misinformation about the war in Ukraine and elicited sentiments on Twitter


Script to preprocess the json files that were outputted from the Google Fact-check Explorer API scraper. The json files are concatenated for all search terms (queries) for each language (German, Italian, Polish), duplicates are removed, files in the time frame December 2021 to March 2022 are selected, and relevant variables are extracted (review date, claim title, publisher, url). This database is then compared to the external database extracted from the local websites of certified fact-checkers, and those already present there are removed. The resulting new fact-checked stories are exported to an excel file.

.
├── build                   # Compiled files (alternatively `dist`)
├── docs                    # Documentation files (alternatively `doc`)
├── src                     # Source files (alternatively `lib` or `app`)
├── test                    # Automated tests (alternatively `spec` or `tests`)
├── tools                   # Tools and utilities
├── LICENSE
└── README.md
