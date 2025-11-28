import json
import pandas as pd
from datetime import date, datetime
from synthetic.synthetic_generator import SyntheticDataEngine

def main():
    start_date = date(2023, 10, 1)
    end_date = date(2023, 12, 31)

    engine = SyntheticDataEngine(start_date=start_date, end_date=end_date, num_assets=50)
    data = engine.run()

    # Export to JSONL/Parquet
    for key, items in data.items():
        if not items:
            continue

        # Convert Pydantic models to dicts
        if isinstance(items[0], dict):
             records = items
        else:
             records = [item.dict() for item in items]

        df = pd.DataFrame(records)

        # Handle datetime serialization for JSON
        def json_serial(obj):
            if isinstance(obj, (date, datetime)):
                return obj.isoformat()
            raise TypeError (f"Type {type(obj)} not serializable")

        # Save as JSONL
        output_file = f"synthetic_output_{key}.jsonl"
        with open(output_file, 'w') as f:
            for record in records:
                f.write(json.dumps(record, default=json_serial) + "\n")
        print(f"Saved {len(records)} records to {output_file}")

        # Save as Parquet (requires pyarrow or fastparquet)
        try:
            parquet_file = f"synthetic_output_{key}.parquet"
            df.to_parquet(parquet_file)
            print(f"Saved {parquet_file}")
        except Exception as e:
            print(f"Could not save parquet for {key}: {e}")

if __name__ == "__main__":
    main()
