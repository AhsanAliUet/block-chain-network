# Read content from the file
with open('istanbul.log', 'r') as file:
    content = file.read()

# Split content into sections based on section headers
sections = [section.strip() for section in content.split('\n\n') if section.strip()]

# Define file names
file_names = {
    "validators": "validators.log",
    "static-nodes.json": "static-nodes.json",
    "genesis.json": "genesis.json"
}

# Iterate through sections and write them into respective files
for section in sections:
    # Split section into name and content
    name, data = section.split('\n', 1)

    # Write content to respective file
    with open(file_names[name], 'w') as file:
        file.write(data)
