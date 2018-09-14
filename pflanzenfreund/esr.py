"""
Function for generating ESR-numbers for orange swiss payment slips ("Oranger Einzahlungsschein").
@param
    bc "Belegartcodes": fix, "01" or "04"
    chf: dynamic, amount in chf without rappen, must have eight chars minimum (if less than eight chars, insert zeros before)
    rappen: dynamic, amount in rappen
    help1, help2, help3: fix, "+" or ">", no editing required
    referenceNumber: dynamic, contains matag number, zeros, client number and job number
    participantNumber: dynamic, bankaccount number
@usage generateCodeline("4378", "85", "94476300000000128001105152", "01200027")
 
"""
def moduloTenRecursive(number):
	lut = [0, 9, 4, 6, 8, 2, 7, 1, 3, 5];
	carryover = 0;
	for i in str(number):
		t = carryover + int(i)
		carryover = lut[t % 10];
	return str((10 - carryover) % 10)

@frappe.whitelist()
def generateCodeline(chf, rappen, referenceNumber, participantNumber):
	if len(referenceNumber) < 27:  # check if referenceNumber has less than 27 chars
		referenceNumber = (27-len(referenceNumber))*"0" + referenceNumber
			
	chf = str(chf)
	rappen = str(rappen) 
	if len(chf) < 8:  # check if amount has less than eight chars
		chf = (8-len(chf))*"0" + chf
	if len(rappen) < 2:  # check if amount has less than 2 chars
		rappen = (2-len(rappen))*"0" + rappen

	# dynamic, check digit for bc and value (calculated with modulo 10 recursive)
	p1 = moduloTenRecursive(bc + chf + rappen)  
	# dynamic, check digit for referenceNumber (calculated with modulo 10 recursive)
	p2 = moduloTenRecursive(referenceNumber)
	
	return bc + chf + rappen + p1 + help1 + referenceNumber + p2 + help2 + " " + participantNumber + help3