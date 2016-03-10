# uberdashboard-src

For compiling FW clone this repo
Run: 
```
$ git submodule update --init
```

Use gnu arm toolchain for build.
Toolchain must be set in PATH. 
Then take waf and build FW: 
```
$ wget https://waf.io/waf-1.8.17
$ mv waf-1.8.17 waf
$ chmod +x ./waf
$ ./waf configure 
$ ./waf build 
```

Enjoy!
