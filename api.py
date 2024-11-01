import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

class MegaverseAPI:
    BASE_URL = "https://challenge.crossmint.io/api"
    
    def __init__(self):
        self.candidate_id = os.getenv("CM_CANDIDATE_ID")

    def handle_request_with_retries(self, method, url, json_data=None, max_retries=5):
        """Handles API requests with retry logic for rate limiting."""
        retries = 0
        backoff_time = 1

        while retries < max_retries:
            try:
                response = requests.request(method, url, json=json_data)
                response.raise_for_status()
                return response
            except requests.exceptions.HTTPError as e:
                if response.status_code == 429:  # Rate limit error
                    print(f"Rate limit hit. Retrying in {backoff_time} seconds...")
                    time.sleep(backoff_time)
                    backoff_time *= 2
                    retries += 1
                else:
                    print(f"Request failed: {e}")
                    break
        return None

    def set_polyanet(self, row, col):
        """Sets a Polyanet on the map at the specified row and column."""
        url = f"{self.BASE_URL}/polyanets"
        json_data = {"row": row, "column": col, "candidateId": self.candidate_id}
        response = self.handle_request_with_retries("POST", url, json_data)

        if response:
            print(f"Polyanet created at ({row}, {col})")
        else:
            print(f"Failed to create Polyanet at ({row}, {col})")

    def delete_polyanet(self, row, col):
        """Deletes a Polyanet at the specified row and column."""
        url = f"{self.BASE_URL}/polyanets"
        json_data = {"row": row, "column": col, "candidateId": self.candidate_id}
        response = self.handle_request_with_retries("DELETE", url, json_data)

        if response:
            print(f"Polyanet deleted at ({row}, {col})")
        else:
            print(f"Failed to delete Polyanet at ({row}, {col})")
        
    def set_soloon(self, row: int, column: int, color: str):
        """Sets a Soloon at the specified row and column with the given color."""
        url = f"{self.BASE_URL}/soloons"
        json_data = {"row": row, "column": column, "candidateId": self.candidate_id, "color": color}
        response = self.handle_request_with_retries("POST", url, json_data)

        if response:
            print(f"Soloon created at ({row}, {column}) with color {color}")
        else:
            print(f"Failed to create Soloon at ({row}, {column}) with color {color}")

    def set_cometh(self, row: int, column: int, direction: str):
        """Sets a Cometh at the specified row and column with the given direction."""
        url = f"{self.BASE_URL}/comeths"
        json_data = {"row": row, "column": column, "candidateId": self.candidate_id, "direction": direction}
        response = self.handle_request_with_retries("POST", url, json_data)

        if response:
            print(f"Cometh created at ({row}, {column}) with direction {direction}")
        else:
            print(f"Failed to create Cometh at ({row}, {column}) with direction {direction}")

    def delete_soloon(self, row: int, column: int):
        """Deletes a Soloon at the specified row and column."""
        url = f"{self.BASE_URL}/soloons"
        json_data = {"row": row, "column": column, "candidateId": self.candidate_id}
        response = self.handle_request_with_retries("DELETE", url, json_data)

        if response:
            print(f"Soloon deleted at ({row}, {column})")
        else:
            print(f"Failed to delete Soloon at ({row}, {column})")

    def delete_cometh(self, row: int, column: int):
        """Deletes a Cometh at the specified row and column."""
        url = f"{self.BASE_URL}/comeths"
        json_data = {"row": row, "column": column, "candidateId": self.candidate_id}
        response = self.handle_request_with_retries("DELETE", url, json_data)

        if response:
            print(f"Cometh deleted at ({row}, {column})")
        else:
            print(f"Failed to delete Cometh at ({row}, {column})")

    def get_goal_map(self):
        """Fetches the goal map for the candidate."""
        try:
            response = requests.get(f"{self.BASE_URL}/map/{self.candidate_id}/goal")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Failed to fetch goal map: {e}")
            return None
