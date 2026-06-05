#!/usr/bin/env python3

import math


def get_player_pos() -> tuple:
    while (True):
        raw_coordinates: str = input("Enter new coordinates "
                                     "as floats in format 'x,y,z': ")
        coordinates: list = raw_coordinates.split(",")
        if (len(coordinates) != 3):
            print("Invalid syntax")
            continue
        coords = []
        error = False
        for coordinate in coordinates:
            try:
                coords.append(float(coordinate.strip()))
            except ValueError as e:
                print(f"Error on parameter '{coordinate.strip()}': {e}")
                error = True
                break
        if (not error):
            return (coords[0], coords[1], coords[2])


def ft_coordinate_system() -> None:
    print("=== Game Coordinate System ===\n")
    print("Get a first set of coordinates")
    s1: tuple = get_player_pos()
    print(f"Got a first tuple: {s1}")
    print(f"It includes: X={s1[0]}, Y={s1[1]}, Z={s1[2]}")
    distance_to_center: float = round(math.sqrt((s1[0]**2) + (s1[1]**2) +
                                      (s1[2]**2)), 4)
    print(f"Distance to center: {distance_to_center}")
    print("")
    print("Get a second set of coordinates")
    s2: tuple = get_player_pos()
    distance_between_pos: float = round(math.sqrt(((s2[0] - s1[0])**2) +
                                        ((s2[1] - s1[1])**2) +
                                        ((s2[2] - s1[2])**2)), 4)
    print("Distance between the 2 sets of coordinates: "
          f"{distance_between_pos}")
    return


def main() -> None:
    ft_coordinate_system()
    return


if __name__ == "__main__":
    main()
