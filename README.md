# Megaverse Map Builder

## Overview

The Megaverse Map Builder is a Python application that interacts with the Megaverse API to build and manage a virtual map. Users can set and remove various entities on the map, such as Polyanets, Soloons, and Comeths, based on a predefined goal map.

## Features

- **Build Map**: Construct the map by placing entities according to the goal map retrieved from the API.
- **Reset Map**: Remove all entities from the map or reset specific rows.
- **Entity Management**: Add or delete Polyanets, Soloons, and Comeths based on the goal.

## Prerequisites

- Python 3.x
- `requests` library
- `python-dotenv` library (for managing environment variables)

You can install the required libraries using pip:

```bash
pip install requests python-dotenv
```

## Environment Variables

Before running the application, you need to set your candidate ID as an environment variable. Create a .env file in the root directory of the project and add the following line:

```bash
CM_CANDIDATE_ID=your_candidate_id
```

Replace `your\_candidate\_id` with your actual candidate ID.

## Usage

1. Clone the repository

1.  Create a .env file and set your candidate ID as mentioned above.
    
1. Run the application: `python main.py`

1.  The MapBuilder will automatically retrieve the goal map and place the entities accordingly. You can also specify a specific row to build by modifying the build\_map method call in main.py.

