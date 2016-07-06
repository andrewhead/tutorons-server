# Connections to Java libraries

At the time this, a lot of the best utilities for natural language generation and processing is written in Java.
This module is our attempt to make the functionality of powerful Java packages easily accessible to Tutorons code.

The `py4j.py` script creates a gateway that can connect to any JAR in the root `deps` directory of this project.
For every JAR that we want to connect to, we will make a new Python that uses the gateway from `py4j.py` to import the relevant classes we want to access from the JAR to a scope from which other Python scripts in this project can import.
For an examples, see the `simplenlg.py` script.
