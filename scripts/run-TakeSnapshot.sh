#!/bin/bash
# SPDX-License-Identifier: MIT
#
# This is a quick-and-dirty script which detects the parameters
# necessary for running scripts/TakeSnapshot.py over multiple scenarios
# without having to manually figure the parameters.
# Requires further tweaking for future use, see TODO.
#
# Copyright (C) 2023 Government of Canada
# Author: Anthony Fok

set -euo pipefail

# TODO: Edit the "scenarios" array as necessary before use

scenarios=(
	ACM5p2_VedderFault
	ACM5p0_MysteryLake
	ACM5p7_SoutheyPoint
	ACM4p9_VedderFault
	SCM5p9_MillesIlesFault
	SCM5p6_GloucesterFault
	ACM5p2_BeaufortFault
	ACM7p7_QueenCharlotteFault
	ACM5p0_GeorgiaStraitFault
	ACM8p0_QueenCharlotteFault
	SCM5p0_BurlingtonTorontoStructuralZone
	SCM5p0_RougeBeach
	ACM5p5_SoutheyPoint
)

for i in "${scenarios[@]}"; do
	echo "Checking $i:"
	# shellcheck disable=SC2012
	n=$(ls -1 "s_shakemap_${i}_"*".csv" | sed -E 's/.*_([0-9]+).csv/\1/')
	# shellcheck disable=SC2012
	expo=$(ls -1 "s_consequences_${i}_b0_$((n+1))_"?".csv" | sed -E 's/.*_(b|s).csv/\1/')

	# Verify that all 7 CSV files exist for each scenario
	echo -en "\t"
	ls "s_shakemap_${i}_$((n)).csv"
	echo -en "\t"
	ls "s_consequences_${i}_b0_$((n+1))_$expo.csv" "s_dmgbyasset_${i}_b0_$((n+1))_$expo.csv"
	echo -en "\t"
	ls "s_consequences_${i}_r1_$((n+2))_$expo.csv" "s_dmgbyasset_${i}_r1_$((n+2))_$expo.csv"
	echo -en "\t"
	ls "s_lossesbyasset_${i}_b0_$((n+3))_$expo.csv" "s_lossesbyasset_${i}_r1_$((n+4))_$expo.csv"

	# Run TakeSnapshot.py
	echo "Running ../scripts/TakeSnapshot.py $i $expo $((n)) $((n+1)) $((n+2)) $((n+3)) $((n+4)):"
	../scripts/TakeSnapshot.py "$i" "$expo" $((n)) $((n+1)) $((n+2)) $((n+3)) $((n+4))
	echo
done
