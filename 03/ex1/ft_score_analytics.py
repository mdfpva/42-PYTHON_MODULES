#!/usr/bin/env python3

import sys


def ft_score_analytics() -> None:
    print("=== Player Score Analytics ===")
    if (len(sys.argv) == 1):
        print("No scores provided. Usage: python3 ft_score_analytics.py "
              "<score1> <score2> ...")
    else:
        args = []
        for arg in sys.argv[1:]:
            try:
                args.append(int(arg))
            except ValueError:
                print(f"Invalid parameter: '{arg}'")
        if (len(args) == 0):
            print("No scores provided. Usage: python3 ft_score_analytics.py "
                  "<score1> <score2> ...")
        else:
            print(f"Total players: {len(args)}")
            print(f"Total score: {sum(args)}")
            print(f"Average score: {sum(args) / len(args)}")
            print(f"High score: {max(args)}")
            print(f"Low score: {min(args)}")
            print(f"Score range: {max(args) - min(args)}")
    return


def main() -> None:
    ft_score_analytics()
    return


if __name__ == "__main__":
    main()
