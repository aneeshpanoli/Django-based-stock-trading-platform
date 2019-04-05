def institutions():
    keywords = ["Natixis", "TIAA", "Deutsche", "Invesco", "Franklin", "Rowe", "AXA", "Legg", "Sumitomo"\
    , "UBS", "Affiliated", "Mitsubishi", "Insight", "BNP", "New", "Allianz", "Columbia", "AllianceBernstein"\
    , "Schroder", "APG", "Generali", "Aberdeen", "Aviva", "HSBC", "MFS", "Morgan"\
    , "Dimensional", "Principal", "Aegon", "Standard", "M&G", "Federated", "Mellon"\
    , "Wells", "Natixis", "Macquarie", "Nomura", "Credit", "Eaton", "Manulife", "Robeco"\
    , "Eurizon", "Union", "RBC", "MEAG", "Fidelity", "SEI", "Dodge", "Pioneer"\
    , "Neuberger", "DekaBank", "BNY", "Babson", "BMO", "Loomis", "Voya", "Nordea", "NN"\
    , "SEB", "Guggenheim", "PGGM", "Nuveen", "Swiss", "Baillie", "TCW", "Caisse"\
    , "Janus", "Santander", "Lazard", "Russell", "La Banque", "Nikko", "Standish"\
    , "Pictet", "Putnam", "Bridgewater", "Bank", "DIAM", "AQR", "First", "American"\
    , "Itau", "Talanx", "Eastspring", "Swedbank", "Helaba", "MN", "Lyxor", "Lord,"\
    , "Royal", "Zurcher", "Harris", "Henderson", "GAM", "Kohlberg", "Danske", "AMP"\
    , "Achmea", "GE", "Union", "BBVA", "KBC", "Artisan", "Sumitomo", "Investec"\
    , "SURA", "Hartford", "Candriam", "GMO", "Harvest", "Groupama", "Bram", "Covea"\
    , "Oaktree", "BMO", "CIBC", "Vontobel", "Payden", "Ares", "First", "MacKay"\
    , "CBRE", "Barrow", "Conning", "Hines", "PineBridge", "LSV", "Kames", "CI"\
    , "Man", "Mirae", "Mediolanum", "OP", "Anima", "BayernInvest", "OFI", "Metzler"\
    , "Newton", "Mesirow", "Acadian", "CM", "Storebrand", "LBBW", "DNB", "Erste"\
    , "Arrowstreet", "Handelsbanken", "Prologis", "Walter", "BBH", "LaSalle", "William"\
    , "Edmond", "La", "BlueBay", "Irish", "QIC", "Mondrian", "Actiam", "Carmignac"\
    , "Delta", "Warburg", "M", "Rothschild", "Thornburg", "Degroof", "LGT", "Record"\
    , "Marathon", "Jupiter", "Cohen", "Sal", "Brown", "Daiwa", "Hauck", "Partners"\
    , "Oddo", "Caixabank", "Cornerstone", "GCM", "Ashmore", "Tokio", "Lombard"\
    , "CVC", "KLP", "Joh", "Coronation", "THEAM", "Fischer", "Epoch", "CPR", "Stone"\
    , "HarbourVest", "Quilvest", "Schroder", "Columbia", "Principal", "Manulife"\
    , "APG", "Robeco", "Barings", "Dekabank", "Nordea", "Loomis", "Baillie", "Lazard"\
    , "Russell", "Bram", "China", "Nikko", "Bridgewater", "Pictet", "Standish"\
    , "Zurcher", "John", "Talanx", "Helaba", "Eastspring", "Lyxor", "Henderson"\
    , "ClearBridge", "IGM", "Harvest", "Harris", "Conning", "Candriam", "KBC", "Payden"\
    , "Danske", "CIBC", "Groupama", "Sumitomo", "Vontobel", "Hartford", "Covea"\
    , "LSV", "Hines", "Ares", "New", "MacKay", "Galliard", "Mirae", "CI", "Boston"\
    , "Fiera", "CBRE", "Man", "Metzler", "Anima", "BayernInvest", "Acadian", "Mediolanum"\
    , "Arrowstreet", "OFI", "KLP", "Irish", "Mesirow", "CM", "Storebrand", "Prologis"\
    , "LBBW", "Newton", "Brandywine", "William", "Hauck", "La Francaise", "Kames"\
    , "Delta", "Carmignac", "DNB", "Erste", "Edmond", "Handelsbanken", "Mondrian"\
    , "Walter", "LaSalle", "Actiam", "QIC", "Cohen", "Partners", "M", "Rothschild"\
    , "Record", "Colony", "Pavilion", "LGT", "BBH", "Victory", "Degroof", "Tokio"\
    , "CapitaLand", "Brown", "Marathon", "Caixabank", "ASR", "Ashmore", "Sal", "Kempen"\
    , "BlueBay", "Jupiter", "Daiwa", "Thornburg", "GCM", "W", "Starwood", "HarbourVest"\
    , "Oddo", "Pathway", "Lombard", "Clarion", "Old", "Joh", "PanAgora", "Epoch"\
    , "Northill", "CPR", "Coronation", "Tishman", "Hamilton", "THEAM", "The", "Quilvest"\
    , "Harding", "Heitman", "Stone", "Fischer", "Logan", "Hermes", "Fisher", "Colchester"\
    , "CVC", "Pantheon", "Shinhan", "Eagle", "GW", "Arca", "Raiffeisen", "Bentall", "J"\
    , "Artemis", "Gothaer", "Alcentra", "HFT", "Winton", "Adams", "Universal"\
    , "Mirabaud", "VidaCaixa", "Muzinich", "Brandes", "Quoniam", "AEW", "Seix", "Davis"\
    , "Beutel", "AGF", "Genesis", "Axeltis", "Capital", "TKP", "Managed", "Intermediate"\
    , "Comgest", "First", "KGAL", "AEW", "Nykredit", "Kutxabank", "BlueMountain"\
    , "SPF", "Banco", "DNCA", "Unigestion", "EnTrust", "Assenagon", "Patrizia"\
    , "Southeastern", "BankInvest", "Calamos", "Lendlease", "Calamos", "Westwood"\
    , "Jyske", "Tweedy", "Savills", "Royce", "QS", "ValueAct", "Frankfurt", "Allianz"\
    , "Syz", "Majedie", "Yacktman", "TimesSquare", "Landmark", "PAG", "Veritas"\
    , "Brookfield", "Kepler", "Seeyond", "Scor", "Siemens", "Semper", "Highland"\
    , "Martin", "EIG", "CamGestion", "The", "Millennium", "Bankia", "Millennium", "GNB"\
    , "C", "Theodoor", "Sydbank", "Frontier", "Patron", "Alfred", "CQS", "H2O"\
    , "Veritable", "Siguler", "DJE", "Gateway", "HQ", "McDonnell", "BPI", "Evli"\
    , "Vaughan", "EFG", "Sparinvest", "T", "Aktia", "Glenview", "RWC", "Systematica"\
    , "LocalTapiola", "Capital", "DTZ", "Chicago", "Baring", "Pacific", "TwentyFour"\
    , "Pyrford", "KBI", "Skagen", "Fisch", "Arion", "Bantleon", "Maj", "Lupus", "Setanta"\
    , "Maple", "Adrian", "Trilogy", "Bouwinvest", "Edinburgh", "Sparx", "CenterSquare"\
    , "Hayfin", "Kairos", "Foyston", "Ecofi", "IDFC", "Tristan", "Caser", "Rockspring"\
    , "Renta", "Orchard", "Driehaus", "Access", "La", "TOBAM", "Jacobs", "Investa"\
    , "DDJ", "Liontrust", "River", "Cromwell", "Abbott", "Adveq", "Bankia", "Sentinel"\
    , "Sberbank", "Sentinel", "Mirova", "March", "myCIO", "IPM", "Ibercaja", "AlphaSimplex"\
    , "Perennial", "Impax", "LumX", "texas", "california"]

    uniqueKw = list(set(keywords))
    return uniqueKw
