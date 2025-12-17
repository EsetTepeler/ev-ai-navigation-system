import re

file_path = "src/services/route_planning_service.py"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace the API key
old_key = "w9xr4Dka9SWOvK8QhPy5tSTvAS9lj3Cq"
new_key = "NilqB0Tl3r0T1dMLMx277kjXS6d0IY4s"

new_content = content.replace(old_key, new_key)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print("API key updated successfully!")
