Description
===========

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

-d

It will show the jsonrpc request and response on the terminal.

Example::

      --> {"id": "21c36a78-f9b1-11ea-bc62-001fc69cc946", "jsonrpc": "2.0", "method": "admin_config_get_records", "params": ["proxy.config.diags.debug.tags"]}
      <-- {"jsonrpc": "2.0", "result": [{...}], "id": "21c36a78-f9b1-11ea-bc62-001fc69cc946"}
    



-r

Repeat the same command N times.

-s

Do not send the message, just show the request message (this can be combined with -f to show pretty json or yaml

-f

Formatting output options
^^^^^^^^^^^^^^^^^^^^^^^^^
        
legacy
""""""

Show output that is similar to traffic_ctl

raw
"""

Show raw messages, if it's json a raw one line json will be shown.

json
""""

Formatted json will be display in the terminal

Example::        
         
   $ tscli -f json config --get proxy.config.diags.debug.tags
     -->
    {
        "id": "69d7033c-f9b2-11ea-852a-001fc69cc946",
        "jsonrpc": "2.0",
        "method": "admin_config_get_records",
        "params": [
            "proxy.config.diags.debug.tags"
        ]
    }
    < --
    {
        "id": "69d7033c-f9b2-11ea-852a-001fc69cc946",
        "jsonrpc": "2.0",
        "result": [
            {
                "access": "0",
                "checktype": "0",
                "current_value": "test_tag",
                "data_type": "STRING",
                "default_value": "http|dns",
                "name": "proxy.config.diags.debug.tags",
                "order": "421",
                "overridable": "no",
                "raw_stat_block": "0",
                "record_class": "1",
                "record_type": "3",
                "source": "1",
                "syntax_check": "null",
                "update_status": "1",
                "update_type": "1",
                "version": "0"
            }
        ]
    }     

yaml
""""

Formatted yaml will be display

Example::


    $ tscli -f yaml config --get proxy.config.diags.debug.tags
    -->
    id: a465e108-f9b2-11ea-a32c-001fc69cc946
    jsonrpc: '2.0'
    method: admin_config_get_records
    params:
    - proxy.config.diags.debug.tags
    
    <--
    id: a465e108-f9b2-11ea-a32c-001fc69cc946
    jsonrpc: '2.0'
    result:
    -   access: '0'
        checktype: '0'
        current_value: test_tag
        data_type: STRING
        default_value: http|dns
        name: proxy.config.diags.debug.tags
        order: '421'
        overridable: 'no'
        raw_stat_block: '0'
        record_class: '1'
        record_type: '3'
        source: '1'
        syntax_check: 'null'
        update_status: '1'
        update_type: '1'
        version: '0'    



pretty
""""""

Custom format will be display

Example::

    $ tscli -f pretty config --describe  proxy.config.diags.debug.tags
    
    ┌ proxy.config.diags.debug.tags
    └┬── Current Value:   test_tag
     ├── Default Value:   http|dns
     ├── Record Type:     STRING
     ├── Access Control:  default
     ├── Update Type:     dynamic, no restart
     ├── Update Status:   1
     ├── Source:          built in default
     ├── Overridable:     no
     ├── Syntax Check:    none
     ├── Version:         0
     ├── Order:           421
     └── Raw Stat Block:  0

ATS commands
------------

