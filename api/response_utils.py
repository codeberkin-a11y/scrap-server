import csv
import io
from datetime import datetime


def matches_to_csv_bytes(matches):
    """Convert list of match dicts to CSV bytes. Returns (bytes, filename)."""
    # Define headers similar to standalone scraper's export
    headers = [
        'Kod', 'Saat', 'Maç', 'MBS', 'Spor', 'match_date',
        'odd_1', 'odd_x', 'odd_2', 'under_odd', 'over_odd'
    ]

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=headers, extrasaction='ignore')
    writer.writeheader()

    for m in matches:
        row = {
            'Kod': m.get('kod') or m.get('Kod') or '',
            'Saat': m.get('saat') or m.get('Saat') or '',
            'Maç': m.get('mac') or m.get('Maç') or '',
            'MBS': m.get('mbs') or m.get('MBS') or '',
            'Spor': m.get('spor') or m.get('Spor') or '',
            'match_date': m.get('match_date') or m.get('match_date') or '',
            'odd_1': m.get('odd_1', ''),
            'odd_x': m.get('odd_x', ''),
            'odd_2': m.get('odd_2', ''),
            'under_odd': m.get('under_odd', ''),
            'over_odd': m.get('over_odd', ''),
        }
        writer.writerow(row)

    csv_text = output.getvalue()
    output.close()

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"nesine_matches_{timestamp}.csv"
    return csv_text.encode('utf-8-sig'), filename
