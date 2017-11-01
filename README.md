Intro
=====
This fork adds DNS server, which redirects traffic from defined domains into picoweb application. So you do not have to access the webpage using IP Address, but using set of domain names you define. You can see it live on ESP8266 in this [video] (https://www.youtube.com/watch?v=G8uyDuOrvUI)

HOW-TO run
==========
We are assuming you successfuly installed some application using picoweb framework. If you have not, you can try it on [notes-pico]
(https://github.com/pfalcon/notes-pico) example application.

If you want yo use this framework, you have to substitute picoweb/ directory sources with sources from this repository. It is just 3 files inside picoweb directory: \_\_init\_\_.py, utils.py, captivedns.py. Now you can build your app and use it.

Let assume you have built [notes-pico](https://github.com/pfalcon/notes-pico) and picoweb from this repository. Now you can flash the image and start the application as usual:

1. ``import notes_pico.__main__``
2. ``notes_pico.__main__.main(host="0.0.0.0", port=80)``

DNS server is running by default on domain ``esp.device``, so it can be accessed by browser not only on url ``http://192.168.4.1/``, but also on url ``http://esp.device/``. If you want to use custom set of domains, you can use keyword argument ``captive_domains`` when calling ``app.run``. Since ``main`` method in _notes\_pico_ is passing arguments to ``app.run`` we can user the argument in ``main``

2. ``notes_pico.__main__.main(host="0.0.0.0", port=80, captive_domains=['esp.device', 'yourname.yourdomain'])``
