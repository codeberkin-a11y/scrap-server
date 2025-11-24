from http.server import BaseHTTPRequestHandler
import json
from datetime import datetime, timedelta
from api.scraper_core import scrape_matches_for_date
from api.response_utils import matches_to_csv_bytes


def _parse_time_minutes(time_str):
    try:
        if ":" in time_str:
            parts = time_str.split(":")
            hour = int(parts[0])
            minute = int(parts[1].split("'")[0]) if parts[1] else 0
            return hour * 60 + minute
    except Exception:
        return None
    return None


class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length) if content_length else b"{}"
            request_data = json.loads(post_data.decode('utf-8'))

            date_str = request_data.get('date', datetime.now().strftime('%d.%m.%Y'))

            day_matches = scrape_matches_for_date('basketbol', date_str)

            dt = datetime.strptime(date_str, '%d.%m.%Y')
            next_dt = dt + timedelta(days=1)
            next_date_str = next_dt.strftime('%d.%m.%Y')
            next_matches = scrape_matches_for_date('basketbol', next_date_str)

            cutoff_minutes = 6 * 60
            filtered_next = []
            for m in next_matches:
                mins = _parse_time_minutes(m.get('saat', ''))
                if mins is None:
                    continue
                if mins <= cutoff_minutes:
                    filtered_next.append(m)

            matches = day_matches + filtered_next

            # CSV support
            fmt = request_data.get('format') if isinstance(request_data, dict) else None
            query = self.path.split('?', 1)[-1] if '?' in self.path else ''
            if 'format=csv' in query or fmt == 'csv' or 'text/csv' in self.headers.get('Accept', ''):
                csv_bytes, filename = matches_to_csv_bytes(matches)
                self.send_response(200)
                self.send_header('Content-Type', 'text/csv; charset=utf-8')
                self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(csv_bytes)
                return

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            response = {
                'matches': matches,
                'count': len(matches),
                'sport': 'basketbol',
                'date': date_str,
                'status': 'success'
            }

            self.wfile.write(json.dumps(response).encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({'status': 'OK', 'endpoint': 'basketbol'}).encode('utf-8'))
