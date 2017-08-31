#! /usr/bin/env python3
from __future__ import print_function
from __future__ import unicode_literals

"""

[+] Description: Recon script to geolocate a street address, gps coords, or ip address by providing multiple satellite views

[+] Author: nxkennedy

[+] Usage: python3 osint-address.py [option] <arg>

"""

import webbrowser
import sys
import argparse
import geocoder
from termcolor import colored


def main():
    descriptionFmtr = print(colored("\n[+] Recon script to geolocate a street address, gps coords, or ip address by providing multiple satellite views", "magenta"))
    parser = argparse.ArgumentParser(description=descriptionFmtr, usage='%(prog)s [option] <arg>')
    parser.add_argument('-a', nargs='*', help='search an address')
    parser.add_argument('-c', nargs='*', help='search coordinates')
    parser.add_argument('-i', help='search ip address')
    args = parser.parse_args()

    # collection of maps
    maps = ["https://www.google.com/maps/embed?origin=mfe&pb=!1m4!2m1!1s{0}+{1}!5e1!6i20", "https://www.google.com/maps/place/{0},{1}", "http://data.mapchannels.com/dualmaps5/map.htm?lat={0}&lng={1}", "https://wego.here.com/?map={0},{1},satellite", "https://www.bing.com/mapspreview?&cp={0}~{1}&lvl=20&sty=a&w=100%25", "https://www.bing.com/mapspreview?&cp={0}~{1}&lvl=20&sty=o&w=100%25&dir=0", "https://www.bing.com/mapspreview?&cp={0}~{1}&lvl=20&sty=o&w=100%25&dir=90", "https://www.bing.com/mapspreview?&cp={0}~{1}&lvl=20&sty=o&w=100%25&dir=180", "https://www.bing.com/mapspreview?&cp={0}~{1}&lvl=20&sty=o&w=100%25&dir=270", "http://wikimapia.org/#lang=en&lat={0}&lon={1}&z=20m=b"]

    # street address lookup function
    def addressLookup(address):
        find_coords = geocoder.google(address)
        lat = find_coords.latlng[0]
        lng = find_coords.latlng[1]
        print(colored("\nSearching... ", 'magenta'))
        for view in maps:
            webbrowser.open(view.format(lat, lng))

        print(colored("Address: {0}".format(address), 'cyan'))
        print(colored("Coords: {0}, {1}\n".format(lat, lng), 'cyan'))

    # ip address lookup function
    def ipAddressLookup(ipaddress):
        find_address = geocoder.ip(ipaddress)
        ipaddress_options = {
            "city": str(find_address.city),
            "state": str(find_address.state),
            "country": str(find_address.country)
        }
        lat = find_address.latlng[0]
        lng = find_address.latlng[1]
        print(colored("\nSearching... ", 'magenta'))
        for view in maps:
            webbrowser.open(view.format(lat, lng))

        print(colored("IP: {0}".format(ipaddress), 'cyan'))
        print(colored("Address: {0}, {1}, {2}".format(ipaddress_options["city"], ipaddress_options["state"], ipaddress_options["country"]), 'cyan'))
        print(colored("Coords: {0}, {1}\n".format(lat, lng), 'cyan'))


    # coordinate lookup function
    def coordLookup(coordinates):
        find_address = geocoder.google([coordinates], method='reverse')
        lat = coordinates.split(' ')[0]
        lng = coordinates.split(' ')[1]
        coordaddress_options = {
            "housenumber": str(find_address.housenumber),
            "street": str(find_address.street),
            "city": str(find_address.city),
            "state": str(find_address.state),
            "postal": str(find_address.postal),
            "country_long": str(find_address.country_long)
        }
        print(colored("\nSearching... ", 'magenta'))
        for view in maps:
            webbrowser.open(view.format(lat, lng))
        print(colored("Address: {0}, {1}, {2}, {3}, {4}, {5}".format(coordaddress_options["housenumber"], coordaddress_options["street"], coordaddress_options["city"], coordaddress_options["state"], coordaddress_options["postal"], coordaddress_options["country_long"]), 'cyan'))
        print(colored("Coords: {0}\n".format(coordinates), 'cyan'))

    # argument checker for start of script
    if len(sys.argv) <= 2:
       parser.print_help()
       sys.exit(1)
    else:
        if sys.argv[1] == "-a":
            address = ' '.join(sys.argv[2:])
            addressLookup(address)
        elif sys.argv[1] == "-c":
            coordinates = ' '.join(sys.argv[2:])
            coordLookup(coordinates)
        elif sys.argv[1] == "-i":
            ipaddress = ' '.join(sys.argv[2:])
            ipAddressLookup(ipaddress)
        else:
            parser.print_help()
            sys.exit(1)

if __name__ == '__main__':
    main()

#google, bing, mailtester.com, pipl api, facebook api, haveibeenpwned, https://groups.google.com/forum/?fromgroups#!search/foo, https://www.google.com/?gws_rd=ssl#q=inurl:ftp+-inurl:(http%7Chttps)+foo,http://www.whoismind.com/email/,
