import json
import pandas as pd
from datetime import date, datetime
import os
from synthetic.synthetic_generator import SyntheticDataEngine
import os

def main():
    start_date = date(2023, 10, 1)
    end_date = date(2023, 12, 31)

    # Ensure output directory exists
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    engine = SyntheticDataEngine(start_date=start_date, end_date=end_date, num_assets=50)
    data = engine.run()

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    # Export to JSONL/Parquet
    for key, items in data.items():
        if not items:
            continue

        # Convert Pydantic models to dicts
        if isinstance(items[0], dict):
             records = items
        else:
             records = [item.model_dump() for item in items]

        # Handle datetime serialization for DataFrame (pandas handles dates usually fine, but for Parquet it needs compatibility)
        # We might need to ensure dates are datetime objects or strings depending on what we want.
        # Parquet handles datetime objects well.

        df = pd.DataFrame(records)

        # Handle datetime serialization for JSON
        def json_serial(obj):
            if isinstance(obj, (date, datetime)):
                return obj.isoformat()
            raise TypeError (f"Type {type(obj)} not serializable")

        # Save as JSONL
        output_file_jsonl = os.path.join(output_dir, f"synthetic_output_{key}.jsonl")
        with open(output_file_jsonl, 'w') as f:
            for record in records:
                f.write(json.dumps(record, default=json_serial) + "\n")
        print(f"Saved {len(records)} records to {output_file_jsonl}")

        # Save as Parquet (requires pyarrow or fastparquet)
        try:
            output_file_parquet = os.path.join(output_dir, f"synthetic_output_{key}.parquet")
            df.to_parquet(output_file_parquet)
            print(f"Saved {output_file_parquet}")
        except Exception as e:
            print(f"Could not save parquet for {key}: {e}")

if __name__ == "__main__":
    main()
