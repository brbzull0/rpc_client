Description
===========
Installation
===============
Dev::

    pip3 install -e . --user
Dependencies
------------
- argparse
- yaml
- json
- colorama

They all will be installed when running pip.


Usage
=====

help::

    tscli --help

::

    usage: tscli [-h] [-v] [-d] [-r [count]] [-s] [-f [{legacy,raw,json,yaml,pretty}]]
                 {data,config,c,host,h,metric,m,plugin,p,server,s,storage,st} ...
    
    Apache Traffic Server RPC TEST tool
    
    optional arguments:
      -h, --help            show this help message and exit
      -v, --version         Show current version
      -d, --verbose         Display raw request and response message
      -r [count], --repeat [count]
                            Repeat the same command N times
      -s, --sim             Show json, don't send the message[not implemented]
      -f [{legacy,raw,json,yaml,pretty}], --formatting [{legacy,raw,json,yaml,pretty}]
                            Output formatting options
    
    Commands:
      Basic interaction command to talk with ATS
    
      {data,config,c,host,h,metric,m,plugin,p,server,s,storage,st}
        data                Accept raw json and yaml as request
        config (c)          Manipulate configuration records
        host (h)            Interact with host status
        metric (m)          Manipulate performance metrics
        plugin (p)          Interact with plugins
        server (s)          Stop, restart and examine the server ????
        storage (st)        Manipulate cache storage

Optional Arguments
------------------

ATS commands
------------

