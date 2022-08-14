Module flipperzero_protobuf
===========================

Sub-modules
-----------
* flipperzero_protobuf.cli_helpers
* flipperzero_protobuf.flipperCmd
* flipperzero_protobuf.flipper_app
* flipperzero_protobuf.flipper_base
* flipperzero_protobuf.flipper_gpio
* flipperzero_protobuf.flipper_gui
* flipperzero_protobuf.flipper_proto
* flipperzero_protobuf.flipper_storage
* flipperzero_protobuf.flipper_sys
* flipperzero_protobuf.flipperzero_cmd

Classes
-------

`FlipperProto(serial_port=None, debug=0)`
:   Meta command class

### Ancestors (in MRO)

* flipperzero_protobuf.flipper_base.FlipperProtoBase
* flipperzero_protobuf.flipper_sys.FlipperProtoSys
* flipperzero_protobuf.flipper_gpio.FlipperProtoGpio
* flipperzero_protobuf.flipper_app.FlipperProtoApp
* flipperzero_protobuf.flipper_gui.FlipperProtoGui
* flipperzero_protobuf.flipper_storage.FlipperProtoStorage

### Methods

`rpc_app_button_press(self, args) ‑> None`
:   Send button press command to app.
    
    Returns
    ----------
    None
    
    Raises
    ----------
    cmdException

`rpc_app_button_release(self) ‑> None`
:   Send button release command to app
    
    Returns
    ----------
    None
    
    Raises
    ----------
    cmdException

`rpc_app_exit(self) ‑> None`
:   Send exit command to app
    
    Returns
    ----------
    None
    
    Raises
    ----------
    cmdException

`rpc_app_load_file(self, path) ‑> None`
:   Send load file command to app.
    
    Returns
    ----------
    None
    
    Raises
    ----------
    cmdException

`rpc_app_start(self, name, args) ‑> None`
:   Start/Run application
    
    Parameters
    ----------
    name : str
    args : str
    
    Returns
    ----------
    None
    
    Raises
    ----------
    cmdException

`rpc_audiovisual_alert(self) ‑> None`
:   Launch audiovisual alert on flipper ??
    
    Parameters
    ----------
    None
    
    Returns
    ----------
    None
    
    Raises
    ----------
    cmdException

`rpc_backup_create(self, archive_path=None) ‑> None`
:   Create Backup
    
    Parameters
    ----------
    archive_path : str
	path to archive_path
    
    Returns
    -------
	None
    
    Raises
    ----------
	cmdException

`rpc_backup_restore(self, archive_path=None) ‑> None`
:   Backup Restore
    
    Parameters
    ----------
    archive_path : str
	path to archive_path
    
    Returns
    -------
	None
    
    Raises
    ----------
	cmdException

`rpc_delete(self, path=None, recursive=False) ‑> None`
:   delete file or dir
    
    Parameters
    ----------
    path : str
	path to file or dir on flipper device
    
    Raises
    ----------
	cmdException

`rpc_device_info(self) ‑> tuple[str, str]`
:   Device Info
    
    Return
    ----------
    key, value : str
    
    Raises
    ----------
    cmdException

`rpc_factory_reset(self) ‑> None`
:   Factory Reset
    
    Parameters
    ----------
    None
    
    Returns
    ----------
    None
    
    Raises
    ----------
    cmdException

`rpc_get_datetime(self) ‑> dict`
:   Get system Date and Time
    
    Parameters
    ----------
    None
    
    Returns
    ----------
    dict
	keys: 'year', 'month', 'day', 'hour', 'minute', 'second', 'weekday'
    
    Raises
    ----------
    cmdException

`rpc_gpio_get_pin_mode(self, pin) ‑> str`
:   get GPIO pin mode
    
    Parameters
    ----------
    pin : int or str
	0 = 'PC0'
	1 = 'PC1'
	2 = 'PC3'
	3 = 'PB2'
	4 = 'PB3'
	5 = 'PA4'
	6 = 'PA6'
	7 = 'PA7'
    
    Returns:
    ----------
    str
	'OUTPUT'
	'INPUT'
    
    Raises
    ----------
    InputTypeException
    cmdException

`rpc_gpio_read_pin(self, pin) ‑> int`
:   query GPIO pin
    
    Parameters
    ----------
    pin : int or str
	0 = 'PC0'
	1 = 'PC1'
	2 = 'PC3'
	3 = 'PB2'
	4 = 'PB3'
	5 = 'PA4'
	6 = 'PA6'
	7 = 'PA7'
    
    Returns:
    ----------
    int
	pin value
    
    Raises
    ----------
    InputTypeException
    cmdException

`rpc_gpio_set_input_pull(self, pin, pull_mode) ‑> None`
:   Set GPIO pill Input
    
    Parameters
    ----------
    pin : int or str
	0 = 'PC0'
	1 = 'PC1'
	2 = 'PC3'
	3 = 'PB2'
	4 = 'PB3'
	5 = 'PA4'
	6 = 'PA6'
	7 = 'PA7'
    
    pull_mode : str
	0 = 'NO'
	1 = 'UP'
	2 = 'DOWN'
    
    Returns:
    ----------
    None
    
    Raises
    ----------
    InputTypeException
    cmdException

`rpc_gpio_set_pin_mode(self, pin, mode) ‑> None`
:   set GPIO pin mode
    
    Parameters
    ----------
    pin : int or str
	0 = 'PC0'
	1 = 'PC1'
	2 = 'PC3'
	3 = 'PB2'
	4 = 'PB3'
	5 = 'PA4'
	6 = 'PA6'
	7 = 'PA7'
    
    mode : str
	0 = 'OUTPUT'
	1 = 'INPUT'
    
    Returns:
    ----------
    None
    
    Raises
    ----------
    InputTypeException
    cmdException

`rpc_gpio_write_pin(self, pin, value) ‑> None`
:   write GPIO pin
    
    Parameters
    ----------
    pin : int or str
	0 = 'PC0'
	1 = 'PC1'
	2 = 'PC3'
	3 = 'PB2'
	4 = 'PB3'
	5 = 'PA4'
	6 = 'PA6'
	7 = 'PA7'
    
    value : int
    
    Returns:
    ----------
    None
    
    Raises
    ----------
    InputTypeException
    cmdException

`rpc_gui_send_input(self, key_arg) ‑> None`
:   Send Input Event Request Type
    
    Parameters
    ----------
    key_arg : tuple
	tuple = (InputKey, InputType)
	valid InputKeykey values: 'UP', 'DOWN', 'RIGHT', 'LEFT', 'OK'
	valid InputType values: 'PRESS', 'RELEASE', 'SHORT', 'LONG', 'REPEAT'
    
    Returns
    -------
    None
    
    Raises
    ----------
    cmdException
    InputTypeException

`rpc_gui_send_input_event_request(self, key, itype) ‑> None`
:   Send Input Event Request Key
    
    Parameters
    ----------
    key : str
	'UP', 'DOWN', 'RIGHT', 'LEFT', 'OK'
    itype : str
	'PRESS', 'RELEASE', 'SHORT', 'LONG', 'REPEAT'
    
    Returns
    -------
    None
    
    Raises
    ----------
    cmdException

`rpc_gui_snapshot_screen(self) ‑> bytes`
:   Snapshot screen
    
    Parameters
    ----------
    None
    
    Returns
    -------
	bytes
    
    Raises
    ----------
    cmdException

`rpc_gui_start_screen_stream(self) ‑> None`
:   Start screen stream
    
    Parameters
    ----------
    None
    
    Returns
    -------
    None
    
    Raises
    ----------
    cmdException

`rpc_info(self, path=None) ‑> dict`
:   get filesystem info
    
    Parameters
    ----------
    path : str
	path to filesystem
    
    Returns:
    ----------
    dict
    
    Raises
    ----------
	cmdException

`rpc_lock_status(self) ‑> bool`
:   Get LockScreen Status
    
    Returns
    ----------
    bool
    
    Raises
    ----------
    cmdException

`rpc_md5sum(self, path=None) ‑> str`
:   get md5 of file
    
    Parameters
    ----------
    path : str
	path to file on flipper device
    
    Raises
    ----------
	cmdException

`rpc_mkdir(self, path) ‑> None`
:   creates a new directory
    
    Parameters
    ----------
    path : str
	path for ew directory on flipper device
    
    Raises
    ----------
	cmdException

`rpc_power_info(self) ‑> tuple[str, str]`
:   Power info / charging status
    
    Parameters
    ----------
    None
    
    Returns
    ----------
    key, value : str
    
    Raises
    ----------
    cmdException

`rpc_protobuf_version(self) ‑> tuple[int, int]`
:   Protobuf Version
    
    Parameters
    ----------
    None
    
    Return
    ----------
    major, minor : int
    
    Raises
    ----------
    cmdException

`rpc_read(self, path=None) ‑> bytes`
:   read file from flipperzero device
    
    Parameters
    ----------
    path : str
	path to file on flipper device
    
    Returns
    -------
	bytes
    
    Raises
    ----------
	cmdException

`rpc_reboot(self, mode=0) ‑> None`
:   Reboot flipper
    
    Parameters
    ----------
    mode : int or str
	0 = OS
	1 = DFU
	2 = UPDATE
    
    Returns
    ----------
    None
    
    Raises
    ----------
    InputTypeException
    cmdException

`rpc_rename_file(self, old_path=None, new_path=None) ‑> None`
:   rename file or dir
    
    Parameters
    ----------
    old_path : str
	path to file or dir on flipper device
    new_path : str
	path to file or dir on flipper device
    
    Raises
    ----------
	cmdException

`rpc_set_datetime(self, arg_datetm=None) ‑> None`
:   Set system Date and Time
    
    Parameters
    ----------
    datetm : dict or datetime obj
	dict keys: 'year', 'month', 'day', 'hour', 'minute', 'second', 'weekday'
	datetime obj
	None (default) method datetime.datetime.now() is called
    
    Returns
    ----------
    None
    
    Raises
    ----------
    InputTypeException
    cmdException

`rpc_start_virtual_display(self, data) ‑> None`
:   Start Virtual Display
    
    Parameters
    ----------
    data : bytes
    
    Returns
    -------
    None
    
    Raises
    ----------
    cmdException

`rpc_stat(self, path=None) ‑> dict`
:   get info or file or directory file from flipperzero device
    
    Parameters
    ----------
    path : str
	path to file on flipper device
    
    Raises
    ----------
	cmdException

`rpc_stop_session(self) ‑> None`
:   Stop RPC session
    
    Parameters
    ----------
    None
    
    Returns
    ----------
    None
    
    Raises
    ----------
    cmdException

`rpc_stop_virtual_display(self) ‑> None`
:   Stop Virtual Display
    
    Parameters
    ----------
    None
    
    Returns
    -------
    None
    
    Raises
    ----------
    cmdException

`rpc_storage_list(self, path='/ext') ‑> list`
:   get file & dir listing
    
    Parameters
    ----------
    path : str
	path to filesystem
    
    Returns:
    ----------
    list
    
    Raises
    ----------
	cmdException

`rpc_system_ping(self, data=b'\xde\xad\xbe\xef') ‑> list`
:   Ping flipper
    
    Parameters
    ----------
    data : bytes
    
    Returns
    ----------
    list
    
    Raises
    ----------
    InputTypeException
    cmdException

`rpc_update(self, update_manifest='') ‑> None`
:   Update
    
    Parameters
    ----------
    update_manifest : str
    
    Returns
    ----------
    None
    
    code ; str
	0 OK
	1 ManifestPathInvalid
	2 ManifestFolderNotFound
	3 ManifestInvalid
	4 StageMissing
	5 StageIntegrityError
	6 ManifestPointerError
	7 TargetMismatch
	8 OutdatedManifestVersion
	9 IntFull

`rpc_write(self, path=None, data='') ‑> None`
:   write file from flipperzero device
    
    Parameters
    ----------
    path : str
	path to file on flipper device
    data : bytes
	data to write
    
    Raises
    ----------
	cmdException

`send_cmd(self, cmd_str) ‑> None`
:   send non rpc command to flipper

`start_rpc_session(self) ‑> None`
:   start rpc session
