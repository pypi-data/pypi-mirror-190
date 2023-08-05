from setuptools import setup, find_packages

VERSION = '0.0.4' 
DESCRIPTION = 'urm_validatetoken package contains method validate_token() which takes access_token as input and returns status of the token as valid or invalid.'
LONG_DESCRIPTION = 'Method validate_token() takes four required parameters and returns two values.\\ syntax: <TOKEN_VALIDATION_STATUS>, <TOKEN_STATUS> = urm_validatetoken.validate_token(<REQUEST_METHOD>,<VALIDATE_TOKEN_URL>,<ACCESS_TOKEN>,<CONTENT_TYPE>).\\ <REQUEST_METHOD>: POST, PUT, GET, PATCH, etc.\ <VALIDATE_TOKEN_URL>: url of validate_token api.\ <ACCESS_TOKEN>: unique access token for authorization.\ <CONTENT_TYPE>: for ex. application/json.\ <TOKEN_VALIDATION_STATUS>: validation status description.\ <TOKEN_STATUS>: it may contain value True or False or status_code(403 or 401).'

# Setting up
setup(
        name="urm_validatetoken", 
        version=VERSION,
        author="Shubham Nalawade",
        author_email="s.satish.nalawade@accenture.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type="text/markdown",
        packages=find_packages(),
        install_requires=["urllib3>=1.26.12"], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)