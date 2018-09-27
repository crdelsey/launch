# Copyright 2018 Open Source Robotics Foundation, Inc.
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

"""Module for the LaunchLogger class."""

import datetime
import logging
import os
import socket
import sys

from typing import Optional
from typing import Text


class LaunchLogger:
    """
    Logging interface for launch and processes started by launch.

    This class enables:

    - Configuring logging to screen, to a log file, or both, for each process.
    - Setting verbosity levels for logs sent to the screen and log file independently.
    - Configuring the location of the log file on disk.

    This class is a singleton. The default verbosity level and log directory can be
    configured with the first call to the constructor. Subsequent calls will not update
    the default verbosity level or log directory.
    """

    class __LaunchLogger:

        def __init__(self, *, level, log_dir):
            # Set the default verbosity level. This can be overridden in configure_logger().
            logging.root.setLevel(level)

            # Generate log filename
            # TODO(jacobperron): Check if filename already exists.
            #                    If so, either add counter or try generating datetime string again
            datetime_str = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')
            log_basename = '{0}-{1}-{2}.log'.format(
                datetime_str,
                socket.gethostname(),
                os.getpid(),
            )
            self.log_filename = os.path.join(log_dir, log_basename)
            # Make sure directory exists
            os.makedirs(os.path.dirname(self.log_filename), exist_ok=True)

            # Establish log format
            # TODO(jacobperron): Add fixed padding to 'created' time
            self.__formatter = logging.Formatter(
                '{created} [{levelname}] [{name}] {msg}',
                style='{',
            )

            # Create handlers for the log file and screen
            self.file_handler = logging.FileHandler(self.log_filename)
            self.file_handler.setFormatter(self.__formatter)
            # TODO(jacobperron): Support streaming to stderr, maybe with Filters?
            self.stdout_handler = logging.StreamHandler(sys.stdout)
            # self.__stderr_handler = logging.StreamHandler(sys.stderr)
            self.stdout_handler.setFormatter(self.__formatter)
            # self.__stderr_handler.setFormatter(self.__formatter)

        def configure_logger(self, name: Text, output: Text, level: Optional[int] = None):
            """Configure the output and verbosity level for a process by name."""
            allowed_output_options = ['screen', 'log', 'both']
            if output not in allowed_output_options:
                raise ValueError(
                    "output argument to ExecuteProcess is '{}', expected one of [{}]".format(
                        output,
                        allowed_output_options,
                    )
                )
            logger = logging.getLogger(name)

            if level is not None:
                logger.setLevel(level)

            if 'log' == output or 'both' == output:
                logger.addHandler(self.file_handler)
            if 'screen' == output or 'both' == output:
                logger.addHandler(self.stdout_handler)

        def debug(self, name: Text, message: Text) -> None:
            """
            Log a debug message for a process or module.

            :param: name of the process or module.
            :param: message to log.
            """
            logging.getLogger(name).debug(message)

        def error(self, name: Text, message: Text) -> None:
            """
            Log an error message for a process or module.

            :param: name of the process or module.
            :param: message to log.
            """
            logging.getLogger(name).error(message)

        def info(self, name: Text, message: Text) -> None:
            """
            Log an info message for a process or module.

            :param: name of the process or module.
            :param: message to log.
            """
            logging.getLogger(name).info(message)

        def warn(self, name: Text, message: Text) -> None:
            """
            Log a warning message for a process or module.

            :param: name of the process or module.
            :param: message to log.
            """
            logging.getLogger(name).warn(message)

        def shutdown(self) -> None:
            """Perform an orderly shutdown, flushing and closing all handlers."""
            logging.shutdown()

    # Singleton instance
    instance = None

    def __init__(
        self,
        *,
        level: int = logging.INFO,
        log_dir: Text = os.path.join(os.path.expanduser('~'), '.ros/log')
    ):
        """
        Constructor.

        :param: level is the default verbosity level for logging if not specified for
            an individual process.
        :param: log_dir is where the launch log file will be created.
        """
        if LaunchLogger.instance is None:
            LaunchLogger.instance = LaunchLogger.__LaunchLogger(level=level, log_dir=log_dir)

    def __getattr__(self, name):
        return getattr(LaunchLogger.instance, name)
