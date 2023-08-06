#!/usr/bin/env python3

import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        description="Ribdif correct will take a feature table + taxa table and correct the diversity and genera level for species that can not be differentiated by the used primers")
    
    parser.add_argument("-f", dest = "featuretable", 
                        help = "The feature table to be corrected", 
                        required = True)
    parser.add_argument("-t", dest = "taxatable",
                        help = "The taxa table related to the given feature table",
                        required = True)