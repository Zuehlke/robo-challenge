#!/bin/env python3

import time

from gamemaster import TournamentRadio, Tournament

LOOP_CYCLE_TIME_SEC = 0.5

if __name__ == '__main__':
    tournament = Tournament()

    with TournamentRadio("broker", 1883, tournament) as radio:
        while True:
            radio.process_messages(LOOP_CYCLE_TIME_SEC)
            radio.publish_tournament(tournament)
            time.sleep(1)