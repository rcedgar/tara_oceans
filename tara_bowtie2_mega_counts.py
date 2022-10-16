#!/usr/bin/python3

import sys

MIN_MAPQ = 0 # set to zero to avoid losing reads that map to multiple contigs
MIN_ALN_PCT = 75
MIN_PCTID = 90
MIN_POLYA_RUN = 10
MAX_POLYA_PCT = 50
MIN_READ_LENGTH = 50

SAMFileNames = sys.argv[1:]
ContigToMegaFN = "contig_mega.tsv"

CIGAR_Ns = []
CIGAR_Letters = []

def CmpKey__(i):
	global d, Keys
	ki = Keys[i]
	ni = d[ki]
	return ni

def GetOrder(Dict):
	global d, Order, Keys

	d = Dict
	Keys = list(d.keys())
	N = len(Keys)
	Order = list(range(0, N))
	Order.sort(key=CmpKey__)
	Order.reverse()
	return Order

def ParseCigar(C):
	global CIGAR_Ns, CIGAR_Letters

	CIGAR_Ns = []
	CIGAR_Letters = []

	if C == "*":
		return

	n = len(C)
	assert n > 0
	if not C[0].isdigit():
		print(("not C[0].isdigit()", C))
		assert False
	assert C[n-1].isalpha()

	N = 0
	for c in C:
		if c.isdigit():
			N = N*10 + (ord(c) - ord('0'))
		elif c.isalpha() or c == '=':
			CIGAR_Letters.append(c)
			CIGAR_Ns.append(N)
			N = 0
		else:
			print(("not letter or digit", C))
			assert False
	return CIGAR_Ns, CIGAR_Letters

def GetLeftClip():
	if len(CIGAR_Letters) == 0:
		return 0
	if CIGAR_Letters[0] != 'S':
		return 0
	return CIGAR_Ns[0]

def GetRightClip():
	if len(CIGAR_Letters) < 2:
		return 0
	if CIGAR_Letters[-1] != 'S':
		return 0
	return CIGAR_Ns[-1]
	
def GetReadLength():
	L = 0
	for i in range(0, len(CIGAR_Ns)):
		x = CIGAR_Letters[i]
		if x == 'M' or x == 'I' or x == '=' or x == 'X' or x == 'S':
			L += CIGAR_Ns[i]
	return L

def GetSoftClipCount():
	L = 0
	for i in range(0, len(CIGAR_Ns)):
		x = CIGAR_Letters[i]
		if x == 'S':
			L += CIGAR_Ns[i]
	return L

def GetPolyCount_Letter(Seq, Letter):
	L = len(Seq)
	Sum = 0
	Start = None
	for Pos in range(L):
		c = Seq[Pos]
		if c != Letter:
			if Start != None:
				RunLength = Pos - Start
				if RunLength >= MIN_POLYA_RUN:
					Sum += RunLength
			Start = None
		else:
			if Start == None:
				Start = Pos
	if Start != None:
		RunLength = Pos - Start
		if RunLength >= MIN_POLYA_RUN:
			Sum += RunLength
	return Sum

def GetPolyAPct(Seq):
	L = len(Seq)
	if L == 0:
		return 0
	NA = GetPolyCount_Letter(Seq, 'A')
	NT = GetPolyCount_Letter(Seq, 'T')
	Pct = (NA + NT)*100.0/L
	return Pct

NewLong = {}
def Rename(New, Long):
	NewLong[New] = Long
Rename('"""New_12at1.1"""', 'Taraviricota')
Rename('"""New_14at1.1"""', 'Pomiviricota')
Rename('"""New_16at1.1"""', 'Paraxenoviricota')
Rename('"""New_17at1.1"""', 'Lenar-like')
Rename('"""New_18at1.1"""', 'Wamoviricota')
Rename('"""New_19at1.1"""', 'Arctiviricota')

ContigToMega = {}
Contigs = set()
Megas = set()
MegaToCount = {}
for Line in open(ContigToMegaFN):
	Fields = Line[:-1].split('\t')
	assert len(Fields) == 2
	Contig = Fields[0]
	Mega = Fields[1]
	try:
		Mega = NewLong[Mega]
	except:
		pass
	Mega = Mega.replace('"', '')

	assert Contig not in Contigs
	Contigs.add(Contig)
	if Mega not in Megas:
		Megas.add(Mega)
		MegaToCount[Mega] = 0
	ContigToMega[Contig] = Mega

TotalReads = 0
KeptReads = 0
DiscardedLowPctId = 0
DiscardedLowMapQ = 0
DiscardedLowCoverage = 0
DiscardedHighPolyA = 0
DiscardedShort = 0
for SAMFileName in SAMFileNames:
	sys.stderr.write(SAMFileName + "\n")
	for Line in open(SAMFileName):
		if Line.startswith("@"):
			continue
		Fields = Line.split('\t')
		Mapq = int(Fields[4])
		TotalReads += 1
		if Mapq < MIN_MAPQ:
			DiscardedLowMapQ += 1
			continue
		ReadLabel = Fields[0]
		Contig = Fields[2]
		CIGAR = Fields[5]
		ReadSeq = Fields[9]
		if len(ReadSeq) < MIN_READ_LENGTH:
			DiscardedShort += 1
			continue

		Contig = Contig.replace("TARA_", "")
		Contig = Contig.replace("Tara_", "")
		if Contig not in Contigs:
			sys.stderr.write("Not found contig " + Contig + "\n")
			assert False
		NM = None
		Diffs = None
		for Field in Fields[11:]:
			if Field.startswith("NM:i"):
				Diffs = int(Field[5:])
				break
		if Diffs == None:
			sys.stderr.write("NM not found\n")

		ParseCigar(CIGAR)
		SoftClip = GetSoftClipCount()
		ReadLength = GetReadLength()

		assert ReadLength > 0
		AlnPct = (ReadLength - SoftClip)*100.0/ReadLength
		PctId = (ReadLength - Diffs)*100.0/ReadLength
		if AlnPct < MIN_ALN_PCT:
			DiscardedLowCoverage += 1
			continue
		if PctId < MIN_PCTID:
			DiscardedLowPctId += 1
			continue

		PolyA = GetPolyAPct(ReadSeq)
		if PolyA > MAX_POLYA_PCT:
			DiscardedHighPolyA += 1
			continue

		KeptReads += 1
		Mega = ContigToMega[Contig]
		MegaToCount[Mega] += 1

Order = GetOrder(MegaToCount)
MegaList = list(MegaToCount.keys())
print("Total\t%d" % TotalReads)
print("Kept\t%d" % KeptReads)
print("DiscardedLowMapQ\t%d\t%.1f%%" % (DiscardedLowMapQ, (DiscardedLowMapQ*100.0)/TotalReads))
print("DiscardedShort\t%d\t%.1f%%" % (DiscardedShort, (DiscardedShort*100.0)/TotalReads))
print("DiscardedHighPolyA\t%d\t%.1f%%" % (DiscardedHighPolyA, (DiscardedHighPolyA*100.0)/TotalReads))
print("DiscardedLowCoverage\t%d\t%.1f%%" % (DiscardedLowCoverage, (DiscardedLowCoverage*100.0)/TotalReads))
print("DiscardedLowPctId\t%d\t%.1f%%" % (DiscardedLowPctId, (DiscardedLowPctId*100.0)/TotalReads))

SumPct = 0
for k in Order:
	Mega = MegaList[k]
	n = MegaToCount[Mega]
	Pct = (n*100.0)/KeptReads
	SumPct += Pct
	s = "%d" % n
	s += "\t%.3g%%" % Pct
	s += "\t" + Mega
	print(s)
