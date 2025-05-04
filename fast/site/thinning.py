def thinning(chooseSite, thinningValue, lmin = -180, lmax = 180, bmin = -90, bmax = 90):
    import numpy as np
    grid_ranges = []

    # 输出每个格网的经纬度范围，并将范围添加到列表中
    for longitude in np.arange(lmin, lmax, thinningValue):
        for latitude in np.arange(bmin, bmax, thinningValue):
            grid = [longitude, longitude + thinningValue, latitude, latitude + thinningValue]
            grid_ranges.append(grid)
    
    outSiteAll = {}
    for s in chooseSite:
        sL = chooseSite[s]['L']
        sB = chooseSite[s]['B']
        for grid_range in grid_ranges:
            if grid_range[0] <= sL <= grid_range[1] and grid_range[2] <= sB <= grid_range[3]:
                index = grid_ranges.index(grid_range)
                if index not in outSiteAll:
                    outSiteAll[index] = {}
                outSiteAll[index][s] = chooseSite[s]

    outSite = {}
    for grid_range in outSiteAll:
        if len(list(outSiteAll[grid_range])) > 0:
            outSite[list(outSiteAll[grid_range])[0]] = outSiteAll[grid_range][list(outSiteAll[grid_range])[-1]]
    
    return outSite
        