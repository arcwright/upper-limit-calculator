# INPUT PARAMETERS
bane_pth= '/home/lijo/.local/bin/BANE'						# Path to BANE executable
srcdir	= '/media/lijo/data/upper_limit_calculator/sources/PLCKG200/'	# Source Directory
visfile = srcdir + '/' + 'PLCK200_610_APCALUVDATA.MS'   				# Reference visibility file
imgfile = srcdir + '/' + 'PLCK200_610_APCALUVDATA_i10000.image' 			# Reference image file made from 'vis'
# z       = 1.059
cluster = 'PLCK G200.9-28.2'								# Cluster name (optional)
z       = float(Ned.query_object(cluster)['Redshift'])	# Redshift of source
l       = 1000      										# Size of halo to be injected (kpc)
alpha   = -1.3       										# Spectral index for frequency scaling (S = k*v^(-a))
ftype	= 'E'												# Radial profile of halo. Options: (G)aussian, (P)olynomial, (E)xponential

# ESTIMATED PARAMETERS
theta   = (l/cosmo.kpc_proper_per_arcmin(z).value)*60.		# Angular size (in arcsec) for halo (size=l) at redshift z
x0,y0   = imhead(imgfile)['refpix'][0], imhead(imgfile)['refpix'][1] # Halo injection position
cell   	= np.rad2deg(imhead(imgfile)['incr'][1])*3600		# Pixel separation (in arcsec)
hsize   = theta/cell										# Size of halo (in pixels)

# FLUX LEVELS
flx_fac = [50, 100, 200, 300, 500, 1000, 2000]

# CLEAN PARAMETERS
N		= 1000000
isize	= imhead(imgfile)['shape'][0]
csize	= str(cell) + 'arcsec'
weight	= 'briggs'
rbst	= 0.0
grdr	= 'widefield'
wproj	= -1
dcv 	= 'multiscale'
scle	= [0,5,15,30]
thresh_f= 3

# REGION SIZE (in arcsec)
radius	= theta/2.
rms_reg	= 3 * radius

# SMOOTH PARAMETERS
nbeams	= 100
bparams	= (25.0, 25.0, 0.0)
smooth_f= 4

# RECOVERY PARAMETERS
recv_th = 10.0