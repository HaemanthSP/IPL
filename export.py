import json
import os

def transform_teams(teams_file):
    """
    Transform teams data from TSV to a list of dictionaries.
    
    Args:
        teams_file (str): Path to the teams TSV file
    
    Returns:
        list: Transformed teams data with additional metadata
    """
    transformed_teams = []
    
    with open(teams_file, 'r') as f:
        for line in f:
            name, abbr, code = line.strip().split('\t')
            transformed_teams.append({
                'name': name,
                'abbr': abbr,
                'code': code,
                'rank': len(transformed_teams) + 1  # Dynamic ranking based on order
            })
    
    return transformed_teams

def transform_venues(venues_file):
    """
    Transform venues data from TSV to a list of dictionaries.
    
    Args:
        venues_file (str): Path to the venues TSV file
    
    Returns:
        list: Transformed venues data
    """
    transformed_venues = []
    
    with open(venues_file, 'r') as f:
        for line in f:
            name, sym = line.strip().split('\t')
            transformed_venues.append({
                'name': name,
                'sym': sym
            })
    
    return transformed_venues

def transform_matches(matches_file, teams, venues):
    """
    Transform matches data from TSV to a list of dictionaries.
    
    Args:
        matches_file (str): Path to the matches TSV file
        teams (dict): Dictionary of teams for validation
        venues (dict): Dictionary of venues for validation
    
    Returns:
        list: Transformed matches data
    """
    transformed_matches = []
    
    with open(matches_file, 'r') as f:
        for line in f:
            match_day, match_id, day, date, time, teamA, teamB, venue = line.strip().split('\t')
            
            # Validate teams and venues
            if teamA not in teams or teamB not in teams or venue not in venues:
                print(f"Warning: Invalid data in match {match_id}")
                continue
            
            transformed_matches.append({
                'id': int(match_id),
                'day': day,
                'date': date,
                'teamA': teamA,
                'teamB': teamB,
                'venue': venue,
                'time': time
            })
    
    return sorted(transformed_matches, key=lambda x: x['id'])

def export_json(data, filename):
    """
    Export data to a JSON file.
    
    Args:
        data (list/dict): Data to be exported
        filename (str): Output JSON filename
    """
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

def main():
    # Define input and output paths
    input_files = {
        'teams': 'teams.tsv',
        'venues': 'venues.tsv',
        'matches': 'fixtures.tsv'
    }
    
    output_files = {
        'teams': 'teams.json',
        'venues': 'venues.json',
        'matches': 'matches.json'
    }
    
    # Transform teams
    teams_data = transform_teams(input_files['teams'])
    export_json(teams_data, output_files['teams'])
    
    # Transform venues
    venues_data = transform_venues(input_files['venues'])
    export_json(venues_data, output_files['venues'])
    
    # Create lookup dictionaries for validation
    teams_lookup = {team['abbr']: team for team in teams_data}
    venues_lookup = {venue['name']: venue for venue in venues_data}
    
    # Transform matches
    matches_data = transform_matches(
        input_files['matches'], 
        teams_lookup, 
        venues_lookup
    )
    export_json(matches_data, output_files['matches'])
    
    print("Data transformation complete. JSON files generated.")

if __name__ == "__main__":
    main()