"""
Global variables for color coding based upon candidate and sentiment, 
for importing into server file
"""

POSITIVE_COLORS = {"Trump" : {"backgroundColor" : "rgba(253, 175, 175, 0.2)",
                        "borderColor" : "rgba(253, 175, 175,1)",
                        "pointBorderColor" : "rgba(253, 175, 175,1)",
                        "pointHoverBorderColor" : "rgba(253, 175, 175,1)"},
            "Clinton" : {"backgroundColor" : "rgba(143, 211, 228, 0.2)",
                        "borderColor" : "rgba(143, 211, 228,1)",
                        "pointBorderColor" : "rgba(143, 211, 228,1)",
                        "pointHoverBorderColor" : "rgba(143, 211, 228,1)"},
            "Both" : {"backgroundColor" : "rgba(128, 239, 133, 0.2)",
                        "borderColor" : "rgba(128, 239, 133, 1)",
                        "pointBorderColor" : "rgba(128, 239, 133, 1)",
                        "pointHoverBorderColor" : "rgba(128, 239, 133, 1)"}}


################################################################################


NEGATIVE_COLORS = {"Trump" : {"backgroundColor" : "rgba(182,6,6,0.2)",
                        "borderColor" : "rgba(182,6,6,1)",
                        "pointBorderColor" : "rgba(182,6,6,1)",
                        "pointHoverBorderColor" : "rgba(182,6,6,1)"},
            "Clinton" : {"backgroundColor" : "rgba(55,7,247,0.2)",
                        "borderColor" : "rgba(55,7,247,1)",
                        "pointBorderColor" : "rgba(55,7,247,1)",
                        "pointHoverBorderColor" : "rgba(55,7,247,1)"},
            "Both" : {"backgroundColor" : "rgba(17, 130, 53, 0.2)",
                        "borderColor" : "rgba(17, 130, 53, 1)",
                        "pointBorderColor" : "rgba(17, 130, 53, 1)",
                        "pointHoverBorderColor" : "rgba(17, 130, 53, 1)"}}


################################################################################


GOOGLE_MAPS_COLORS = {"Trump" : {"neg" : "rgba(253,0,0,1)", "pos" : "rgba(255,199,199,1)"},
                        "Clinton" : {"neg" : "rgba(55,7,247,1)", "pos" : "rgba(143, 211, 228,1)"},
                        "Both" : {"neg" : "rgba(20, 163, 27, 1)", "pos" : "rgba(128, 239, 133, 1)"}}


################################################################################


CANDIDATE_COUNTS = {"Clinton" : { "neg" : 0, "pos" : 0},
                  "Trump" : {"neg" : 0, "pos" : 0}, 
                  "Both" : {"neg" : 0, "pos" : 0}}


SEED_DATA_DIR = "seed_data/"

TEST_DATA_DIR = "test_data/"

CANDIDATE_SENTIMENT_FILES = {"Clinton" : "seed_data/clinton_data.txt", 
                              "Trump" : "seed_data/trump_data.txt", 
                              "Both" : "seed_data/both_data.txt"}




