## class FlipperProto ##

### [Application Calls](flipper_app.py) ###
---

rpc_lock_status()
> Get LockScreen Status

    Returns:
       bool

rpc_app_start(name, args)
> Start/Run application

rpc_app_exit()
> Send exit command to app

rpc_app_load_file(path)
> Send load file command to app

rpc_app_button_press(args)
> Send button press command to app

rpc_app_button_release()
> Send button release command to app

rpc_app_get_error()
> Get extended error info

    Returns:
      Error info as tuple (int, str)

rpc_app_data_exchange_send(data)
> Send user data to application

    Arg:
      data: User data to send as bytes

rpc_app_data_exchange_recv()
> Receive user data from application

    Returns:
      Received user data as bytes


### [GPIO Calls](flipper_gui.py) ###
---

rpc_gpio_get_pin_mode(pin)
> get GPIO pin mode

    Arg:
       pin:  'PC0', 'PC1', 'PC3', 'PB2', 'PB3', 'PA4', 'PA6', 'PA7'

rpc_gpio_set_pin_mode(pin, mode)
> set GPIO pin mode

    Arg:
       pin:  'PC0', 'PC1', 'PC3', 'PB2', 'PB3', 'PA4', 'PA6', 'PA7'
       mode: 'OUTPUT', 'INPUT'

rpc_gpio_write_pin(pin, value)
> write GPIO pin

    Arg:
       pin:  'PC0', 'PC1', 'PC3', 'PB2', 'PB3', 'PA4', 'PA6', 'PA7'
       mode: bool
       
rpc_gpio_read_pin(pin)
> query GPIO pin

    Arg:
       pin:  'PC0', 'PC1', 'PC3', 'PB2', 'PB3', 'PA4', 'PA6', 'PA7'
    Returns:
       bool

rpc_gpio_set_input_pull(pin, pull_mode)
> Set GPIO pill Input

    Arg:
       pin:  'PC0', 'PC1', 'PC3', 'PB2', 'PB3', 'PA4', 'PA6', 'PA7'
       pull_mode :  'NO', 'UP', 'DOWN'
   
  
### [GUI Calls](flipper_gpio.py)  ###
---

rpc_start_virtual_display(data)
> Start Virtual Display

rpc_stop_virtual_display()
> Stop Virtual Display

rpc_gui_start_screen_stream()
> Start screen stream

rpc_gui_snapshot_screen()
> Snapshot screen

    Returns:
       screen data as bytes
  

rpc_gui_send_input_event_request(key, itype)
> Send Input Event Request Key

    Arg:
       key : 'UP', 'DOWN', 'RIGHT', 'LEFT', 'OK'
       itype : 'PRESS', 'RELEASE', 'SHORT', 'LONG', 'REPEAT'
        
 
rpc_gui_send_input(key_arg)
> Send Input Event Request Type

    Arg: tuple (InputKey, InputType)
       InputKeykey values: 'UP', 'DOWN', 'RIGHT', 'LEFT', 'OK'
       InputType values: 'PRESS', 'RELEASE', 'SHORT', 'LONG', 'REPEAT'


### [Storage Calls](flipper_storage.py) ###
---

rpc_backup_create(archive_path)
> Create Backup

rpc_backup_restore(archive_path)
> Backup Restore

rpc_read(path)
> read file from flipperzero device

    Arg:
       path to file
    Returns:
       file data in bytes

rpc_write(path, data)
> write file from flipperzero device

    Arg:
       path to file
       data bytes to write

rpc_info(path)
> get filesystem info

    Arg:
       path to file
    Returns:
       dict containing  'totalSpace' 'freeSpace'
       
rpc_stat(path)
> get info or file or directory file from flipperzero device

    Arg:
       path to file
    Returns
       dict containing: 'name' 'type' 'size'


rpc_md5sum(path)
> get md5 of file

    Arg:
       path to file
    Returns
       md5 checksum of file

rpc_mkdir(path)
> creates a new directory

    Arg:
       path for new directory

rpc_delete(path, recursive)
> delete file or dir

    Arg:
       path to deleted file or directory

rpc_rename_file(old_path, new_path)
> rename file or dir

    Arg:
       old_path to file
       new_path to file

rpc_storage_list(path")
> get file & dir listing

    Arg:
       path to file
    Returns
       list of dict containing: 'name' 'type' 'size'

### [System Calls](flipper_sys.py) ###
---

rpc_factory_reset()
> Factory Reset

rpc_update(update_manifest)
> Update

rpc_reboot(mode)
> Reboot flipper

    Arg:
       mode: 'OS', 'DFU', 'UPDATE'

rpc_power_info()
> Power info / charging status

    Returns
       dict containing: 'key' & 'value'
       
rpc_device_info()
> Device Info

    Returns
       dict containing: 'key' & 'value'

rpc_protobuf_version()
> Protobuf Version

    Returns
       tuple: (major, minor)

rpc_get_datetime()
> Get system Date and Time

    Returns
       dict containing: 'year', 'month', 'day', 'hour', 'minute', 'second', 'weekday'

rpc_set_datetime(arg_datetm)
> Set system Date and Time

    Arg:
       datetime obj (optional)
       default = datetime.datetime.now()

rpc_system_ping(data_bytes)
> Ping flipper

rpc_audiovisual_alert()
> Launch audiovisual alert on flipper ??

rpc_stop_session()
> Stop RPC session


### [Exceptions](flipper_base.py) ###
---

FlipperProtoException<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;RPC Proto return code error


InputTypeException<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Input Type call argument error

Varint32Exception<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Protocal error, reading varint from serial port


-----

See Also:  [flipperdevices/flipperzero-protobuf](http://github.com/flipperdevices/flipperzero-protobuf)

