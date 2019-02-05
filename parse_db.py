import argparse
import collections
import sqlite3
import sys

import pandas as pd


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('db')
    args = parser.parse_args()

    conn = sqlite3.connect(args.db)
    conn.row_factory = sqlite3.Row 
    process_db(conn)


def process_db(conn):
    # ['ID', 'Game', 'Frame', 'T1', 'T2', 'Foul1', 'Foul2', 'Split', 'Renzoku', 'Pin']
    rows = conn.execute("""
select *
from T_Games G
inner join T_Event E
on G.ID = E.ID
where Frame <= 10
and (
  E.comment is null or 
  (trim(lower(E.comment)) != 'low ball'))""").fetchall()
    df = pd.DataFrame(rows, columns=rows[0].keys())
    fba = df['T1'].mean()
    print(f'First Ball Average: {fba}')
    
    pin_leaves = []
    for row in rows:
        pins = row['Pin']
        pin_leaves.append(parse_pins(pins))
    n = len(pin_leaves)
    print(f"You've bowled {n} frames")
    first = collections.defaultdict(int)
    second = collections.defaultdict(int)
    for leave in pin_leaves:
        for pin in leave['first_ball']:
            first[pin] += 1
        for pin in leave['second_ball']:
            second[pin] += 1
    print('---')
    print('Pin Leaves')
    print('Pin\t1\t2')
    for pin in range(1, 11):
        print(f'{pin}\t{first[pin] / n:0.2%}\t{second[pin] / n:0.2%}')
    print('---')
    frames = 0
    strikes = 0
    spares = 0
    opens = 0
    splits = 0
    split_conversion = 0
    non_splits = 0
    non_split_conversion = 0
    single_pin_leaves = collections.defaultdict(int)
    single_pin_conversions = collections.defaultdict(int)
    games = set((r['ID'], r['Game']) for r in rows)

    for row in rows:
        if row['Frame'] > 10:
            continue
        frames += 1
        if row['T1'] == 10:
            strikes += 1
            continue
        if row['T1'] + row['T2'] == 10:
            spares += 1
        else:
            opens += 1
        if row['Split']:
            splits += 1
            if row['T1'] + row['T2'] == 10:
                split_conversion += 1
        else:
            non_splits += 1
            if row['T1'] + row['T2'] == 10:
                non_split_conversion += 1
        leaves = parse_pins(row['Pin'])
        if len(leaves['first_ball']) == 1:
            pin = next(iter(leaves['first_ball']))
            single_pin_leaves[pin] += 1
            if len(leaves['second_ball']) == 0:
                single_pin_conversions[pin] += 1
    print(f'Strikes: {strikes} / {frames} => {strikes/frames:%}')
    print(f'Spares: {spares} / {frames} => {spares/frames:%}')
    print(f'Opens: {opens} / {frames} => {opens/frames:%}')
    print('---')
    non_strikes = frames - strikes
    print(f'Splits: {splits} / {non_strikes} => {splits/non_strikes:%}')
    print(f'Split-Conversion: {split_conversion} / {splits} => {split_conversion/splits:%}')
    print('---')
    print(f'Non-Splits: {non_splits} / {non_strikes} => {non_splits/non_strikes:%}')
    print(f'Non-Split-Conversion: {non_split_conversion} / {non_splits} => {non_split_conversion/non_splits:%}')
    print('---')
    n_single_pin_conversions = sum(single_pin_conversions.values())
    n_single_pin_leaves = sum(single_pin_leaves.values())
    print(f'Single Pin Leaves: {n_single_pin_leaves} / {non_splits} => {n_single_pin_leaves / non_splits}')
    print(f'Single Pin Conversion: {n_single_pin_conversions} / {n_single_pin_leaves} =>  {n_single_pin_conversions / n_single_pin_leaves}')
    for _, pin in sorted_single_pins_by_misses(single_pin_leaves, single_pin_conversions):
        conv = single_pin_conversions[pin]
        left = single_pin_leaves[pin]
        rate = conv / left
        print(f'For pin {pin}: {conv} / {left} => {rate:0.1%}')
    n_games = len(games)
    missed_single_pins = n_single_pin_leaves - n_single_pin_conversions
    missed_single_pins_per_game = missed_single_pins / n_games
    better_average = missed_single_pins_per_game * (fba + 1)
    print(f'If single pin conversion was 100%, your average would increase by: {better_average}')


def sorted_single_pins_by_misses(leaves, conversions):
    return sorted(
        [(leaves[pin] - conversions[pin], pin) for pin in range(1, 11)],
        reverse=True
    )

# what is a more verbose way of expressing the
# pins?
# {first_ball: [remaining pins], second_ball: [remaining pins]}
def parse_pins(pin_int):
    pin_str = str(pin_int)
    if pin_str == '0':
        return {'first_ball': set(), 'second_ball': set()}
    first_ball = set()
    second_ball = set()
    for i, val in zip(range(11 - len(pin_str), 11), pin_str):
        if val == '2':
            first_ball.add(i)
            second_ball.add(i)
        elif val == '1':
            first_ball.add(i)
    return {'first_ball': first_ball, 'second_ball': second_ball}
            




if __name__ == '__main__':
    sys.exit(main())
