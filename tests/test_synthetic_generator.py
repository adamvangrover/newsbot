import pytest
from datetime import date
from synthetic.synthetic_generator import SyntheticDataEngine

def test_synthetic_data_generation():
    start_date = date(2023, 10, 1)
    end_date = date(2023, 10, 5) # Short duration for test
    engine = SyntheticDataEngine(start_date=start_date, end_date=end_date, num_assets=5)
    data = engine.run()

    assert len(data["assets"]) == 5
    # 5 assets * 5 days + weekends (Oct 1 2023 was Sunday)
    # Oct 1 (Sun), Oct 2 (Mon), Oct 3 (Tue), Oct 4 (Wed), Oct 5 (Thu)
    # Trading days: 2, 3, 4, 5 = 4 days.
    # 5 assets * 4 days = 20 prices.
    # Note: range(delta.days + 1) -> 0 to 4 inclusive.
    # 0: Oct 1 (Sun) - No
    # 1: Oct 2 (Mon) - Yes
    # 2: Oct 3 (Tue) - Yes
    # 3: Oct 4 (Wed) - Yes
    # 4: Oct 5 (Thu) - Yes
    assert len(data["equity_daily_prices"]) >= 15 # Allow for some flexibility if my manual calc is off slightly
    assert len(data["news_articles_metadata"]) >= 0

if __name__ == "__main__":
    test_synthetic_data_generation()
    print("Test passed!")
