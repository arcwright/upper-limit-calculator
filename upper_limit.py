'''
Program to create artificial halo into visibility and estimate upper limit to halo flux

NOTE: Currently this program needs visibilities with a single spectral window

--------------------------------------------------------
Main Program
STAGES:
1) Estimate RMS 	: BANE is used to estimate the rms in a defined region of the image.
					  This value will be used to estimate the threshold of cleaning
					  as well as the flux of the halo to be injected.
2) Create Halo 		: Halo image is created at given position based on certain parameters
3) Add to MS file	: Halo image is extrapolated to all BW frequencies, Fourier transformed
					  then added to input visibilities in a new MS file
4) Run CLEAN again	: The CASA task tclean is run on new MS file
5) Convolve 		: Both the original image and the newly created image are convolved.
					  Beam parameters have to be either provided or a certain factor times
					  original beam is taken
--------------------------------------------------------
Changes
=======
2019-07/17 - Added nbeams and finetuning parameters
'''

import os
import sys
import shutil
import subprocess
from astropy.modeling.models import Gaussian2D, Polynomial1D, ExponentialCutoffPowerLaw1D
from astropy.cosmology import Planck15 as cosmo
from astroquery.ned import Ned
import numpy as np

execfile('modules.py')
# execfile('mylogging.py')
# import mylogging

while True:
	clean_task = str(raw_input('Choose CLEAN algorithm to use:\n\
	1. tclean\n\
	2. wsclean\n\n\
Your choice is... '))
	if clean_task not in ('1', 'tclean', '2', 'wsclean'):
		print('No proper option given. Try again...')
		continue
	else:
		break
logger.info('Running upper limit estimator.\n')

img_rms = estimateRMS(imgfile, x0, y0, rms_reg)

# Convolve original image (Set last parameter as either 'factor' OR 'beam')
i1_conv = '.'.join(imgfile.split('.')[:-1]) + '.conv'
logger.info('Convolving and getting statistics for input image:')
i1_conv = myConvolve(imgfile, i1_conv, 'num_of_beams')
i1_stats = getStats(i1_conv, x0, y0, radius)
logger.info('DONE!\n')

thresh = thresh_f * img_rms			# Threshold to CLEAN
flx_list = [f*img_rms for f in flx_fac]  # List of Halo fluxes to be injected

for i, flux in enumerate(flx_list):
    haloimg = createHalo(imgfile, x0, y0, hsize, flux, ftype)
    newvis = addHaloVis(visfile, haloimg, flux, alpha)
    otpt = '.'.join(imgfile.split('.')[:-1]) + '_wHalo_flux_{:f}'.format(flux)
    while True:
        try:
            run_imaging(clean_task, otpt)
            break
        except Exception as e:
            logger.error('Something went wrong. Please try again!')
            sys.exit(1)

    # Convolve new images (Set last parameter as either 'factor' OR 'beam')
    logger.info('\nConvolving new image and getting statistics...')
    if clean_task in ('wsclean', '2'):
        importfits(fitsimage=otpt+'-image.fits', imagename=otpt+'.image')
    i2_conv = otpt + '.conv'
    i2_conv = myConvolve(otpt+'.image', i2_conv, 'num_of_beams')
    i2_stats = getStats(i2_conv, x0, y0, radius)
    logger.info('DONE!\n')

    excessFlux = i2_stats['flux'][0]-i1_stats['flux'][0]
    recovery = (excessFlux/i1_stats['flux'][0]) * 100.
    logger.info('Excess flux in central {:.2f}\' region = {:.2f} mJy'.format(
        theta/60., excessFlux*1.e3))
    logger.info('Halo flux recovered = {:.2f}%'.format(recovery))
    cleanup(srcdir)
    clearcal(vis=visfile)
    clearstat()
    logger.info('----')
    if recovery > recv_th:
    	logger.info('Recovery threshold reached.\nFinetuning now...')
    	break

try:
	new_flx_list = np.linspace(flx_list[i], flx_list[i-1], 6)
	new_flx_list = new_flx_list[1:-1]
except Exception as e:
	logger.error(e)
else:
	new_flx_list = np.arange(flx_list[i], 10)

logger.info('Repeating process for new flux values...\n')
for flux in new_flx_list:
	haloimg = createHalo(imgfile, x0, y0, hsize, flux, ftype)
	newvis = addHaloVis(visfile, haloimg, flux, alpha)
	otpt = '.'.join(imgfile.split('.')[:-1]) + '_wHalo_flux_{:f}'.format(flux)
	while True:
		try:
			run_imaging(clean_task, otpt)
			break
		except Exception as e:
			logger.error('Something went wrong. Please try again!')
			sys.exit(1)

	# Convolve new images (Set last parameter as either 'factor' OR 'beam')
	logger.info('\nConvolving new image and getting statistics...')
	if clean_task in ('wsclean', '2'):
		importfits(fitsimage=otpt+'-image.fits', imagename=otpt+'.image')
	i2_conv = otpt + '.conv'
	i2_conv = myConvolve(otpt+'.image', i2_conv, 'num_of_beams')
	i2_stats = getStats(i2_conv, x0, y0, radius)
	logger.info('DONE!\n')

	excessFlux = i2_stats['flux'][0]-i1_stats['flux'][0]
	recovery = (excessFlux/i1_stats['flux'][0]) * 100.
	logger.info('Excess flux in central {:.2f}\' region = {:.2f} mJy'.format(
		theta/60., excessFlux*1.e3))
	logger.info('Halo flux recovered = {:.2f}%'.format(recovery))
	cleanup(srcdir)
	clearcal(vis=visfile)
	clearstat()
	logger.info('----')
