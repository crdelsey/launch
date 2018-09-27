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

"""Tests for the Launchlogger class."""

import tempfile

from launch import LaunchLogger


def test_launch_logger_constructors():
    """Test the constructors for the LaunchLogger class."""
    LaunchLogger(level=100, log_dir=tempfile.gettempdir())
    LaunchLogger(level=50)
    LaunchLogger()


def test_launch_logger_configure_logger_output():
    """Test the configure_logger() methods output option for the LaunchLogger class."""
    # TODO(jacobperron): Add tests for logging to screen, file, and both.
    pass


def test_launch_logger_configure_logger_level():
    """Test the configure_logger() methods level option for the LaunchLogger class."""
    # TODO(jacobperron): Add tests for different levels of logging.
    pass


def test_launch_logger_shutdown():
    """Test the shutdown() method for the LaunchLogger class."""
    logger = LaunchLogger()
    logger.shutdown()
