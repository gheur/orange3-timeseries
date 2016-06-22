#!/usr/bin/env python

import os
import sys
import pkg_resources
from setuptools import setup, find_packages
from setuptools.command.install import install

VERSION = '0.1.0'

ENTRY_POINTS = {
    'orange3.addon': (
        'timeseries = orangecontrib.timeseries',
    ),
    # Entry point used to specify packages containing tutorials accessible
    # from welcome screen. Tutorials are saved Orange Workflows (.ows files).
    'orange.widgets.tutorials': (
        # Syntax: any_text = path.to.package.containing.tutorials
    ),

    # Entry point used to specify packages containing widgets.
    'orange.widgets': (
        # Syntax: category name = path.to.package.containing.widgets
        # Widget category specification can be seen in
        #    orangecontrib/datafusion/widgets/__init__.py
        'Time Series = orangecontrib.timeseries.widgets',
    ),
}


class LinkDatasets(install):
    def run(self):
        super().run()

        old_cwd = os.getcwd()
        os.chdir(os.path.abspath(os.path.sep))

        src = pkg_resources.resource_filename('orangecontrib.timeseries', 'datasets')
        dst = os.path.join(pkg_resources.resource_filename('Orange', 'datasets'), 'timeseries')

        try:
            os.remove(dst)
        except OSError:
            pass
        try:
            os.symlink(src, dst, target_is_directory=True)
        except OSError:
            pass
        finally:
            os.chdir(old_cwd)



if __name__ == '__main__':
    setup(
        name="Orange3-Timeseries",
        description="Orange add-on for exploring time series and sequential data.",
        version=VERSION,
        author='Bioinformatics Laboratory, FRI UL',
        author_email='info@biolab.si',
        url='https://github.com/biolab/orange3-timeseries',
        keywords=(
            'time series',
            'sequence analysis',
            'orange3 add-on',
            'ARIMA',
            'VAR model',
            'forecast'
        ),
        cmdclass={'install': LinkDatasets},
        packages=find_packages(),
        package_data={
            "orangecontrib.timeseries.widgets": ["icons/*.svg"],
            "orangecontrib.timeseries": ["datasets/*.tab",
                                         "datasets/*.csv"],
        },
        install_requires=[
            'Orange3',
            'statsmodels>=0.6.1',
            'numpy',
            'scipy',
            'pyqtgraph'
        ],
        entry_points=ENTRY_POINTS,
        namespace_packages=['orangecontrib'],
        zip_safe=False,
    )
