#!/bin/bash
pytest --cov-report html --cov=opv_directorymanager --cov-config .conf_coverage.conf .
