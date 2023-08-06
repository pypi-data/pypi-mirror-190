from pathlib import Path

DOCS = "https://PKGNAME.readthedocs.io/en/latest/"
GIT_URL = "https://github.com/SouthGreenPlatform/PKGNAME"

INSTALL_PATH = Path(__file__).resolve().parent
SINGULARITY_URL_FILES = [('https://itrop.ird.fr/culebront_utilities/singularity_build/Singularity.culebront_tools.sif',
                          f'{INSTALL_PATH}/containers/Singularity.culebront_tools.sif'),
                         ('https://itrop.ird.fr/culebront_utilities/singularity_build/Singularity.report.sif',
                          f'{INSTALL_PATH}/containers/Singularity.report.sif')
                         ]

DATATEST_URL_FILES = ("Data-Xoo-sub.zip", "https://itrop.ird.fr/culebront_utilities/Data-Xoo-sub.zip")



