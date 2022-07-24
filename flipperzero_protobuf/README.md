## class FlipperProto ##

### [Application Calls](flipper_app.py) ###
---

cmd_LockStatus()
> Get LockScreen Status

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

cmd_gpio_set_pin_mode(pin, mode)
> set GPIO pin mode

cmd_gpio_write_pin(pin, value)
> write GPIO pin

cmd_gpio_read_pin(pin)
> query GPIO pin

cmd_gpio_set_input_pull(pin, pull_mode)
> Set GPIO pill Input

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

cmd_gui_send_input_event_request(key, itype)
> Send Input Event Request Key

cmd_gui_send_input(key_arg)
> Send Input Event Request Type

### [Storage Calls](flipper_storage.py) ###
---

cmd_BackupCreate(archive_path)
> Create Backup

cmd_BackupRestore(archive_path)
> Backup Restore

cmd_read(path)
> read file from flipperzero device

cmd_write(path, data)
> write file from flipperzero device

cmd_info(path)
> get filesystem info

cmd_stat(path)
> get info or file or directory file from flipperzero device

cmd_md5sum(path)
> get md5 of file

cmd_mkdir(path)
> creates a new directory

cmd_delete(path, recursive)
> delete file or dir

cmd_rename_file(old_path, new_path)
> rename file or dir

cmd_storage_list(path")
> get file & dir listing

### [System Calls](flipper_sys.py) ###
---

cmd_FactoryReset()
> Factory Reset

cmd_Update(update_manifest)
> Update

cmd_Reboot(mode)
> Reboot flipper

cmd_PowerInfo()
> Power info / charging status

cmd_DeviceInfo()
> Device Info

cmd_ProtobufVersion()
> Protobuf Version

cmd_GetDateTime()
> Get system Date and Time

cmd_SetDateTime(arg_datetm)
> Set system Date and Time

cmd_System_Ping(data_bytes)
> Ping flipper

cmd_Audiovisual_Alert()
> Launch audiovisual alert on flipper ??

cmd_Stop_Session()
> Stop RPC session

-----

See Also:  [flipperdevices/flipperzero-protobuf](http://github.com/flipperdevices/flipperzero-protobuf)

