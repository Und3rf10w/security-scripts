# Installation
See [this page](https://developers.google.com/api-client-library/python/start/installation#system-requirements) for instructions on how to install the Google client library

# Requirements
You need to create a Google Developer API Key. Register [here](https://console.developers.google.com/) and create a new project.

You'll also need to create a Google Custom Search Engine. Register [here](https://cse.google.com/cse/all).

# Configuration
Copy [config.exmpl.cfg](config.exmpl.cfg) to ```config.cfg```:

```
cp config.{exmpl,}.cfg
```

Insert your Google Developer API key into ```config.cfg```, replacing ```<GOOGLE DEVELOPER KEY>``` with it.
Finally, insert your Google Custom Search Engine key into ```config.cfg```, replacing ```<GOOGLE CUSTOM SEARCH ENGINE KEY>``` with it.

# Usage

```
usage: ./org2linkedin.py [options]

Google Linkedin Scraper to enumerate current employees at a given organization
with publicly available Linkedin profiles

optional arguments:
  -h, --help            show this help message and exit
  -n NORESULTS          Number of results from Google
  -o ORGNAME            Name of organization to search for
  --dev-key DEVELOPER_KEY
                        Your Google Developer Key
  --cx-key CX_KEY       Your Google Custom Search Engine key
  -v, --verbose         Verbose output
  -d, --debug           Debugging output (implies -v)
```

# Issues
Should any issues arise with this, please run the script with the ```-d``` flag, and provide any output in the comments of a new issue you open through Github.
