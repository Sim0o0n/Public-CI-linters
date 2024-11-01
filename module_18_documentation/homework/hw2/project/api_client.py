import requests
import time
from concurrent.futures import ThreadPoolExecutor


class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()

    def request(self, use_session=True):
        client = self.session if use_session else requests
        response = client.get(f"{self.base_url}/api/books")
        return response

    def perform_requests(self, count, use_session=True, parallel=False):
        if parallel:
            with ThreadPoolExecutor() as executor:
                futures = [executor.submit(self.request, use_session) for _ in range(count)]
                return [f.result().json() for f in futures]
        else:
            return [self.request(use_session).json() for _ in range(count)]

    def measure_performance(self, count, use_session=True, parallel=False):
        start = time.time()
        self.perform_requests(count, use_session, parallel)
        return time.time() - start


if __name__ == "__main__":
    base_url = "http://localhost:5000"
    client = APIClient(base_url)
    test_cases = [(n, s, p) for n in [10, 100, 1000] for s in [False, True] for p in [False, True]]
    results = {f"{n}_{'S' if s else 'NS'}_{'T' if p else 'NT'}": client.measure_performance(n, s, p)
               for n, s, p in test_cases}
    client.session.close()

    for k, v in results.items():
        print(f"{k}: {v:.2f} seconds")
