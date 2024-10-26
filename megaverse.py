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


class Grid:
    def __init__(self, api, size=12):
        self.api = api
        self.size = size
        self.grid = [[" " for _ in range(size)] for _ in range(size)]

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
    grid.create_x_shape()

if __name__ == "__main__":
    main()
