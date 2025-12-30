def doodson_filter_mat(in_mat_3D_hourly_means):
    # Doodson filter to remove tides from hourly data.
    #
    #  doodson filter on an array of 2d maps, (0th dimension must be time)
    #
    #       Jonathan Tinker 04/07/2019, Met Office Hadley Centre, UK
    #                  jonathan.tinker@metoffice.gov.uk
 
 
 
    # define doodson filter, and size of filter
    doodson_filter =  np.array([1.,0.,1.,0.,0.,1.,0.,1.,1.,0.,2.,0.,1.,1.,0.,2.,1.,1.,2., 0., 2.,1.,1.,2.,0.,1.,1.,0.,2.,0.,1.,1.,0.,1.,0.,0.,1.,0.,1.,], dtype = 'double')/30.
    doodson_size = doodson_filter.size
 
 
    #prepare input and output arrays
    out_mat = np.ma.array(in_mat_3D_hourly_means.copy()*0.)
    out_mat.mask = np.ma.getmaskarray(out_mat)
    out_mat.mask = True
 
    #size of arrays
    outsize = out_mat.shape
    ntime = outsize[0]
 
    # prepare temporary array of correct size
    tmp_outsize = np.array(outsize)
    tmp_outsize[0] = tmp_outsize[0] - doodson_size
    tmp_array = np.ma.zeros(tuple(tmp_outsize))
 
    # vectorised... calculate for each of the 39 doodson filter hours one at a time
    for tmpi,tmpweight in enumerate(doodson_filter): tmp_array += tmpweight*in_mat_3D_hourly_means[tmpi:ntime-doodson_size+tmpi,:,:]
 
    out_mat[doodson_size//2:(ntime - doodson_size//2-1)]= tmp_array
 
 
    return out_mat
 
 
 
def doodson_filter_mat_3_months(prev_file,curr_file,next_file,ncvar = 'sossheig'):
 
    # load the data from the current, next and previous file,
    # for the given netcdf variable name
    # onlu load the last 19 hours, and first 19 hours from the previous
    # and next file
    #
    # Assumes files are hourly data, with 3 dimensions
    #                    (Time being the zeroth dim)
    #
    #       Jonathan Tinker 04/07/2019, Met Office Hadley Centre, UK
    #                  jonathan.tinker@metoffice.gov.uk
 
    rootgrp = Dataset(prev_file,'r')
    ssh_prev = rootgrp.variables[ncvar][-19:,:,:]
    rootgrp.close
    rootgrp = Dataset(curr_file,'r')
    ssh_curr = rootgrp.variables[ncvar][:,:,:]
    rootgrp.close
    rootgrp = Dataset(next_file,'r')
    ssh_next = rootgrp.variables[ncvar][:20,:,:]
    rootgrp.close
 
    # combine the data
    ssh_combmat = np.ma.concatenate((ssh_prev,ssh_curr,ssh_next))
 
 
 
    tmp_ssh_detide = doodson_filter_mat(ssh_combmat)
    ssh_detide = tmp_ssh_detide[19:-20,:,:]
 
    return ssh_detide
