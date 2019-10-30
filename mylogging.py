import logging
import datetime

execfile('params.py')

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logger = logging.getLogger()
now = datetime.datetime.now()
t = now.strftime("%Y%m%d-%H%M%S")
logname = 'ulc-{}-{}.log'.format(srcdir.split('/')[-1], t)

logging.basicConfig(
	filename= os.path.join(srcdir, logname),
	level=logging.DEBUG,
	format="%(asctime)s - %(name)s - %(message)s",
	datefmt='%m/%d/%Y %I:%M:%S %p',
	)

# set up logging to console
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter('%(process)d:[%(levelname)s]: %(message)s')
console.setFormatter(formatter)
# add the handler to the logger
logger.addHandler(console)
