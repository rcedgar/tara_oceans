#!/usr/bin/python3

import sys

S7FN = "tara_data/TableS7.tsv"

f = open(S7FN)
Hdr = f.readline()[:-1]
HdrFields = Hdr.split('\t')
assert len(HdrFields) == 93

FieldNr01 = None
for i in range(0, 93):
	if HdrFields[i] == "0.1":
		FieldNr01 = i
assert FieldNr01 != None

NI = 20

Infs = HdrFields[FieldNr01:FieldNr01+NI]

InfToClusters = []
for i in range(0, NI):
	Clusters = set()
	InfToClusters.append(Clusters)


while 1:
	Line = f.readline()
	if len(Line) == 0:
		break
	Fields = Line[:-1].split('\t')
	assert len(Fields) == 93

	Label = Fields[1]

	for i in range(0, NI):
		ClusterNr = int(Fields[FieldNr01+i])
		InfToClusters[i].add(ClusterNr)

for i in range(0, NI):
	Inf = Infs[i]
	Clusters = InfToClusters[i]
	ClusterCount = len(Clusters)
	print("%s\t%d" % (Inf, ClusterCount))
