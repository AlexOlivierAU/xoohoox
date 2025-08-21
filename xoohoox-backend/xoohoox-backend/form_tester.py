# form_tester.py
import yaml
from pathlib import Path

form_path = Path("forms/form_juicing.yaml")  # adjust if needed
data = yaml.safe_load(form_path.read_text())

print(f"\n🧪 Testing Form: {data['form_name']}\n")

form_data = {}
for field in data["fields"]:
    prompt = f"{field['label']} ({field['type']})"
    if field.get("required"):
        prompt += " [REQUIRED]"
    user_input = input(f"{prompt}: ")
    form_data[field["id"]] = user_input

print("\n✅ Form input collected:")
print(form_data)