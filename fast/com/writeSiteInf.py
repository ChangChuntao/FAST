def writeSiteInf(siteInf, siteInfFile):
    siteInfWrite = open(siteInfFile, 'w+')
    for site in siteInf:
        L = siteInf[site]['L']
        B = siteInf[site]['B']
        line = '%15.8f' % L + '%15.8f' % B + '   ' + site + '\n'
        siteInfWrite.write(line)
    siteInfWrite.close()
    
def writeSiteList(siteInf, siteListFile):
    siteListWrite = open(siteListFile, 'w+')
    for site in siteInf:
        line = site + ' '
        siteListWrite.write(line)
    siteListWrite.close()