# Test functions for the different stellar evolution and atmosphere models
import time
import pdb

def test_evolution_models():
    """
    Test to make sure the different evolution models work
    """
    from spisea import evolution

    # Age ranges to test
    age_young_arr = [6.7, 7.9]
    age_all_arr = [6.7, 8.0, 9.7]

    # Metallicity ranges to test (if applicable)
    metal_range = [-2.5, 0, 0.4]
    metal_solar = [0]

    # Array of evolution models to test
    evo_models = [evolution.MISTv1(version=1.2), evolution.MergedBaraffePisaEkstromParsec(), evolution.MergedSiessGenevaPadova(),
                      evolution.Parsec(), evolution.Baraffe15(), evolution.Ekstrom12(), evolution.Pisa()]

    
    # Array of age_ranges for the specific evolution models to test
    age_vals = [age_all_arr, age_all_arr, age_all_arr, age_all_arr, age_young_arr, age_young_arr, age_young_arr]

    # Array of metallicities for the specific evolution models to test
    metal_vals = [metal_range, metal_solar, metal_solar, metal_solar, metal_solar, metal_solar, metal_solar]

    assert len(evo_models) == len(age_vals) == len(metal_vals)

    # Loop through models, testing if them work
    for ii in range(len(evo_models)):
        evo = evo_models[ii]

        # Loop through metallicities
        for jj in metal_vals[ii]:
            # Loop through ages
            for kk in age_vals[ii]:
                try:
                    test = evo.isochrone(age=10**kk, metallicity=jj)
                except:
                    raise Exception('EVO TEST FAILED: {0}, age = {1}, metal = {2}'.format(evo, kk, jj))

        print('Done {0}'.format(evo))
        
    return

def test_atmosphere_models():
    """
    Test the rebinned atmosphere models used for synthetic photometry
    """
    from spisea import atmospheres as atm

    # Array of atmospheres
    atm_arr = [atm.get_merged_atmosphere, atm.get_castelli_atmosphere, atm.get_phoenixv16_atmosphere, atm.get_BTSettl_2015_atmosphere,
                   atm.get_BTSettl_atmosphere, atm.get_kurucz_atmosphere, atm.get_phoenix_atmosphere, atm.get_wdKoester_atmosphere]

    # Array of metallicities
    metals_range = [-2.0, 0, 0.15]
    metals_solar = [0]
    metals_arr = [metals_solar, metals_range, metals_range, metals_solar, metals_range, metals_range, metals_range, metals_solar]

    assert len(atm_arr) == len(metals_arr)

    # Loop through models, testing if them work
    for ii in range(len(atm_arr)):
        atm_func = atm_arr[ii]

        # Loop through metallicities
        for jj in metals_arr[ii]:
            try:
                test = atm_func(metallicity=jj)
            except:
                raise Exception('ATM TEST FAILED: {0}, metal = {1}'.format(atm_func, jj))
                
        print('Done {0}'.format(atm_func))
        
    # Test get_merged_atmospheres at different temps
    temp_range = [2000, 3500, 4000, 5250, 6000, 12000]
    atm_func = atm.get_merged_atmosphere
    for ii in metals_range:
        for jj in temp_range:
            try:
                test = atm_func(metallicity=ii, temperature=jj, verbose=True)
            except:
                raise Exception('ATM TEST FAILED: {0}, metal = {1}, temp = {2}'.format(atm_func, ii, jj))


    print('get_merged_atmosphere: all temps/metallicities passed')
    
    # Test get_bb_atmosphere at different temps
    # This func only requests temp
    temp_range = [2000, 3500, 4000, 5250, 6000, 12000]
    atm_func = atm.get_bb_atmosphere
    for jj in temp_range:
        try:
            test = atm_func(temperature=jj, verbose=True)
        except:
            raise Exception('ATM TEST FAILED: {0}, temp = {2}'.format(atm_func, jj))
    
    print('get_bb_atmosphere: all temps passed')
    
    return

def test_filters():
    """
    Test to make sure all of the filters work as expected
    """
    from spisea import synthetic

    # Define vega spectrum
    vega = synthetic.Vega()
    
    # Filter list to test
    filt_list = ['wfc3,ir,f127m','acs,wfc1,f814w',
                     '2mass,J', '2mass,H','2mass,Ks',
                     'ctio_osiris,K', 'ctio_osiris,H',
                     'ubv,U', 'ubv,B', 'ubv,V', 'ubv,R',
                     'ubv,I', 'jg,J', 'jg,H', 'jg,K',
                     'decam,y', 'decam,i', 'decam,z',
                     'decam,u', 'decam,g', 'decam,r',
                     'gaia,dr2_rev,G', 'gaia,dr2_rev,Gbp', 'gaia,dr2_rev,Grp',
                     'jwst,F070W', 'jwst,F090W', 'jwst,F115W', 'jwst,F140M',
                     'jwst,F150W', 'jwst,F150W2', 'jwst,F162M', 'jwst,F164N',
                     'jwst,F182M', 'jwst,F187N', 'jwst,F200W', 'jwst,F212N',
                     'jwst,F210M','jwst,F250M', 'jwst,F277W', 'jwst,F300M',
                     'jwst,F322W2', 'jwst,F323N', 'jwst,F335M', 'jwst,F356W',
                     'jwst,F360M', 'jwst,F405N', 'jwst,F410M', 'jwst,F430M',
                     'jwst,F444W', 'jwst,F460M', 'jwst,F466N', 'jwst,F470N',
                     'jwst,F480M', 'naco,J', 'naco,H', 'naco,Ks',
                     'nirc1,K', 'nirc1,H', 'nirc2,J', 'nirc2,H',
                     'nirc2,Kp', 'nirc2,K', 'nirc2,Lp', 'nirc2,Hcont',
                     'nirc2,FeII', 'nirc2,Brgamma', 'ps1,z',
                     'ps1,g', 'ps1,r','ps1,i', 'ps1,y',
                     'ukirt,J', 'ukirt,H', 'ukirt,K',
                     'vista,Y', 'vista,Z', 'vista,J',
                     'vista,H',  'vista,Ks', 'ztf,g', 'ztf,r', 'ztf,i',
                     'hawki,J', 'hawki,H', 'hawki,Ks']

    # Loop through filters to test that they work: get_filter_info
    for ii in filt_list:
        try:
            filt = synthetic.get_filter_info(ii, rebin=True, vega=vega)
        except:
            raise Exception('get_filter_info TEST FAILED for {0}'.format(ii))

    print('get_filter_info pass')
    
    # Loop through filters to test that they work: get_obs_str
    for ii in filt_list:
        try:
            # Test going from col_name to obs_str
            col_name = synthetic.get_filter_col_name(ii)
            obs_str = synthetic.get_obs_str('m_{0}'.format(col_name))
            # Does the obs_str work?
            filt_info = synthetic.get_filter_info(obs_str)
        except:
            raise Exception('get_obs_str TEST FAILED for {0}'.format(ii)) 
            
    print('get_obs_str pass')
    print('Filters done')

    return

def test_Baraffe15_update():
    """
    Make sure expanded age/mass ranges of Baraffe15
    models are working
    """
    from spisea import synthetic as syn
    from spisea import reddening, evolution, atmospheres
    from spisea.imf import imf, multiplicity
    import numpy as np
    
    # Define cluster parameters
    logAge = 5.8
    AKs = 2.4
    distance = 4000
    cluster_mass = 10**5.
    mass_sampling=1

    # Test filters
    filt_list = ['nirc2,J', 'nirc2,Kp']

    startTime = time.time()
    
    evo = evolution.Baraffe15()
    atm_func = atmospheres.get_merged_atmosphere

    red_law = reddening.RedLawNishiyama09()
    
    iso = syn.IsochronePhot(logAge, AKs, distance,
                            evo_model=evo, atm_func=atm_func,
                            red_law=red_law, filters=filt_list,
                            mass_sampling=mass_sampling)

    print('Constructed isochrone: %d seconds' % (time.time() - startTime))

    # Now to create the cluster.
    imf_mass_limits = np.array([0.01, 0.5, 1, np.inf])
    imf_powers = np.array([-1.3, -2.3, -2.3])

    ##########
    # Start without multiplicity
    ##########
    my_imf1 = imf.IMF_broken_powerlaw(imf_mass_limits, imf_powers,
                                      multiplicity=None)
    print('Constructed IMF: %d seconds' % (time.time() - startTime))
    
    cluster1 = syn.ResolvedCluster(iso, my_imf1, cluster_mass)
    clust1 = cluster1.star_systems
    print('Constructed cluster: %d seconds' % (time.time() - startTime))

    # Let's make sure M = 0.01 Msun stars are in table, and that it
    # reaches ~1.4 Msun
    assert np.isclose(0.01, np.min(clust1['mass']), 0.02)
    assert np.isclose(1.4, np.max(clust1['mass']), 0.1)

    ##########
    # Test with multiplicity
    ##########
    multi = multiplicity.MultiplicityUnresolved()
    my_imf2 = imf.IMF_broken_powerlaw(imf_mass_limits, imf_powers,
                                      multiplicity=multi)
    print('Constructed IMF with multiples: %d seconds' % (time.time() - startTime))
    
    cluster2 = syn.ResolvedCluster(iso, my_imf2, cluster_mass)
    clust2 = cluster2.star_systems
    print('Constructed cluster with multiples: %d seconds' % (time.time() - startTime))

    assert len(clust2) > 0
    assert len(cluster2.companions) > 0
    assert np.sum(clust2['N_companions']) == len(cluster2.companions)

    # Let's make sure M = 0.01 Msun stars are in table, and that it
    # reaches ~1.4 Msun
    assert np.isclose(0.01, np.min(clust2['mass']), 0.02)
    assert np.isclose(1.4, np.max(clust2['mass']), 0.1)

    return
