#!/usr/bin/env python3
from datetime import datetime

def generate_tracking_id():
    print("🧪 XooHooX Batch ID Generator\n")

    grower_id = input("Enter Grower ID (e.g. 01): ").strip()
    fruit_id = input("Enter Fruit ID (e.g. F01): ").strip().upper()
    varietal_id = input("Enter Varietal ID (e.g. 01): ").strip()
    batch_no = input("Enter Batch Number (e.g. 01): ").strip()
    process_stage = input("Enter Process Stage Code (e.g. J01): ").strip().upper()
    date_input = input("Enter Process Date (YYYY-MM-DD) [Leave blank for today]: ").strip()

    # Default to today if no date is provided
    if not date_input:
        process_date = datetime.today()
    else:
        try:
            process_date = datetime.strptime(date_input, "%Y-%m-%d")
        except ValueError:
            print("⚠️ Invalid date format. Use YYYY-MM-DD.")
            return

    date_str = process_date.strftime("%y%m%d")
    tracking_id = f"{grower_id}.{fruit_id}.{varietal_id}.{batch_no}.{process_stage}.{date_str}"

    print("\n✅ Tracking ID Generated:")
    print(tracking_id)

if __name__ == "__main__":
    generate_tracking_id()
