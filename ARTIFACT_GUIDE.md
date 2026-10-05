# Artifact labels

File headers use four labels:

- `original-sanitized`: an excerpt of a recorded configuration with identifying or sensitive values removed or replaced.
- `reconstructed-from-project-records`: a technical reconstruction supported by procedures, diagrams, or configuration appendices; it is not a raw device export.
- `reference-implementation`: an executable or adaptable example that follows the documented design but includes review choices not verified as the exact lab configuration.
- `synthetic-example`: invented test input or output, identified as such.

Documentation addresses use RFC 5737 ranges. Private subnet examples use RFC 1918 ranges. The public files do not contain a source-to-replacement address map. Read a file's label and notes before applying any configuration to a new lab; device release, interface names, and existing policy may require changes.
