#include <iostream>
#include <iomanip>
#include <cstdlib>
#include <string>
#include <random>

using namespace std;

bool Zero(double r);

int main() {

    double seed;
    string awayTeam;
    int awayOff;
    int awayDef;
    string homeTeam;
    int homeOff;
    int homeDef;
    cout << "Away team name:";
    getline(cin, awayTeam);
    cout << "Home team name:";
    getline(cin, homeTeam);
    cout << "Enter stats between 0-100.\n";
    cout << awayTeam << " offense:";
    cin >> awayOff;
    cout << awayTeam << " defense:";
    cin >> awayDef;
    cout << homeTeam << " offense:";
    cin >> homeOff;
    cout << homeTeam << " defense:";
    cin >> homeDef;
    cout << "seed:";
    cin >> seed;

    int awayAdv;
    awayAdv = awayOff - homeDef;
    int homeAdv;
    homeAdv = homeOff - awayDef;
    int adv;
    string possession;

    default_random_engine time(seed);
    normal_distribution<double> distribution (0, 20);

    if (distribution(time) <= 0) {
        cout << endl << homeTeam << " wins the coin toss! \nThey choose to receive.";
        possession = homeTeam;
        adv = homeAdv;
    } else {
        cout << awayTeam << " wins the coin toss! \nThey choose to receive.";
        possession = awayTeam;
        adv = awayAdv;
    }

    char cont;
    cout << "\nPress C and hit enter to continue:";
    cin >> cont;

    int down;
    string abbr;
    int toFirst;
    int toGoal;
    int gained;
    int homeScore;
    homeScore = 0;
    int awayScore;
    awayScore = 0;
    double clock = 1000;
    double r;

    down = 1;
    toFirst = 10;
    toGoal = 75;
    int q;
    q = 1;
    while ((q < 5) || (homeScore == awayScore)) {
        while (clock > 0) {

            switch (down) {
                case (1):
                    abbr = "st";
                    break;
                case (2):
                    abbr = "nd";
                    break;
                case (3):
                    abbr = "rd";
                    break;
                case (4):
                    abbr = "th";
                    break;
                default:
                    cout << "Error: there can't be " << down << " downs";
            }

            cout << endl << down << abbr << " and ";

            if (toGoal <= toFirst)
                cout << "goal";
            else
                cout << toFirst;

            cout << ", ball on ";

            if (toGoal < 50) {
                if (possession == homeTeam)
                    cout << awayTeam << "'s " << toGoal;
                else
                    cout << homeTeam << "'s " << toGoal;
            } else {
                if (possession == awayTeam)
                    cout << awayTeam << "'s " << 100 - toGoal;
                else
                    cout << homeTeam << "'s " << 100 - toGoal;
            }
            cout << "\nPress C and hit enter to continue:";
            cin >> cont;
            r = distribution(time) + adv / 4;
                if (r <= -40) {
                    if (possession == homeTeam) {
                        possession = awayTeam;
                        adv = awayAdv;
                    } else {
                        possession = homeTeam;
                        adv = homeAdv;
                    }
                    cout << "\nPass is intercepted!\n" << possession << " now has the ball.\n";
                    if (Zero(abs(r)))
                        gained = 0;
                    else
                        gained = rand() % abs(static_cast<int>(r));
                    toGoal = 100 - toGoal - gained;
                    toFirst = 10;
                    down = 1;
                    clock -= rand() % 20 + 60;
                } else if ((r > -40) && (r <= -35)) {
                    gained = (rand() % 6 + 1);
                    cout << "\nSacked! A " << gained << " yard loss for " << possession << ".\n";
                    toGoal += gained;
                    toFirst += gained;
                    down++;
                    clock -= rand() % 10 + 30;
                } else if ((r > -35) && (r <= -15)) {
                    cout << "\nIncomplete pass.\n";
                    down++;
                    clock -= rand() % 10 + 10;
                } else if ((r > -15) && (r <= 0)) {
                    if (Zero(r + 15))
                        gained = 0;
                    else
                        gained = rand() % static_cast<int>(r + 15);
                    if (gained > toGoal)
                        gained = toGoal;
                    cout << endl << possession << " ran the ball and gained " << gained << " yards.\n";
                    toGoal -= gained;
                    toFirst -= gained;
                    down++;
                    clock -= rand() % 7 + 20;
                } else if ((r > 0) && (r <= 25)) {
                    if (Zero(r))
                        gained = 1;
                    else
                        gained = rand() % static_cast<int>(r);
                    if (gained > toGoal)
                        gained = toGoal;
                    cout << "\nPass is caught. " << possession << " gained " << gained << " yards.\n";
                    toGoal -= gained;
                    toFirst -= gained;
                    down++;
                    clock -= rand() % 7 + 25;
                } else {
                    if (Zero(r))
                        gained = 0;
                    else
                        gained = rand() % static_cast<int>(r) + 10;
                    if (gained > toGoal)
                        gained = toGoal;
                    cout << "\nPass is caught! " << possession << " gained " << gained << " yards.\n";
                    toGoal -= gained;
                    toFirst -= gained;
                    down++;
                    clock -= rand() % gained / 2 + 60;
                }
                if (toGoal > 100) {
                    cout << "\nSafety!";
                    if (possession == homeTeam) {
                        awayScore += 2;
                        possession = awayTeam;
                        adv = awayAdv;
                    } else {
                        homeScore += 2;
                        possession = homeTeam;
                        adv = homeAdv;
                    }
                    cout << "\nThe score is now " << awayTeam << " " << awayScore
                    << ", " << homeTeam << " " << homeScore << ".\n";
                    down = 1;
                    toFirst = 10;
                    toGoal = 75;
                } else if (toGoal <= 0) {
                    cout << "\nTOUCHDOWN!!";
                    if (possession == homeTeam) {
                        homeScore += 6;
                        possession = awayTeam;
                        adv = awayAdv;
                    } else {
                        awayScore += 6;
                        possession = homeTeam;
                        adv = homeAdv;
                    }
                    cout << "\nThe extra point is...";
                    if (rand() % 7 == 0) {
                        cout << "no good.";
                    } else {
                        cout << "Good!";
                        if (possession == homeTeam) {
                            awayScore += 1;
                        } else {
                            homeScore += 1;
                        }
                    }
                    cout << "\nThe score is now " << awayTeam << " " << awayScore
                         << ", " << homeTeam << " " << homeScore << ".\n";
                    clock -= rand() % 20 + 30;
                    down = 1;
                    toFirst = 10;
                    toGoal = 75;
                } else if (toFirst <= 0) {
                    down = 1;
                    cout << "First down.\n";
                    if (toFirst >= toGoal) {
                        toFirst = toGoal;
                    } else {
                        toFirst = 10;
                    }
                } else if (down == 4) {
                    if ((toGoal >= 5) && (toGoal <= 37)) {
                        cout << endl << possession << " will try for a " << toGoal + 18 << " yard field goal.\n";
                        cout << "\nThe kick is...";
                        if (rand() % 100 >= toGoal + 18) {
                            cout << "Good!\n";
                            if (possession == homeTeam) {
                                homeScore += 3;
                                possession = awayTeam;
                                adv = awayAdv;
                            } else {
                                awayScore += 3;
                                possession = homeTeam;
                                adv = homeAdv;
                            }
                            cout << "The score is now " << awayTeam << " " << awayScore << ", " << homeTeam << " "
                                 << homeScore
                                 << ".\n";
                            toGoal = 75;
                        } else {
                            cout << "no good.\n";
                            if (possession == homeTeam) {
                                possession = awayTeam;
                                adv = awayAdv;
                            } else {
                                possession = homeTeam;
                                adv = homeAdv;
                            }
                            toGoal = 100 - toGoal;
                        }
                        down = 1;
                        toFirst = 10;
                    } else if (toGoal > 40) {
                        int punt = rand() % 20 + 30;
                        clock -= rand() % 20 + 30;
                        cout << possession << " punts the ball for " << punt << " yards.\n";
                        if (possession == homeTeam) {
                            possession = awayTeam;
                            adv = awayAdv;
                        } else {
                            possession = homeTeam;
                            adv = homeAdv;
                        }
                        down = 1;
                        toFirst = 10;
                        toGoal = 100 - toGoal + punt;
                        if (toGoal > 99) {
                            toGoal = 80;
                        }
                    }
                } else if (down > 4) {
                    if (possession == homeTeam) {
                        possession = awayTeam;
                        adv = awayAdv;
                    } else {
                        possession = homeTeam;
                        adv = homeAdv;
                    }
                    cout << "\nTurnover on downs. " << possession << " now has possession.\n";
                    toGoal = 100 - toGoal;
                    toFirst = 10;
                    down = 1;
                }
        }//end clock loop
        q ++;
        clock = 1000;
        if (q <= 4) {
            cout << "\nIt is now Quarter " << q << ".\n";
            cout << "The score is " << awayTeam << " " << awayScore
                 << ", " << homeTeam << " " << homeScore << ".\n";
        } else if (awayScore == homeScore){
            cout << "\nOvertime! The score is tied at " << awayTeam << " "
                 << awayScore << ", " << homeTeam << " " << homeScore << ".\n";
        }
        if (homeScore - awayScore > 42)
            homeAdv -= 10;
        else if (awayScore - homeScore > 42)
            awayAdv -= 10;

    } //end q loop
    cout << "\nAnd that's the end of the game. \n";
    cout << "Final score: " << awayTeam << " " << awayScore
         << ", " << homeTeam << " " << homeScore << ".\n";
 
    return 0;
} //end Main

bool Zero(double r) {
    if (static_cast<int>(r) < 1)
        return true;
    else
        return false;
}