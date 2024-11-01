from api import MegaverseAPI
from map_builder import MapBuilder

def main():
    api_client = MegaverseAPI()
    map_builder = MapBuilder(api_client)

    # Example usage
    # map_builder.build_map()  # Build the entire map
    map_builder.reset_map(2)  # Reset a specific row

if __name__ == "__main__":
    main()
