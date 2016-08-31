#!/usr/bin/python
# -*- coding: utf-8 -*-
import binascii
import re
import sys

def one_wgs84_coord_to_tomtom_coord(wgs84_coord_str):
    bd, ad = wgs84_coord_str.split('.')
    tomtom_coord = (bd + ad)[:7]
    return tomtom_coord

def wgs84_coord_to_tomtom_coord(wgs84_coord_str):
    print wgs84_coord_str
    lat, lon = wgs84_coord_str.split(',')

    return one_wgs84_coord_to_tomtom_coord(lon), one_wgs84_coord_to_tomtom_coord(lat)

def waypoint_gm_coord_to_tomtom_coord(waypoint_gm_coord_str):
    lon, lat = waypoint_gm_coord_str.split('!2d')
    lon, lat = one_wgs84_coord_to_tomtom_coord(lon), one_wgs84_coord_to_tomtom_coord(lat)

    return lon, lat

def to_tomtom_itn(tomtom_coords_list):
    s = ''
    for no, tomtom_coord in enumerate(tomtom_coords_list):
        flag = 0
        if no == 0:
            flag = 4
        elif no == len(tomtom_coords_list) - 1:
            flag = 2
        s += '{}|{}|WP - {}|{}|\n'.format(tomtom_coord[0], tomtom_coord[1], no, flag)

    return s

def tomtom_itn_to_file(filename, tomtom_itn):
    with open(filename, "wb") as f:
        f.write(binascii.unhexlify('ef'))
        f.write(binascii.unhexlify('bb'))
        f.write(binascii.unhexlify('bf'))

    with open(filename, "at") as f:
        f.write(tomtom_itn)

#s = "https://www.google.ca/maps/dir/45.4411602,12.3059277/46.5486383,13.7149386/@45.9969317,12.4437186,9z/data=!4m14!4m13!1m10!3m4!1m2!1d13.4880256!2d46.1581339!3s0x477a5021cfa0fa4b:0x4cad8ec4af26197b!3m4!1m2!1d13.7437744!2d46.4220801!3s0x477a63a3a7173027:0xa70900f2994ad9aa!1m0!3e0?hl=en"

def print_help():
    print "Usage: gm_to_itn.py '<google_maps_direction_share_string>' <destination_file>"
    print

def main():
    print 'argv', sys.argv

    if len(sys.argv) < 2:
        print
        print "Not enough arguments"
        print_help()
        return -1
    elif len(sys.argv) > 3:
        print
        print "Too many arguments"
        print_help()
        return -1
    else:
        s = sys.argv[1]

    prefix = "https://www.google.\S+/maps/dir/"

    _, s = re.split(prefix, s)

    re_at_coord = '@\d+\.\d+,\d+\.\d+'

    start_end_coords, waypoints = re.split(re_at_coord, s)

    start_coord_str, end_coord_str, _ = start_end_coords.split('/')

    tomtom_start = wgs84_coord_to_tomtom_coord(start_coord_str)
    tomtom_end = wgs84_coord_to_tomtom_coord(end_coord_str)

    print "Start: {}, End: {}".format(tomtom_start, tomtom_end)


    re_waypoint_coord = '\d+\.\d+!2d\d+\.\d+'

    waypoints_coords = re.findall(re_waypoint_coord, waypoints)

    waypoints_tomtom = []

    all_points_tomtom = [tomtom_start]

    for waypoint in waypoints_coords:
        tt_w = waypoint_gm_coord_to_tomtom_coord(waypoint)
        print tt_w
        waypoints_tomtom.append(tt_w)
        all_points_tomtom.append(tt_w)

    all_points_tomtom.append(tomtom_end)

    tomtom_itn = to_tomtom_itn(all_points_tomtom)
    print tomtom_itn

    if len(sys.argv) == 3:
        tomtom_itn_to_file(sys.argv[2], tomtom_itn)

if __name__ == "__main__":
    main()
