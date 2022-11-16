# Teeko2
An AI game player for a modified version of the game called Teeko. We call this modified version Teeko2.

Teeko is a game between two players on a 5x5 board. Each player has four markers of either red or black. Beginning with black, they take turns placing markers (the "drop phase") until all markers are on the board, with the goal of getting four in a row horizontally, vertically, or diagonally, or in a 2x2 box as shown above. If after the drop phase neither player has won, they continue taking turns moving one marker at a time -- to an adjacent space only! (Note this includes diagonals, not just left, right, up, and down one space.) -- until one player wins.

# How to play Teeko2
The Teeko2 rules are almost identical to those of Teeko but we will exchange a rule. Specifically, we remove the 2x2 box winning condition and replace it with a 3x3 box winning condition -- same colored markers at the four corners of a 3x3 square. Mathematically, if (i,j) is the center of a 3x3 board, then it must be that (i,j) is empty and that there is a marker of the appropriate color on each of (i-1,j-1), (i-1,j+1), (i+1,j-1), and (i+1,j+1). 
