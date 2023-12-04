def lookup(input):
    fitbase_ids = [2320127002, 4702921684, 4319703577, 
                   4445114986, 1644430081, 5577150313, 
                   4388161847, 2026352035, 5553957443, 
                   1503960366, 1844505072, 2347167796,
                   7086361926, 3977333714, 6117666160]

    '''
    'user_7086361926.csv', done
    'user_3977333714.csv', done
    'user_6117666160.csv', done
    'user_4558609924.csv', 
    'user_4020332650.csv', 
    'user_8792009665.csv', 
    'user_1927972279.csv', 
    'user_8378563200.csv', 
    'user_6962181067.csv', 
    'user_6775888955.csv', 
    'user_8053475328.csv', 
    'user_7007744171.csv']
    '''

    fhir_ids = ["421e45e2-0ad3-e5c3-9e0f-2cb25f672354", "421e45e2-0ad3-e5c3-9e0f-2cb25f672354", "bbc604f2-9a1c-8a40-4113-2cd2a9228ba0", 
                "428d4180-1673-33e9-917d-bad566910780", "35d9cf9d-1830-73f4-6c3a-6e464d1ad828", "d6965c04-a4e4-fa9f-3c0f-2741ad59bce8", 
                "16bd78bc-1363-7a71-0575-e888da625d5a", "16bd78bc-1363-7a71-0575-e888da625d5a", "11baaff2-58f5-4393-8c0a-58416230e196", 
                "04abb9be-37cc-d005-6a55-d440e79eaff6", "0cb18cae-1af5-bba4-582b-0bcf4eb4f085", "713caf25-4bcf-d07a-2481-01a7289ebd76",
                "bdccfa01-f735-a151-1a25-72212302743f", "c0e6867d-c17c-76f1-a2fe-631715d57aa4", "aaa422c8-d6f9-6537-020d-d69960f44aa1"]

    idx = fitbase_ids.index(int(input)) 
    fhirid = fhir_ids[idx]
    return fhirid