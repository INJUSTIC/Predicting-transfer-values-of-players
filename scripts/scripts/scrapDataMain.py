from scrapFBREF import scrapFBREF
from scrapTransfermarkt import scrapTransfermarkt, get_player_links
from cleaningFinal import dropGoalkeepers, avg_missing
from CombineFBREF_and_Transfermarkt import combine


def gatherData():
    scrapFBREF()
    scrapTransfermarkt(get_player_links())
    combine()
    avg_missing(dropGoalkeepers())


if __name__ == '__main__':
    gatherData()
