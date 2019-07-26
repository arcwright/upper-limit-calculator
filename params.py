# INPUT PARAMETERS (Descriptions at the end)
bane_pth= '/home/lijo/.local/bin/BANE' 
srcdir	= '/media/lijo/data/upper-limit-calculator/sources/1046-25'
visname	= '1046-25.GMRT325.SP2B.CAL.RR.MS'
imgname = '1046-25.GMRT325.SP2B.PBCOR.IMAGE'
vispath = os.path.join(srcdir, visname)
imgpath = os.path.join(srcdir, imgname)
# z       = 1.059
cluster = 'RX J1046.8-2535'
z       = float(Ned.query_object(cluster)['Redshift'])
l       = 1000
alpha   = -1.3
ftype	= 'E'

# ESTIMATED PARAMETERS
theta   = (l/cosmo.kpc_proper_per_arcmin(z).value)*60.
x0,y0   = imhead(imgpath)['refpix'][0], imhead(imgpath)['refpix'][1]
cell   	= np.rad2deg(imhead(imgpath)['incr'][1])*3600
hsize   = theta/cell

# FLUX LEVELS
flx_fac = [50, 100, 200, 300, 500, 1000, 2000]

# CLEAN PARAMETERS
N		= 1000000
isize	= imhead(imgpath)['shape'][0]
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

#######################
# bane_pth	= Path to BANE executable
# srcdir	= Source Directory
# visname	= Reference visibility file
# imgname	= Reference image file made from 'visname'
# z 		= Redshift of source
# cluster 	= Cluster name (optional)
# l 		= Size of halo to be injected (kpc)
# alpha 	= Spectral index for frequency scaling (S = k*v^(-a))
# ftype		= Radial profile of halo. Options: (G)aussian, (P)olynomial, (E)xponential
# theta		= Angular size (in arcsec) for halo (size=l) at redshift z
# x0, y0	= Halo injection position
# cell		= Pixel separation (in arcsec)
# hsize		= Size of halo (in pixels)
# flx_fac	= Flux level factors
# N 		= No. of iterations
# csize 	= Cell size
# weight	= Weighting to be used
# dcv		= Deconvolver to use
# scle		= Multi-scale options
# thresh_f	= Cleaning threshold factor
# radius	= Radius of halo (in arcsec)
# rms_reg	= Region from which to estimate rms
# nbeams	= No. of synthesized beams in halo
# bparams	= Beam size (bmaj("), bmin("), bpa(deg))
# smooth_f	= Factor to smooth input beam
# recv_th	= Threshold of Excess flux recovery at which to fine tune
#######################