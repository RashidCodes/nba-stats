from NBA import NBA
from os import getenv 

def main():

    nba = NBA()

    # get statistics 
    nba_website = getenv("NBA_WEBSITE")
    stats_df = nba.get_stats(url=nba_website)

    if stats_df.shape[0] != 0:
        stats_df.to_excel("./reports/stats.xlsx", index=False)


if __name__ == '__main__':
    main()