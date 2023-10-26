from NBA import NBA
from os import getenv 

def main():

    nba = NBA()

    # get statistics 
    nba_website = getenv("BOX_SCORES")
    stats_df = nba.get_box_scores(url=nba_website)

    if stats_df.shape[0] != 0:
        stats_df.to_csv("./reports/box_scores.csv", index=False)


if __name__ == '__main__':
    main()