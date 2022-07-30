#!/usr/bin/python3

import sys
from sklearn.metrics.cluster import adjusted_rand_score

GPFN = "edgar_data/genbank_phylum.tsv"
S7FN = "tara_data/TableS7.tsv"

AccToPhy = {}

f = open(GPFN)
Hdr = f.readline()
assert Hdr.startswith("Genbank	Phylum")
while 1:
	Line = f.readline()
	if len(Line) == 0:
		break
	Fields = Line[:-1].split('\t')
	assert len(Fields) == 2

	Acc = Fields[0]
	Phy = Fields[1]

	if Phy != ".":
		AccToPhy[Acc] = Phy

f = open(S7FN)
Hdr = f.readline()[:-1]
HdrFields = Hdr.split('\t')
assert len(HdrFields) == 93

FieldNr05 = None
for FieldNr in range(0, len(HdrFields)):
	if HdrFields[FieldNr] == "0.5":
		assert FieldNr05 == None
		FieldNr05 = FieldNr
assert FieldNr05 != None

MegaClusterVec = []
AccVec = []
PhyVec = []
ClustersVec = [] 

while 1:
	Line = f.readline()
	if len(Line) == 0:
		break
	Fields = Line[:-1].split('\t')
	assert len(Fields) == 93

	Label = Fields[1]
	if Label[0] == '"':
		Label = Label[1:]
	if not Label.startswith("REF_"):
		continue

# delete REF_
	Label = Label[4:]

# find the first underscore that can't be in the GenBank accession
	n = Label[4:].find('_')
	Label = Label[:n+4]

# strip .n version to leave version-independent accession
	Acc = Label.split('.')[0]
	try:
		Phy = AccToPhy[Acc]
	except:
		Phy = None

# must have phylum to evaluate agreement
	if Phy == None:
		continue

	MegaCluster = Fields[2]

	MegaClusterVec.append(MegaCluster)
	AccVec.append(Acc)
	PhyVec.append(Phy)

	Clusters = []
	for i in range(0, 11):
		Cluster = int(Fields[FieldNr05+i])
		Clusters.append(Cluster)
	ClustersVec.append(Clusters)

N = len(AccVec)
assert len(PhyVec) == N
assert len(ClustersVec) == N

print("Inf	ARA_Phylum	ARI_MegaCluster")
for i in range(0, 11):
	FieldNr = FieldNr05 + i
	Inf = HdrFields[FieldNr]

	Clusters = []
	for j in range(0, N):
		Clusters.append(ClustersVec[j][i])

	ARI_MegaCluster = adjusted_rand_score(MegaClusterVec, Clusters)
	ARI_Phylum = adjusted_rand_score(PhyVec, Clusters)

	s = Inf
	s += "\t%.3f" % ARI_Phylum
	s += "\t%.3f" % ARI_MegaCluster
	print(s)
