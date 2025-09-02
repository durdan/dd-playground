# Pipeline Examples

This document provides comprehensive examples of different pipeline scenarios, showing complete configurations and expected outputs.

## Table of Contents
- [Simple Feature Development](#simple-feature-development)
- [Bug Fix Pipeline](#bug-fix-pipeline)
- [Security Remediation](#security-remediation)
- [Production Deployment](#production-deployment)
- [Multi-Environment Pipeline](#multi-environment-pipeline)
- [Rollback Scenario](#rollback-scenario)

## Simple Feature Development

### Scenario
A developer creates a new feature branch and pushes code. The pipeline should run tests, build the application, and deploy to a staging environment.

### Configuration (`examples/simple-feature.yml`)