#!/usr/bin/python3

import sys

S7FN = "tara_data/TableS7.tsv"

f = open(S7FN)
Hdr = f.readline()[:-1]
HdrFields = Hdr.split('\t')
assert len(HdrFields) == 93

MegaClusterToCount = []
MegaClusterToName = []
for MegaCluster in range(0, 19):
	MegaClusterToCount.append(0)
	MegaClusterToName.append(None)

while 1:
	Line = f.readline()
	if len(Line) == 0:
		break
	Fields = Line[:-1].split('\t')
	assert len(Fields) == 93

	Label = Fields[1]
	MegaCluster = int(Fields[23]) - 1
	MegaClusterName = Fields[2]

	MegaClusterToCount[MegaCluster] += 1

	if MegaClusterToName[MegaCluster] == None:
		MegaClusterToName[MegaCluster] = MegaClusterName

for MegaCluster in range(0, 19):
	Name = MegaClusterToName[MegaCluster]
	Name = Name.replace('"', '')

	if Name == "New_12at1.1":
		Name = "New_12at1.1 (Taraviricota)"
	elif Name == "New_14at1.1":
		Name = "New_14at1.1 (Pomiviricota)"
	elif Name == "New_19at1.1":
		Name = "New_19at1.1 (Arctiviricota)"
	elif Name == "New_16at1.1":
		Name = "New_16at1.1 (Paraxenoviricota)"
	elif Name == "New_17at1.1":
		Name = "New_17at1.1 (Lenar-like)"
	elif Name == "New_18at1.1":
		Name = "New_18at1.1 (Wamoviricota)"

	s = "%d" % MegaClusterToCount[MegaCluster]
	s += "\t" + Name
	print(s)
