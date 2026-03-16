import random
from pathlib import Path

from unittest.mock import patch
from src import SPOT

from services.get_max_value import get_max_value

def test_get_max_value_db():
    """
    Test: verifies that it can get a value from the database, returns -1 if not able
    """
    SPOT.OFFLINE = False
    result = get_max_value("Consignments", "consignment_id")
    assert result >= 0, "Failed to retrieve a max value through online mode"

def test_get_max_value_offline():
    """
    Test: inserts fake files into OFFLINE tickets dir, then checks if the random int is the same
    """
    offline_dir = Path(__file__).parent.parent.parent / 'utils' / 'OFFLINE_tickets'
    with patch.object(SPOT, 'OFFLINE', True):
        for i in range(3):
            fake_tick_num = random.randint(50, 100)
            fake_file = offline_dir / f"OFFLINE_{fake_tick_num}.json"
            fake_file.touch()
            result = get_max_value("Consignments", "consignment_id")
            wanted_name = '_'.join(['OFFLINE', str(fake_tick_num)])
            assert result == wanted_name, "Failed to retrieve a max value through offline mode"
            fake_file.unlink()