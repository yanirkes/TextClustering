# external libraries
from flask import Flask, request, jsonify, render_template_string
import json
import os
import pandas as pd
import random

# Internal libraries
from model import my_model


app = Flask(__name__)

# Route for the home page, which renders an HTML form for user input
@app.route('/', methods=['GET'])
def home():
    # Simple HTML form to accept the number of groups
    html = '''
    <h1>Welcome to the Flask App!</h1>
    <form action="/groups" method="POST">
        <label for="groups">Enter number of groups:</label>
        <input type="number" id="groups" name="groups" value="1" min="1">
        <button type="submit">Submit</button>
    </form>
    '''
    return render_template_string(html)

@app.route('/groups', methods=['POST'])
def hello_user():
    # Get the number of groups from the submitted form
    submits = request.form.get('groups', type=int)

    # Validate the input before proceeding
    if validate_input(submits):
        # Select random groups based on user input
        random_groups = random_group_selection(submits)

        # Create the response dictionary with group details
        return_group_dict = {
            "groups": [
                {
                    "title": row['topic'],  # Use correct dictionary key
                    "number_of_claims": str(row['count'])  # Convert count to string
                } for ind, row in groups_distribution.iloc[random_groups].iterrows()
            ]
        }
        # Convert response dictionary to JSON
        response = json.dumps(return_group_dict)
    else:
        # Handle invalid input
        response = json.dumps({
            "message": "You've submitted an invalid value for groups."
        })

    # Return the response as JSON with HTTP status code 200 (OK)
    return jsonify(response), 200


# Function to validate user input for the number of groups
def validate_input(submits):
    """
    Validate the user's input for the number of groups.
    Ensures that the number is greater than 0 and less than or equal to the number of available groups.
    """
    if submits <= 0:
        return False
    elif submits > groups_distribution.shape[0]:
        return False
    return True

# Function to select random groups
def random_group_selection(number_of_groups):
    """
    Randomly select a number of unique groups based on user input.
    """
    unique_groups = dbmodel.df_['topic'].nunique()

    # Randomly select a sample of group indices based on the available unique topics
    random_groups = random.sample(range(unique_groups), number_of_groups)

    return random_groups

if __name__ == '__main__':
    # Get the path to the current file
    current_file_path = os.path.abspath(__file__)
    # Define the path to the project directory
    project_dir = os.path.dirname(os.path.dirname(current_file_path))
    # Construct the path to the CSV file with group data
    group_data_path = os.path.join(project_dir, 'data', 'claims_text.csv')

    # Load the CSV data into a DataFrame
    corpus_df = pd.read_csv(group_data_path)

    # Initialize the model with the loaded data
    dbmodel = my_model.claimsModel(corpus_df)

    # Group the data by 'topic' and count the number of claims per topic
    groups_distribution = dbmodel.df_.groupby('topic')['text'].count().reset_index().rename(columns={'text': 'count'})

    # Run the Flask app in debug mode
    app.run(debug=True)