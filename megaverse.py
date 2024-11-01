import os
import requests
import time
from dotenv import load_dotenv
from typing import Dict

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
                if method == "POST":
                    response = requests.post(url, json=json_data)
                elif method == "DELETE":
                    response = requests.delete(url, json=json_data)
                else:
                    raise ValueError("Unsupported HTTP method.")

                response.raise_for_status()
                return response
            except requests.exceptions.HTTPError as e:
                if response.status_code == 429:  # Rate limit error
                    print(f"Rate limit hit. Retrying in {backoff_time} seconds...")
                    time.sleep(backoff_time)
                    backoff_time *= 2  # Exponential backoff
                    retries += 1
                else:
                    print(f"Request failed: {e}")
                    break  # Exit on non-rate-limiting errors
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

    def delete_polyanet(self, row, col, max_retries=5):
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
        try:
            response = requests.get(f"{self.BASE_URL}/map/{self.candidate_id}/goal")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Failed to fetch goal map: {e}")
            return None


class MapBuilder:
    ENTITY_MAPPING: Dict[str, str] = {
        "POLYANET": "polyanet",
        "RIGHT_COMETH": "cometh",
        "UP_COMETH": "cometh",
        "LEFT_COMETH": "cometh",
        "DOWN_COMETH": "cometh",
        "BLUE_SOLOON": "soloon",
        "RED_SOLOON": "soloon",
        "PURPLE_SOLOON": "soloon",
        "WHITE_SOLOON": "soloon",
        "SPACE": "space"
    }

    def __init__(self, api_client):
        self.api_client = api_client

    def build_map(self, row_to_build: int = None):
        """Builds the map by placing entities based on the goal map. 
        Builds the entire map by default, or a specific row if specified."""
        goal_data = self.api_client.get_goal_map()  # Get goal data from API
        if not goal_data or 'goal' not in goal_data:
            print("Error: Goal map is empty or failed to retrieve.")
            return

        goal_map = goal_data['goal']  # Access the 2D array under the 'goal' key

        if row_to_build is not None:
            # Ensure the specified row is within bounds
            if 0 <= row_to_build < len(goal_map):
                self.build_row(goal_map, row_to_build)
            else:
                print(f"Error: Row {row_to_build} is out of bounds.")
        else:
            # Build the entire map if no specific row is provided
            for row_index, row in enumerate(goal_map):
                self.build_row(goal_map, row_index)

    def build_row(self, goal_map, row_index):
        """Builds a specific row in the map."""
        row = goal_map[row_index]
        for col_index, entity in enumerate(row):
            self.place_entity(entity, row_index, col_index)

    def reset_map(self, row_to_reset: int = None):
        """Resets the map by removing entities from the specified row or all rows if none is specified."""
        goal_data = self.api_client.get_goal_map()
        if not goal_data or 'goal' not in goal_data:
            print("Error: Goal map is empty or failed to retrieve.")
            return

        goal_map = goal_data['goal']

        # If a specific row is given, only reset that row
        if row_to_reset is not None:
            if 0 <= row_to_reset < len(goal_map):
                for col_index, entity in enumerate(goal_map[row_to_reset]):
                    self.remove_entity(entity, row_to_reset, col_index)
            else:
                print(f"Error: Row {row_to_reset} is out of range.")
        else:
            # Reset all rows if no specific row is provided
            for row_index, row in enumerate(goal_map):
                for col_index, entity in enumerate(row):
                    self.remove_entity(entity, row_index, col_index)


    def place_entity(self, entity: str, row: int, column: int):
        if entity == "SPACE":
            return  # Skip SPACE, as it's already blank

        entity_type = self.ENTITY_MAPPING.get(entity)
        if entity_type == "polyanet":
            self.api_client.set_polyanet(row, column)
        elif entity_type == "soloon":
            color = entity.split("_")[0].lower()  # Extracts color from entity name, e.g., "BLUE_SOLOON"
            self.api_client.set_soloon(row, column, color)
        elif entity_type == "cometh":
            direction = entity.split("_")[0].lower()  # Extracts direction from entity name, e.g., "RIGHT_COMETH"
            self.api_client.set_cometh(row, column, direction)
        else:
            print(f"Unknown entity type: {entity}")

    def remove_entity(self, entity: str, row: int, column: int):
        """Removes the given entity from the map."""
        if entity == "SPACE":
            return  # Skip SPACE, as there's nothing to remove

        entity_type = self.ENTITY_MAPPING.get(entity)
        if entity_type == "polyanet":
            self.api_client.delete_polyanet(row, column)
        elif entity_type == "soloon":
            self.api_client.delete_soloon(row, column)
        elif entity_type == "cometh":
            self.api_client.delete_cometh(row, column)
        else:
            print(f"Unknown entity type: {entity}")

def main():
    api_client = MegaverseAPI()
    map_builder = MapBuilder(api_client)
    
    map_builder.build_map()

if __name__ == "__main__":
    main()
