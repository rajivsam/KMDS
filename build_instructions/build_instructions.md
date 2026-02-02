### Building KMDS
This package is built with ```uv```. Install uv, then run ``` uv build ```

### Updating Documentation
This is the sequence of steps to follow to make changes to the documentation.
1. Clone the repository, change directory to ```docs``` sub-directory.
2. Run ```sphinx-apidoc -o source source/``` to generate the rst
3. Run ```make html``` 
