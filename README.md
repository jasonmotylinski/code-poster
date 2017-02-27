# Code Poster
Code Poster generates an SVG image from a source image using text taken from code files in a github repository. 

This project is inspired by the Elixir project by Pete Corey. Pete did much of the hard work like determining the optimal image size and how to adjust the image to correct for the font width. Read his post [here](http://www.east5th.co/blog/2017/02/13/build-your-own-code-poster-with-elixir/) and see the elixir code [here](https://github.com/pcorey/elixir_poster).

This version automatically scales the image by a configured ratio so that any image can be used without modification.

## Setup
### Install the Source Code Pro Font
Download and unzip the [latest release](https://github.com/adobe-fonts/source-code-pro/releases) of the Adobe fonts. 

#### OSX instructions
1. Open `Font Book`
1. Select `File -> Add Fonts`
1. Navigate to the unzipped directory, open the `TFF` directory, and select all the `SourceCodePro-*.tff` files. 

### Set up Python Environment
The following commands will create a virtual envrionment, activate it, and install the project's requirements.

```
virtualenv venv
source venv/bin/activate
pip install -r requirements
```

### Configuration
The configuration file defines the options for retrieving the source code from GitHub and SVG options. 

**YOU MUST** copy the `config.yml.EXAMPLE` file to `config.yml` before running the application.

#### General
```
general:
  source: <local OR github>
  code_file_regex: '^.*\.(scala|js|py|cs|java|rb)$'
```
| Option | Description |
|---|---|
|source|Which source to use for the code, local or github|
|code\_file\_regex|The regular expression used to determine which files in GitHub to use for the source code. By default the expression scans .scala, .js, .py, .cs, and .java files.
 
#### Local
```
local:
  path: <PATH TO THE LOCAL FILES>
```
| Option | Description |
|---|---|
|path| The local file path to the code files used to build the image |

#### GitHub
```
github:
  api_url: https://api.github.com
  username: <OPTIONAL>
  personal_access_token: <OPTIONAL>
  owner: unitedstates
  repo: congress-legislators
  branch: master
```
| Option | Description |
|---|---|
|api_url| The GitHub API URL. Can be changed to use Github Enterprise API v3 |
|username| The username to make GitHub API calls as. This is REQUIRED if using public GitHub, optional if using GitHub Enterprise. Remove from config file if not used.|
|personal\_access\_token| The personal access token to make GitHub API calls with. This is REQUIRED if using public GitHub, optional if using GitHub Enterprise. Remove from config file if not used.|
|owner|The owner of the repository to use|
|repo| The name of the repo to use|
|branch| The branch of code to use | 
|code\_file\_regex|The regular expression used to determine which files in GitHub to use for the source code. By default the expression scans .scala, .js, .py, .cs, and .java files.
 
#### SVG
```
svg:
  font_family: 'Source Code Pro'
  font_size: 1
  ratio: 0.6
```
| Option | Description |
|---|---|
|font_family| The font to use to generate the SVG|
|font_size| The size of the font|
|ratio|The amount of compensation to make with widths because the font is not exactly 1 pixel wide. Adjust with caution|


## Running
Before running make sure you have the following:

1. A source image to use
1. A GitHub repository configured in the `config.yml` file.

Run the following command:

```
python svg.py -i logo.png -o code.svg
```

## Github Example
The GitHub example will download a version of the GitHub logo and create an SVG using the code in the [platform-samples](https://github.com/github/platform-samples) repository. 

To run the Github example do the following:

1. Copy `examples/github/config.yml.EXAMPLE` to `config.yml`
1. Update the `[github]` section with the appropriate username and personal\_access\_token
1. Run the command `./examples/github/run.sh` 