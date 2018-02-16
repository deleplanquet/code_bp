
















stack = np.zeros((nbr_sfaults, len(lst_fch), length_t))
for station in lst_fch:
    os.chdir(path_data)
    st = read(station)
    tstart = st[0].stats.starttime
    env_norm = norm1(st[0].data)
    t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
    f = interpolate.interp1d(t, env_norm)
    fmax = 0
    for it in t:
        if f(it) > fmax:
            fmax = f(it)

    ista = lst_fch.index(station)

    for ix in range(nbr_sfaults):
        for it in range(length_t):
            tshift = travt[ista][ix] - (st[0].stats.starttime - t_origin_rupt) + dict_ve_used[st[0].stats.station] - 5 + it/samp_rate
            if tshift > 0 and tshift < t[-1]:
                if (it > <) and (ix > < (it)) and (f(tshift) > 0.1*fmax):
                    stack[ix, ista, it] = 0.1 * f.max
                else:
                    stack[ix, ista, it] = f(tshift)



















