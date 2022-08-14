## class FlipperProto ##

### [Application Calls](flipper_app.py) ###
---

cmd_lock_status()
> Get LockScreen Status

    Returns:
       bool

cmd_app_start(name, args)
> Start/Run application

cmd_app_exit()
> Send exit command to app

cmd_app_load_file(path)
> Send load file command to app

cmd_app_button_press(args)
> Send button press command to app

cmd_app_button_release()
> Send button release command to app


### [GPIO Calls](flipper_gui.py) ###
---

cmd_gpio_get_pin_mode(pin)
> get GPIO pin mode

    Arg:
       pin:  'PC0', 'PC1', 'PC3', 'PB2', 'PB3', 'PA4', 'PA6', 'PA7'

cmd_gpio_set_pin_mode(pin, mode)
> set GPIO pin mode

    Arg:
       pin:  'PC0', 'PC1', 'PC3', 'PB2', 'PB3', 'PA4', 'PA6', 'PA7'
       mode: 'OUTPUT', 'INPUT'

cmd_gpio_write_pin(pin, value)
> write GPIO pin

    Arg:
       pin:  'PC0', 'PC1', 'PC3', 'PB2', 'PB3', 'PA4', 'PA6', 'PA7'
       mode: bool
       
cmd_gpio_read_pin(pin)
> query GPIO pin

    Arg:
       pin:  'PC0', 'PC1', 'PC3', 'PB2', 'PB3', 'PA4', 'PA6', 'PA7'
    Returns:
       bool

cmd_gpio_set_input_pull(pin, pull_mode)
> Set GPIO pill Input

    Arg:
       pin:  'PC0', 'PC1', 'PC3', 'PB2', 'PB3', 'PA4', 'PA6', 'PA7'
       pull_mode :  'NO', 'UP', 'DOWN'
   
  
### [GUI Calls](flipper_gpio.py)  ###
---

cmd_start_virtual_display(data)
> Start Virtual Display

cmd_stop_virtual_display()
> Stop Virtual Display

cmd_gui_start_screen_stream()
> Start screen stream

cmd_gui_snapshot_screen()
> Snapshot screen

    Returns:
       screen data as bytes
  

**cmd_gui_send_input_event_request(key, itype)**
> Send Input Event Request Key

    Arg:
       key : 'UP', 'DOWN', 'RIGHT', 'LEFT', 'OK'
       itype : 'PRESS', 'RELEASE', 'SHORT', 'LONG', 'REPEAT'
        
 
**cmd_gui_send_input(key_arg)**
> Send Input Event Request Type

    Arg: tuple (InputKey, InputType)
       InputKeykey values: 'UP', 'DOWN', 'RIGHT', 'LEFT', 'OK'
       InputType values: 'PRESS', 'RELEASE', 'SHORT', 'LONG', 'REPEAT'


### [Storage Calls](flipper_storage.py) ###
---

cmd_backup_create(archive_path)
> Create Backup

cmd_backup_restore(archive_path)
> Backup Restore

cmd_read(path)
> read file from flipperzero device

    Arg:
       path to file
    Returns:
       file data in bytes

cmd_write(path, data)
> write file from flipperzero device

    Arg:
       path to file
       data bytes to write

cmd_info(path)
> get filesystem info

    Arg:
       path to file
    Returns:
       dict containing  'totalSpace' 'freeSpace'
       
cmd_stat(path)
> get info or file or directory file from flipperzero device

    Arg:
       path to file
    Returns
       dict containing: 'name' 'type' 'size'


cmd_md5sum(path)
> get md5 of file

    Arg:
       path to file
    Returns
       md5 checksum of file

cmd_mkdir(path)
> creates a new directory

    Arg:
       path for new directory

cmd_delete(path, recursive)
> delete file or dir

    Arg:
       path to deleted file or directory

cmd_rename_file(old_path, new_path)
> rename file or dir

    Arg:
       old_path to file
       new_path to file

cmd_storage_list(path")
> get file & dir listing

    Arg:
       path to file
    Returns
       list of dict containing: 'name' 'type' 'size'

### [System Calls](flipper_sys.py) ###
---

cmd_factory_reset()
> Factory Reset

cmd_update(update_manifest)
> Update

cmd_reboot(mode)
> Reboot flipper

    Arg:
       mode: 'OS', 'DFU', 'UPDATE'

cmd_power_info()
> Power info / charging status

    Returns
       dict containing: 'key' & 'value'
       
cmd_device_info()
> Device Info

    Returns
       dict containing: 'key' & 'value'

cmd_protobuf_version()
> Protobuf Version

    Returns
       tuple: (major, minor)

cmd_get_datetime()
> Get system Date and Time

    Returns
       dict containing: 'year', 'month', 'day', 'hour', 'minute', 'second', 'weekday'

cmd_set_datetime(arg_datetm)
> Set system Date and Time

    Arg:
       datetime obj (optional)
       default = datetime.datetime.now()

cmd_system_ping(data_bytes)
> Ping flipper

cmd_audiovisual_alert()
> Launch audiovisual alert on flipper ??

cmd_stop_session()
> Stop RPC session

-----

See Also:  [flipperdevices/flipperzero-protobuf](http://github.com/flipperdevices/flipperzero-protobuf)

