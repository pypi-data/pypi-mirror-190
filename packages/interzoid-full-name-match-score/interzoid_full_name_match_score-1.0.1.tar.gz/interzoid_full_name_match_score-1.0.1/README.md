## interzoid_full_name_match_score

Python package for generating a match score of two individual person names from 0-100, where 100 is the highest matching score, on how closely two individual full names are likely to be a match. The scoring is based on a series of tests, algorithms, AI, and an ever-growing and improving body of Machine Learning-based generated knowledge. As the context of the data is known, in this case individual person names, it performs far better than generic string comparison algorithms.

### Usage

To generate the match score, you will need the following information:

- an API License key, available at https://www.interzoid.com
- two individual full names to compare

An API is called by the package to access the Cloud server that performs the comparison and provides the score.

Begin by importing the package:

    from interzoid_full_name_match_score import full_name_match_score

Then, provide the information into the get_score() method:

    score, credits, http_code, msg = full_name_match_score.get_score('YOUR-API-KEY','Jim Smith','Mr. James Smythe')

    #200 is the HTTP status for OK
    if http_code == 200:  
        print(score, msg, credits)
    else:
        print(score, "error:", http_code, msg, credits)

The return values will be the generated match comparison score (0-100), how many remaining credits on your API license key, an http code, and a message (OK or Error). The score allows you to set a score threshold in your own logic for your specific case, for example, any score higher than 50 can be considered a "match" (or 60, 70, etc.)

Examples:

    "James Kelly", "Jim Kelly"  ->  85

    "Mr Robert J McCarthy", "Bob Macarthy"  ->  80