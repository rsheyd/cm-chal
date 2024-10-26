import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

class MegaverseAPI:
    BASE_URL = "https://challenge.crossmint.io/api"
    
    def __init__(self):
        self.candidate_id = os.getenv("CM_CANDIDATE_ID")
        
    def create_polyanet(self, row, col):
        try:
            response = requests.post(
                f"{self.BASE_URL}/polyanets",
                json={"row": row, "column": col, "candidateId": self.candidate_id}
            )
            response.raise_for_status()
            print(f"Polyanet created at ({row}, {col})")
        except requests.RequestException as e:
            print(f"Failed to create Polyanet at ({row}, {col}): {e}")

    def delete_polyanet(self, row, col, max_retries=5):
        retries = 0
        backoff_time = 0.5

        while retries < max_retries:
            try:
                response = requests.delete(
                    f"{self.BASE_URL}/polyanets",
                    json={"row": row, "column": col, "candidateId": self.candidate_id}
                )
                response.raise_for_status()
                print(f"Polyanet deleted at ({row}, {col})")
                return
            except requests.exceptions.HTTPError as e:
                if response.status_code == 429:
                    # Too many requests, apply exponential backoff
                    print(f"Rate limit hit. Retrying in {backoff_time} seconds...")
                    time.sleep(backoff_time)
                    backoff_time *= 2  # Double the wait time for exponential backoff
                    retries += 1
                else:
                    print(f"Failed to delete Polyanet at ({row}, {col}): {e}")
                    break  # Exit if it's a non-rate-limiting error

    def get_goal_map(self):
        try:
            response = requests.get(f"{self.BASE_URL}/map/{self.candidate_id}/goal")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Failed to fetch goal map: {e}")
            return None


class Grid:
    def __init__(self, api, size=11):
        self.api = api
        self.size = size
        self.grid = [[" " for _ in range(size)] for _ in range(size)]

    def reset_map(self):
        """Deletes only the polyanets specified in the goal map."""
        response = self.api.get_goal_map()
        goal_map = response.get("goal", [])
        for row in range(self.size):
            for col in range(self.size):
                if goal_map[row][col] == "POLYANET":
                    self.api.delete_polyanet(row, col)
        print("Map reset.")

    def create_x_shape(self):
        # Top-left to bottom-right
        for i in range(2, 9):
            self.set_polyanet(i, i)
        
        # Bottom-left to top-right
        for i in range(2, 9):
            self.set_polyanet(self.size - 1 - i, i)

    def set_polyanet(self, row, col):
        if 0 <= row < self.size and 0 <= col < self.size:
            self.api.create_polyanet(row, col)
        else:
            print(f"Position ({row}, {col}) is out of bounds.")


def main():
    api = MegaverseAPI()
    grid = Grid(api)
    grid.reset_map()

if __name__ == "__main__":
    main()
