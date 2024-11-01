from typing import Dict
from api import MegaverseAPI  # Import MegaverseAPI

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
        goal_data = self.api_client.get_goal_map()
        if not goal_data or 'goal' not in goal_data:
            print("Error: Goal map is empty or failed to retrieve.")
            return

        goal_map = goal_data['goal']

        if row_to_build is not None:
            if 0 <= row_to_build < len(goal_map):
                self.build_row(goal_map, row_to_build)
            else:
                print(f"Error: Row {row_to_build} is out of bounds.")
        else:
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

        if row_to_reset is not None:
            if 0 <= row_to_reset < len(goal_map):
                for col_index, entity in enumerate(goal_map[row_to_reset]):
                    self.remove_entity(entity, row_to_reset, col_index)
            else:
                print(f"Error: Row {row_to_reset} is out of range.")
        else:
            for row_index, row in enumerate(goal_map):
                for col_index, entity in enumerate(row):
                    self.remove_entity(entity, row_index, col_index)

    def place_entity(self, entity: str, row: int, column: int):
        if entity == "SPACE":
            return

        entity_type = self.ENTITY_MAPPING.get(entity)
        if entity_type:
            if entity_type == "polyanet":
                self.api_client.set_polyanet(row, column)
            elif entity_type == "soloon":
                color = entity.split("_")[0].lower()
                self.api_client.set_soloon(row, column, color)
            elif entity_type == "cometh":
                direction = entity.split("_")[0].lower()
                self.api_client.set_cometh(row, column, direction)
            else:
                print(f"Unknown entity type: {entity}")

    def remove_entity(self, entity: str, row: int, column: int):
        """Removes the given entity from the map."""
        if entity == "SPACE":
            return

        entity_type = self.ENTITY_MAPPING.get(entity)
        if entity_type:
            if entity_type == "polyanet":
                self.api_client.delete_polyanet(row, column)
            elif entity_type == "soloon":
                self.api_client.delete_soloon(row, column)
            elif entity_type == "cometh":
                self.api_client.delete_cometh(row, column)
            else:
                print(f"Unknown entity type: {entity}")
