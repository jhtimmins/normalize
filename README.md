# Normalize

### Quickstart

```python
>>> python3 normalize.py << {input_file}
```

### Setup
1. Clone repository (local machine must have Python3 and Pip3 installed).
2. `cd` into the `normalize` directory.
3. Run the following commands:
  ```
  >>> chmod +x setup.sh
  >>> ./setup.sh
  ```
  This will run the setup operations (for a Unix system) automatically. Optionally, you can run the commands in `setup.sh` manually.
  
4. Run the program as described in the `Quickstart` section.

### Notes
There is (at least) one scenario in which my code doesn't satisfy the requirements. If an invalid duration is encountered a warning will be output, but the row will not be skipped. Instead, the duration will default to zero. Solving this would have required enough rework to push me over the designated time limit.
