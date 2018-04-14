# cbake
Simple build tool for the C language, written in Python.

## Features
- Easy-to-write build files using the YAML standard
- Always writes build files to a new folder so that the existing directory structure is not disturbed. 

## Installing
- You can run this package using both Python 2 and 3.
- Install requirements using `pip install -r requirements.txt`
- Create a `virtualenv` if you are just trying this out.
- After creating a `virtualenv`, run `pip install -e .`

## How to use
- After installing this, just run `cbake` in the directory with the [bake file](#the-bake-file). 
- This will create a new directory called `build` which will contain all the output files.

### The Bake file
The build configuration can be simply put in a YAML file named: `.bake.yml`. A sample bake file is shown below:

```yaml
# name of the project
project: project_name

# executables that you want to add, with the C/C++ files
# that you want to add to each executable
executables:
  - first
    - a.h
    - b.c
  - second
    - c.h
    - d.h
```

## TODO
- Add support for compiler flags
- Add support for tests
 
 ## License
```
 MIT License

Copyright (c) 2018 Man Parvesh Singh Randhawa

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```