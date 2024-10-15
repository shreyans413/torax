# Copyright 2024 DeepMind Technologies Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Basic post-run plotting tool. Plot a single run or comparison of two runs.

Includes a time slider. Reads output files with xarray data or legacy h5 data.

Plots are configured by a plot_config module.
"""
import importlib
from absl import app
from absl import logging
from absl.flags import argparse_flags
import matplotlib
from torax.plotting import plotruns_lib


matplotlib.use('TkAgg')


def parse_flags(_):
  """Parse flags for the plotting tool."""
  parser = argparse_flags.ArgumentParser(description='Plot finished run')
  parser.add_argument(
      '--outfile',
      nargs='*',
      help=(
          'Relative location of output files (if two are provided, a'
          ' comparison is done)'
      ),
  )
  parser.add_argument(
      '--plot_config',
      default='torax.plotting.configs.default_plot_config',
      help='Name of the plot config module.',
  )
  return parser.parse_args()


def main(args):
  plot_config_module_path = args.plot_config
  try:
    plot_config_module = importlib.import_module(plot_config_module_path)
    plot_config = plot_config_module.PLOT_CONFIG
  except (ModuleNotFoundError, AttributeError) as e:
    logging.exception(
        'Error loading plot config: %s: %s', plot_config_module_path, e
    )
    raise
  if len(args.outfile) == 1:
    plotruns_lib.plot_run(plot_config, args.outfile[0])
  else:
    plotruns_lib.plot_run(plot_config, args.outfile[0], args.outfile[1])


if __name__ == '__main__':
  app.run(main, flags_parser=parse_flags)
