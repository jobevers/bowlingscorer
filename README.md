# Bowling Score Stats

This script parses the database from the
[Bowling Scorer android app](https://play.google.com/store/apps/details?id=jp.gr.java_conf.yotchan.bowlingscorerfree).

In settings, you can save a backup of the database, which is stored in
`/BowlingScorer/Backup.db`. I transfer this database to my computer and
run the `parse_db.py` script to print out additional stats.

Output:
```
» python parse_db.py Backup.db
First Ball Average: 8.441666666666666
You've bowled 120 frames
---
Pin Leaves
Pin	1	2
1	13.33%	3.33%
2	12.50%	3.33%
3	22.50%	5.00%
4	15.00%	4.17%
5	22.50%	5.00%
6	20.00%	3.33%
7	13.33%	7.50%
8	5.83%	2.50%
9	8.33%	0.00%
10	22.50%	10.00%
---
Strikes: 35 / 120 => 29.166667%
Spares: 44 / 120 => 36.666667%
Opens: 41 / 120 => 34.166667%
---
Splits: 25 / 85 => 29.411765%
Split-Conversion: 6 / 25 => 24.000000%
---
Non-Splits: 60 / 85 => 70.588235%
Non-Split-Conversion: 38 / 60 => 63.333333%
---
Single Pin Leaves: 28 / 60 => 0.4666666666666667
Single Pin Conversion: 19 / 28 =>  0.6785714285714286
For pin 10: 4 / 7 => 57.1%
For pin 2: 0 / 2 => 0.0%
For pin 8: 0 / 1 => 0.0%
For pin 7: 0 / 1 => 0.0%
For pin 4: 2 / 3 => 66.7%
For pin 3: 2 / 3 => 66.7%
For pin 9: 2 / 2 => 100.0%
For pin 6: 4 / 4 => 100.0%
For pin 5: 4 / 4 => 100.0%
For pin 1: 1 / 1 => 100.0%
SINGLE PIN CONVERSION IS THE EASIEST WAY TO IMPROVE YOUR AVERAGE!
IF THIS WAS 100%, YOUR AVERAGE WOULD INCREASE BY: 7.08125
```
