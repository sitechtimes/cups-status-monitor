# pycups API Reference

Generated from the OpenPrinting/pycups Python bindings for CUPS.

This reference documents the public Python interfaces exposed by `pycups`, including module-level functions, the `Connection` class, PPD handling, IPP request handling, read-only data objects, and exported constants.

> [!IMPORTANT]
> This API reference was created with the help of artificial intelligence to make the development process easier. The information provided was checked manually for errors; however, anyone referring to this documentation should carefully verify important details.

---

## Table of Contents

1. [Module-Level Functions](#module-level-functions)
2. [`cups.Connection`](#cupsconnection)
3. [`cups.PPD`](#cupsppd)
4. [`cups.IPPRequest`](#cupsipprequest)
5. [Read-Only Data Objects](#read-only-data-objects)
6. [Constants and Enumerations](#constants-and-enumerations)

---

## Module-Level Functions

These functions are accessed directly from the imported `cups` module.

### `cups.modelSort(s1, s2) -> integer`

Sort two model strings.

This performs a smart comparison that handles numeric portions of model names correctly, so that model names containing numbers compare in a natural order.

**Parameters**

- `s1` (`string`): First string.
- `s2` (`string`): Second string.

**Returns**

- `integer`: A `strcmp`-style comparison result.

---

### `cups.setUser(user) -> None`

Set the user to connect as.

This affects the default requesting user name used in subsequent CUPS operations.

**Parameters**

- `user` (`string`): Username.

---

### `cups.setServer(server) -> None`

Set the CUPS server to connect to.

**Parameters**

- `server` (`string`): Server hostname or address.

---

### `cups.setPort(port) -> None`

Set the IPP port to connect to.

**Parameters**

- `port` (`integer`): IPP port.

---

### `cups.setEncryption(policy) -> None`

Set the encryption policy.

**Parameters**

- `policy` (`integer`): One of:
    - `HTTP_ENCRYPT_ALWAYS`
    - `HTTP_ENCRYPT_IF_REQUESTED`
    - `HTTP_ENCRYPT_NEVER`
    - `HTTP_ENCRYPT_REQUIRED`

---

### `cups.getUser() -> string`

Get the user to connect as.

**Returns**

- `string`: Current username.

---

### `cups.getServer() -> string`

Get the server to connect to.

**Returns**

- `string`: Current server hostname or address.

---

### `cups.getPort() -> integer`

Get the IPP port to connect to.

**Returns**

- `integer`: Current IPP port.

---

### `cups.getEncryption() -> integer`

Get the encryption policy.

**Returns**

- `integer`: Current encryption policy.

**See Also**

- `cups.setEncryption`

---

### `cups.setPasswordCB(fn) -> None`

Set a password callback function.

The supplied Python function is called when a password is required. It must accept one string parameter, the password prompt, and must return either:

- a string containing the password, or
- `None` to abort the operation.

**Parameters**

- `fn` (`callable object`): Callback function.

---

### `cups.setPasswordCB2(fn, context=None) -> None`

Set an extended password callback function.

The supplied Python function is called when a password is required. It must accept the following parameters:

- password prompt string
- `cups.Connection` instance
- HTTP method string
- HTTP resource string
- optional user-supplied context

It must return either:

- a string containing the password, or
- `None` to abort the operation.

**Parameters**

- `fn` (`callable object`, or `None`): Callback function, or `None` for the default handler.
- `context` (`object`, optional): User-supplied context passed to the callback.

---

### `cups.ppdSetConformance(level) -> None`

Set the PPD conformance level.

**Parameters**

- `level` (`integer`): One of:
    - `PPD_CONFORM_RELAXED`
    - `PPD_CONFORM_STRICT`

---

### `cups.enumDests(cb, flags=0, msec=-1, type=0, mask=0, user_data=None) -> None`

Enumerate destinations.

The callback receives the user data, destination flags, and a destination object. It should return `1` to continue enumeration or `0` to stop enumeration.

**Parameters**

- `cb` (`callable`): Callback function.
- `flags` (`integer`): Enumeration flags.
- `msec` (`integer`): Timeout in milliseconds, or `-1` for no timeout.
- `type` (`integer`): Bitmask of printer types to return.
- `mask` (`integer`): Bitmask of type bits to examine.
- `user_data` (`object`): User data to pass to the callback.

---

### `cups.connectDest(dest, cb, flags=0, msec=-1, user_data=None) -> (conn, resource)`

Connect to a destination.

**Parameters**

- `dest` (`Dest object`): Destination to connect to.
- `cb` (`callable`): Callback function.
- `flags` (`integer`): Enumeration flags.
- `msec` (`integer`): Timeout in milliseconds, or `-1` for no timeout.
- `user_data` (`object`): User data to pass to the callback.

**Returns**

- `(Connection, string)`: A tuple containing a `Connection` object and the HTTP resource.

---

### `cups.ippErrorString(statuscode) -> string`

Get a human-readable string for an IPP status code.

**Parameters**

- `statuscode` (`integer`): IPP request status code.

**Returns**

- `string`: Status code description.

---

### `cups.ippOpString(op) -> string`

Get a human-readable string for an IPP operation.

**Parameters**

- `op` (`integer`): IPP request operation.

**Returns**

- `string`: Operation name.

---

### `cups.require(version) -> None`

Require a minimum `pycups` version.

If the requirement is not met, a `RuntimeError` is raised.

**Parameters**

- `version` (`string`): Minimum required `pycups` version.

**Raises**

- `RuntimeError`: Requirement not met.

---

## `cups.Connection`

A connection to the CUPS server.

Before creating a connection, the server and username may be set using `cups.setServer` and `cups.setUser`; otherwise defaults are used. When a `Connection` object is instantiated, it results in a call to the libcups function `httpConnectEncrypt()`.

The constructor accepts optional `host`, `port`, and `encryption` arguments. These default to the values returned by `cups.getServer()`, `cups.getPort()`, and `cups.getEncryption()`.

---

### Connection Information and Enumeration

#### `Connection.getPrinters() -> dict`

Fetch printers.

**Returns**

- `dict`: A dictionary indexed by printer name. Each value is a dictionary of printer attributes.

**Raises**

- `IPPError`: IPP problem.

---

#### `Connection.getDests() -> dict`

Fetch destinations.

**Returns**

- `dict`: A dictionary representing available destinations. Keys are usually `(queue, instance)` tuples, and values are `Dest` objects.

---

#### `Connection.getClasses() -> dict`

Fetch classes.

**Returns**

- `dict`: A dictionary indexed by class name. Values represent class membership.

**Raises**

- `IPPError`: IPP problem.

---

#### `Connection.getPPDs(limit=0, exclude_schemes=None, include_schemes=None) -> dict`

Fetch available PPDs.

**Parameters**

- `limit` (`integer`): Maximum number of PPDs to return.
- `exclude_schemes` (`string list`): URI schemes to exclude.
- `include_schemes` (`string list`): URI schemes to include.

**Returns**

- `dict`: A dictionary of available PPDs.

**Raises**

- `IPPError`: IPP problem.

---

#### `Connection.getPPDs2(limit=0, exclude_schemes=None, include_schemes=None) -> dict`

Fetch available PPDs, version 2.

This is an extended form of `getPPDs`.

**Parameters**

- `limit` (`integer`): Maximum number of PPDs to return.
- `exclude_schemes` (`string list`): URI schemes to exclude.
- `include_schemes` (`string list`): URI schemes to include.

**Returns**

- `dict`: A dictionary of available PPDs.

**Raises**

- `IPPError`: IPP problem.

---

#### `Connection.getDevices() -> dict`

Fetch devices.

**Returns**

- `dict`: A dictionary indexed by device URI. Each value is a dictionary of device attributes.

**Raises**

- `IPPError`: IPP problem.

---

#### `Connection.getJobs(which_jobs='not-completed', my_jobs=False, limit=-1, first_job_id=-1, requested_attributes=None) -> dict`

Fetch jobs.

**Parameters**

- `which_jobs` (`string`): Which jobs to fetch. Common values include:
    - `'completed'`
    - `'not-completed'`
    - `'all'`
- `my_jobs` (`boolean`): Whether to return only jobs owned by the current CUPS user.
- `limit` (`integer`): Maximum number of jobs to return.
- `first_job_id` (`integer`): Lowest job ID to return.
- `requested_attributes` (`string list`): List of requested attribute names.

**Returns**

- `dict`: A dictionary indexed by job ID. Each value is a dictionary of job attributes.

**Raises**

- `IPPError`: IPP problem.

---

#### `Connection.getJobAttributes(jobid, requested_attributes=None) -> dict`

Fetch attributes for one job.

**Parameters**

- `jobid` (`integer`): Job ID.
- `requested_attributes` (`string list`): List of requested attribute names.

**Returns**

- `dict`: Job attributes.

**Raises**

- `IPPError`: IPP problem.

---

#### `Connection.getPrinterAttributes(name=None, uri=None, requested_attributes=None) -> dict`

Fetch attributes for a printer.

The printer may be specified by either `name` or `uri`, but not both.

**Parameters**

- `name` (`string`): Queue name.
- `uri` (`string`): Queue URI.
- `requested_attributes` (`string list`): List of requested attribute names.

**Returns**

- `dict`: Printer attributes.

Common attributes include:

- `job-sheets-supported`
- `job-sheets-default`
- `printer-error-policy-supported`
- `printer-error-policy`
- `printer-op-policy-supported`
- `printer-op-policy`

The exact attributes returned depend on the IPP server.

**Raises**

- `IPPError`: IPP problem.

---

#### `Connection.getDefault() -> string or None`

Get the system default printer.

**Returns**

- `string` or `None`: Default printer name, or `None` if no default is set.

---

#### `Connection.getPPD(name) -> string`

Fetch a printer’s PPD.

**Parameters**

- `name` (`string`): Queue name.

**Returns**

- `string`: Temporary PPD file name.

**Raises**

- `IPPError`: IPP problem.

---

#### `Connection.getPPD3(name, modtime=None, filename=None) -> (status, modtime, filename)`

Fetch a printer’s PPD if it is newer.

**Parameters**

- `name` (`string`): Queue name.
- `modtime` (`float`): Modification time of existing file.
- `filename` (`string`): Filename of existing file.

**Returns**

- `(integer, float, string)`: HTTP status, modification time, and filename.

---

#### `Connection.getSubscriptions(uri, my_subscriptions=False, job_id=-1) -> integer list`

Get subscriptions.

**Parameters**

- `uri` (`string`): URI for object.
- `my_subscriptions` (`boolean`): Only return subscriptions belonging to the current user.
- `job_id` (`integer`): Only return subscriptions relating to this job.

**Returns**

- `integer list`: List of subscription IDs.

**Raises**

- `IPPError`: IPP problem.

---

#### `Connection.getNotifications(subscription_ids) -> list`

Get notifications for subscribed events.

**Parameters**

- `subscription_ids` (`integer list`): Subscription IDs to receive notifications for.

**Returns**

- `list`: A list of dictionaries, each representing an event.

**Raises**

- `IPPError`: IPP problem.

---

### Job Submission and Control

#### `Connection.printFile(printer, filename, title, options) -> integer`

Print a file.

**Parameters**

- `printer` (`string`): Queue name.
- `filename` (`string`): Local file path to the document.
- `title` (`string`): Title of the print job.
- `options` (`dict`): Dictionary of job options.

**Returns**

- `integer`: Job ID.

**Raises**

- `IPPError`: IPP problem.

---

#### `Connection.printFiles(printer, filenames, title, options) -> integer`

Print a list of files.

**Parameters**

- `printer` (`string`): Queue name.
- `filenames` (`list`): List of local file paths.
- `title` (`string`): Title of the print job.
- `options` (`dict`): Dictionary of job options.

**Returns**

- `integer`: Job ID.

**Raises**

- `IPPError`: IPP problem.

---

#### `Connection.printTestPage(name) -> integer`

Print a test page.

**Parameters**

- `name` (`string`): Queue name.

**Keyword Parameters**

- `file` (`string`): Input file. Defaults to the CUPS test page.
- `title` (`string`): Job title. Defaults to `'Test Page'`.
- `format` (`string`): Document format. Defaults to `'application/postscript'`.
- `user` (`string`): User to submit the job as.

**Returns**

- `integer`: Job ID.

**Raises**

- `IPPError`: IPP problem.

---

#### `Connection.createJob(printer, title, options) -> integer`

Create an empty job for streaming.

**Parameters**

- `printer` (`string`): Queue name.
- `title` (`string`): Title of the print job.
- `options` (`dict`): Dictionary of options.

**Returns**

- `integer`: Job ID.

**Raises**

- `IPPError`: IPP problem.

---

#### `Connection.startDocument(printer, job_id, doc_name, format, last_document) -> integer`

Add a document to a job created with `createJob`.

**Parameters**

- `printer` (`string`): Queue name.
- `job_id` (`integer`): Job ID.
- `doc_name` (`string`): Document name.
- `format` (`string`): MIME type.
- `last_document` (`integer`): `1` if this is the last document in the job, otherwise `0`.

**Returns**

- `integer`: HTTP status.

**Raises**

- `IPPError`: IPP problem.

---

#### `Connection.writeRequestData(buffer, length) -> integer`

Write data after an IPP request.

**Parameters**

- `buffer` (`bytes`): Bytes to write.
- `length` (`integer`): Number of bytes to write.

**Returns**

- `integer`: HTTP status.

**Raises**

- `IPPError`: IPP problem.

---

#### `Connection.finishDocument(printer) -> integer`

Finish sending a document.

**Parameters**

- `printer` (`string`): Queue name.

**Returns**

- `integer`: HTTP status.

**Raises**

- `IPPError`: IPP problem.

---

#### `Connection.cancelJob(jobid, purge_job=False) -> None`

Cancel a job.

**Parameters**

- `jobid` (`integer`): Job ID to cancel.
- `purge_job` (`boolean`): Whether to remove data and control files.

**Raises**

- `IPPError`: IPP problem.

---

#### `Connection.cancelAllJobs(name=None, uri=None, my_jobs=False, purge_jobs=True) -> None`

Cancel all jobs.

**Parameters**

- `name` (`string`): Queue name.
- `uri` (`string`): Printer URI.
- `my_jobs` (`boolean`): Restrict operation to jobs owned by the current CUPS user.
- `purge_jobs` (`boolean`): Whether to remove data and control files.

**Raises**

- `IPPError`: IPP problem.

---

#### `Connection.moveJob(printer_uri=None, job_id=-1, job_printer_uri=None) -> None`

Move a job.

A job may be identified by printer URI and/or job ID. The destination printer is given by `job_printer_uri`.

**Parameters**

- `printer_uri` (`string`): Printer to move job from.
- `job_id` (`integer`): Job ID to move.
- `job_printer_uri` (`string`): Printer to move job to.

**Raises**

- `IPPError`: IPP problem.

---

#### `Connection.authenticateJob(jobid, auth_info=None) -> None`

Authenticate a job.

**Parameters**

- `jobid` (`integer`): Job ID to authenticate.
- `auth_info` (`string list`, optional): Authentication details.

**Raises**

- `IPPError`: IPP problem.

---

#### `Connection.setJobHoldUntil(jobid, job_hold_until) -> None`

Specify when a job should be printed.

**Parameters**

- `jobid` (`integer`): Job ID to adjust.
- `job_hold_until` (`string`): When to print the job. Examples include:
    - `'hold'`
    - `'immediate'`
    - `'restart'`
    - `'resume'`

**Raises**

- `IPPError`: IPP problem.

---

#### `Connection.restartJob(job_id, job_hold_until=None) -> None`

Restart a job.

**Parameters**

- `job_id` (`integer`): Job ID to restart.
- `job_hold_until` (`string`): New `job-hold-until` value for the job.

**Raises**

- `IPPError`: IPP problem.

---

### Printer and Queue Administration

#### `Connection.addPrinter(name) -> None`

Add or adjust a print queue.

Several parameters can select which PPD to use, including `filename`, `ppdname`, and `ppd`, but only one may be given.

**Parameters**

- `name` (`string`): Queue name.

**Keyword Parameters**

- `filename` (`string`): Local filename of a PPD file.
- `ppdname` (`string`): PPD filename from `getPPDs`.
- `info` (`string`): Human-readable printer information.
- `location` (`string`): Human-readable printer location.
- `device` (`string`): Device URI string.
- `ppd` (`cups.PPD`): PPD object.

**Raises**

- `IPPError`: IPP problem.

---

#### `Connection.deletePrinter(name) -> None`

Delete a printer.

**Parameters**

- `name` (`string`): Queue name.

**Raises**

- `IPPError`: IPP problem.

---

#### `Connection.setDefault(name) -> None`

Set the system default printer.

This can be overridden on a per-user basis using the `lpoptions` command.

**Parameters**

- `name` (`string`): Queue name.

**Raises**

- `IPPError`: IPP problem.

---

#### `Connection.enablePrinter(name) -> None`

Enable a printer.

This allows the printer to process its job queue.

**Parameters**

- `name` (`string`): Queue name.

**Raises**

- `IPPError`: IPP problem.

---

#### `Connection.disablePrinter(name) -> None`

Disable a printer.

This prevents the printer from processing its job queue.

**Parameters**

- `name` (`string`): Queue name.

**Keyword Parameters**

- `reason` (`string`): Optional human-readable reason.

**Raises**

- `IPPError`: IPP problem.

---

#### `Connection.acceptJobs(name) -> None`

Cause a printer to accept jobs.

**Parameters**

- `name` (`string`): Queue name.

**Raises**

- `IPPError`: IPP problem.

---

#### `Connection.rejectJobs(name) -> None`

Cause a printer to reject jobs.

**Parameters**

- `name` (`string`): Queue name.

**Keyword Parameters**

- `reason` (`string`): Optional human-readable reason.

**Raises**

- `IPPError`: IPP problem.

---

#### `Connection.setPrinterDevice(name, device_uri) -> None`

Set the device URI for a printer.

**Parameters**

- `name` (`string`): Queue name.
- `device_uri` (`string`): Device URI.

**Raises**

- `IPPError`: IPP problem.

---

#### `Connection.setPrinterInfo(name, info) -> None`

Set human-readable information about a printer.

**Parameters**

- `name` (`string`): Queue name.
- `info` (`string`): Human-readable information.

**Raises**

- `IPPError`: IPP problem.

---

#### `Connection.setPrinterLocation(name, location) -> None`

Set the human-readable printer location.

**Parameters**

- `name` (`string`): Queue name.
- `location` (`string`): Human-readable location.

**Raises**

- `IPPError`: IPP problem.

---

#### `Connection.setPrinterShared(name, shared) -> None`

Set whether a printer is shared with other people.

This works with CUPS servers of at least version 1.2 by setting the `printer-is-shared` printer attribute.

**Parameters**

- `name` (`string`): Queue name.
- `shared` (`boolean`): Whether the printer should be shared.

**Raises**

- `IPPError`: IPP problem.

---

#### `Connection.setPrinterJobSheets(name, start, end) -> None`

Specify job sheets for a printer.

**Parameters**

- `name` (`string`): Queue name.
- `start` (`string`): Sheet to print before each job.
- `end` (`string`): Sheet to print after each job.

**Raises**

- `IPPError`: IPP problem.

---

#### `Connection.setPrinterErrorPolicy(name, policy) -> None`

Set a printer’s error policy.

**Parameters**

- `name` (`string`): Queue name.
- `policy` (`string`): Policy name.

Supported policy names can be found using `getPrinterAttributes` and inspecting the `printer-error-policy-supported` attribute.

**Raises**

- `IPPError`: IPP problem.

---

#### `Connection.setPrinterOpPolicy(name, policy) -> None`

Set a printer’s operation policy.

**Parameters**

- `name` (`string`): Queue name.
- `policy` (`string`): Policy name.

Supported policy names can be found using `getPrinterAttributes` and inspecting the `printer-op-policy-supported` attribute.

**Raises**

- `IPPError`: IPP problem.

---

#### `Connection.setPrinterUsersAllowed(name, allowed) -> None`

Set the list of users allowed to use a printer.

This works with CUPS servers of at least version 1.2 by setting the `requesting-user-name-allowed` printer attribute.

**Parameters**

- `name` (`string`): Queue name.
- `allowed` (`string list`): List of allowed users. `['all']` means no user-name restriction.

**Raises**

- `IPPError`: IPP problem.

---

#### `Connection.setPrinterUsersDenied(name, denied) -> None`

Set the list of users denied the use of a printer.

This works with CUPS servers of at least version 1.2 by setting the `requesting-user-name-denied` printer attribute.

**Parameters**

- `name` (`string`): Queue name.
- `denied` (`string list`): List of denied users. `['none']` means no user-name restriction.

**Raises**

- `IPPError`: IPP problem.

---

#### `Connection.addPrinterOptionDefault(name, option, value) -> None`

Set a network default option.

Jobs submitted to the named queue will have the job option added if it is not already present in the job. This works with CUPS servers of at least version 1.2.

**Parameters**

- `name` (`string`): Queue name.
- `option` (`string`): Option name, for example `'job-priority'`.
- `value` (`string`): Option value as a string.

**Raises**

- `IPPError`: IPP problem.

---

#### `Connection.deletePrinterOptionDefault(name, option) -> None`

Remove a network default option.

**Parameters**

- `name` (`string`): Queue name.
- `option` (`string`): Option name, for example `'job-priority'`.

**Raises**

- `IPPError`: IPP problem.

---

### Class Administration

#### `Connection.addPrinterToClass(name, class) -> None`

Add a printer to a class.

If the class does not yet exist, it is created.

**Parameters**

- `name` (`string`): Queue name.
- `class` (`string`): Class name.

**Raises**

- `IPPError`: IPP problem.

---

#### `Connection.deletePrinterFromClass(name, class) -> None`

Remove a printer from a class.

If the class would be left empty, it is removed.

**Parameters**

- `name` (`string`): Queue name.
- `class` (`string`): Class name.

**Raises**

- `IPPError`: IPP problem.

---

#### `Connection.deleteClass(class) -> None`

Delete a class.

**Parameters**

- `class` (`string`): Class name.

**Raises**

- `IPPError`: IPP problem.

---

### Subscriptions

#### `Connection.createSubscription(uri, events=[], job_id=-1, recipient_uri="", lease_duration=-1, time_interval=-1, user_data="") -> integer`

Create a subscription.

**Parameters**

- `uri` (`string`): URI for object.
- `events` (`string list`): Events to receive notifications for.
- `job_id` (`integer`): Job ID to receive notifications for.
- `recipient_uri` (`string`): URI for notification recipient.
- `lease_duration` (`integer`): Lease duration in seconds.
- `time_interval` (`integer`): Time interval.
- `user_data` (`string`): User data to receive with notifications.

**Returns**

- `integer`: Subscription ID.

**Raises**

- `IPPError`: IPP problem.

---

#### `Connection.cancelSubscription(id) -> None`

Cancel a subscription.

**Parameters**

- `id` (`integer`): Subscription ID.

**Raises**

- `IPPError`: IPP problem.

---

#### `Connection.renewSubscription(id, lease_duration=-1) -> None`

Renew a subscription.

**Parameters**

- `id` (`integer`): Subscription ID.
- `lease_duration` (`integer`): Lease duration in seconds.

**Raises**

- `IPPError`: IPP problem.

---

### Server Files and Administration

#### `Connection.getFile(resource, filename=None, fd=-1, file=None) -> None`

Fetch a CUPS server resource into a local file.

This is useful for obtaining CUPS server configuration files and log files.

**Parameters**

- `resource` (`string`): Resource name.
- `filename` (`string`): Local filename for storage.
- `fd` (`integer`): Local file descriptor.
- `file` (`file`): Python file object for local file.

**Raises**

- `HTTPError`: HTTP problem.

---

#### `Connection.putFile(resource, filename=None, fd=-1, file=None) -> None`

Upload a file to the CUPS server.

This is useful for uploading new configuration files. Note that `adminSetServerSettings` can adjust server settings without needing to parse the configuration file manually.

**Parameters**

- `resource` (`string`): Resource name.
- `filename` (`string`): Local filename to upload.
- `fd` (`integer`): Local file descriptor.
- `file` (`file`): Python file object for local file.

**Raises**

- `HTTPError`: HTTP problem.

---

#### `Connection.adminExportSamba(name, samba_server, samba_username, samba_password) -> None`

Export a printer to Samba.

**Parameters**

- `name` (`string`): Queue name.
- `samba_server` (`string`): Samba server.
- `samba_username` (`string`): Samba username.
- `samba_password` (`string`): Samba password.

**Raises**

- `IPPError`: IPP problem.

---

#### `Connection.adminGetServerSettings() -> dict`

Get server settings.

**Returns**

- `dict`: Server settings.

Keywords may include:

- `CUPS_SERVER_DEBUG_LOGGING`
- `CUPS_SERVER_REMOTE_ADMIN`
- `CUPS_SERVER_REMOTE_PRINTERS`
- `CUPS_SERVER_SHARE_PRINTERS`
- `CUPS_SERVER_USER_CANCEL_ANY`

**See Also**

- `Connection.adminSetServerSettings`

**Raises**

- `IPPError`: IPP problem.

---

#### `Connection.adminSetServerSettings(settings) -> None`

Set server settings.

**Parameters**

- `settings` (`dict`): Dictionary of server settings.

**See Also**

- `Connection.adminGetServerSettings`

**Raises**

- `IPPError`: IPP problem.

---

## `cups.PPD`

A PPD file.

This object represents a parsed PostScript Printer Description file.

---

### `PPD.localize() -> None`

Localize the PPD.

This sets the PPD language to the current locale.

---

### `PPD.localizeIPPReason(reason, scheme) -> string or None`

Localize an IPP reason string.

**Parameters**

- `reason` (`string`): IPP reason string.
- `scheme` (`string`): Scheme.

**Returns**

- `string` or `None`: Localized reason string.

---

### `PPD.localizeMarkerName(name) -> string or None`

Localize a marker name.

**Parameters**

- `name` (`string`): Marker name.

**Returns**

- `string` or `None`: Localized marker name.

---

### `PPD.markDefaults() -> None`

Mark all default options.

This chooses the default choice for each option in the PPD.

---

### `PPD.markOption(option, choice) -> integer`

Mark an option.

**Parameters**

- `option` (`string`): Option keyword.
- `choice` (`string`): Choice keyword.

**Returns**

- `integer`: Number of conflicts.

---

### `PPD.conflicts() -> integer`

Return the number of conflicts.

**Returns**

- `integer`: Number of conflicting options.

---

### `PPD.findOption(option) -> Option or None`

Find an option.

**Parameters**

- `option` (`string`): Option keyword.

**Returns**

- `Option` or `None`: Option object if found.

---

### `PPD.findAttr(name, spec=None) -> Attribute or None`

Find an attribute.

**Parameters**

- `name` (`string`): Attribute name.
- `spec` (`string`, optional): Attribute specifier.

**Returns**

- `Attribute` or `None`: Attribute object if found.

---

### `PPD.findNextAttr(name, spec=None) -> Attribute or None`

Find the next matching attribute.

**Parameters**

- `name` (`string`): Attribute name.
- `spec` (`string`, optional): Attribute specifier.

**Returns**

- `Attribute` or `None`: Attribute object if found.

---

### `PPD.emit() -> string`

Emit marked options.

**Returns**

- `string`: Generated PostScript or PPD output.

---

### `PPD.emitFd(fd) -> None`

Emit marked options to a file descriptor.

**Parameters**

- `fd` (`integer`): File descriptor.

---

### `PPD.emitString() -> string`

Emit marked options as a string.

**Returns**

- `string`: Generated output.

---

### `PPD.emitJCL() -> string`

Emit JCL commands.

**Returns**

- `string`: Generated JCL output.

---

### `PPD.emitJCLEnd() -> string`

Emit JCL end commands.

**Returns**

- `string`: Generated JCL end output.

---

### `PPD.emitAfterOrder() -> string`

Emit marked options after order dependency processing.

**Returns**

- `string`: Generated output.

---

### `PPD.writeFd(fd) -> None`

Write the PPD to a file descriptor.

**Parameters**

- `fd` (`integer`): File descriptor.

---

## `cups.IPPRequest`

An IPP request.

This object represents an IPP request or response message.

---

### `IPPRequest.addSeparator() -> IPPAttribute`

Add a separator to the IPP request.

**Returns**

- `IPPAttribute`: The added separator attribute.

---

### `IPPRequest.add(attr) -> IPPAttribute`

Add an attribute to the IPP request.

**Parameters**

- `attr` (`IPPAttribute`): Attribute to add.

**Returns**

- `IPPAttribute`: The added attribute.

---

### `IPPRequest.readIO(read_fn, blocking=True) -> IPP state`

Read IPP request data using a callback.

**Parameters**

- `read_fn` (`callable`): Read function.
- `blocking` (`boolean`): Whether to read in blocking mode.

**Returns**

- `integer`: IPP state.

---

### `IPPRequest.writeIO(write_fn, blocking=True) -> IPP state`

Write IPP request data using a callback.

**Parameters**

- `write_fn` (`callable`): Write function.
- `blocking` (`boolean`): Whether to write in blocking mode.

**Returns**

- `integer`: IPP state.

---

## Read-Only Data Objects

These objects are returned by various `pycups` functions and methods.

---

### `cups.Dest`

A destination print queue.

Usually returned by `Connection.getDests`.

**Attributes**

- `name` (`string`): Destination queue name.
- `instance` (`string`): Destination instance name.
- `is_default` (`boolean`): Whether this is the default destination.
- `options` (`dict`): Dictionary of default options for this destination, indexed by option name.

---

### `cups.Option`

A PPD option.

**Attributes**

- `conflicted` (`boolean`): Whether this option is in conflict.
- `keyword` (`string`): Option keyword, for example `Duplex`.
- `defchoice` (`string`): Default option choice.
- `text` (`string`): User-presentable option name, for example `Double-sided printing`.
- `ui` (`integer`): Option type. One of:
    - `PPD_UI_BOOLEAN`
    - `PPD_UI_PICKONE`
    - `PPD_UI_PICKMANY`
- `choices` (`list`): List of the option’s choices.

---

### `cups.Group`

A PPD option group.

**Attributes**

- `text` (`string`): User-presentable group name.
- `name` (`string`): Group name.
- `options` (`list`): Options in the group.
- `subgroups` (`list`): Subgroups in the group.

---

### `cups.Constraint`

A PPD constraint.

**Attributes**

- `option1` (`string`): First option.
- `choice1` (`string`): First choice.
- `option2` (`string`): Second option.
- `choice2` (`string`): Second choice.

---

### `cups.Attribute`

A PPD attribute.

**Attributes**

- `name` (`string`): Attribute name.
- `spec` (`string`): Attribute specifier.
- `text` (`string`): Attribute text.
- `value` (`string`): Attribute value.

---

### `cups.IPPAttribute`

An IPP attribute.

**Attributes**

- `group_tag` (`integer`): IPP group tag.
- `value_tag` (`integer`): IPP value tag.
- `name` (`string`): IPP attribute name.
- `values` (`list`): List of values.

---

## Constants and Enumerations

The `cups` module exports many constants corresponding to CUPS, IPP, HTTP, and PPD definitions. Integer values below match the upstream CUPS headers exactly.

Note: Many IPP enumerations intentionally start at `3` (not `0`) to align with the IANA IPP registry. Job states, printer states, resolutions, orientations, qualities, and finishings all follow this convention.

---

### Printer Type Constants (`CUPS_PRINTER_*`)

These are bitmask flags combined with bitwise OR. `printer-type` attribute values are the OR of all applicable bits.

| Constant                     | Decimal    | Hex         |
| ---------------------------- | ---------- | ----------- |
| `CUPS_PRINTER_LOCAL`         | `0`        | `0x0000000` |
| `CUPS_PRINTER_CLASS`         | `1`        | `0x0000001` |
| `CUPS_PRINTER_REMOTE`        | `2`        | `0x0000002` |
| `CUPS_PRINTER_BW`            | `4`        | `0x0000004` |
| `CUPS_PRINTER_COLOR`         | `8`        | `0x0000008` |
| `CUPS_PRINTER_DUPLEX`        | `16`       | `0x0000010` |
| `CUPS_PRINTER_STAPLE`        | `32`       | `0x0000020` |
| `CUPS_PRINTER_COPIES`        | `64`       | `0x0000040` |
| `CUPS_PRINTER_COLLATE`       | `128`      | `0x0000080` |
| `CUPS_PRINTER_PUNCH`         | `256`      | `0x0000100` |
| `CUPS_PRINTER_COVER`         | `512`      | `0x0000200` |
| `CUPS_PRINTER_BIND`          | `1024`     | `0x0000400` |
| `CUPS_PRINTER_SORT`          | `2048`     | `0x0000800` |
| `CUPS_PRINTER_SMALL`         | `4096`     | `0x0001000` |
| `CUPS_PRINTER_MEDIUM`        | `8192`     | `0x0002000` |
| `CUPS_PRINTER_LARGE`         | `16384`    | `0x0004000` |
| `CUPS_PRINTER_VARIABLE`      | `32768`    | `0x0008000` |
| `CUPS_PRINTER_IMPLICIT`      | `65536`    | `0x0010000` |
| `CUPS_PRINTER_DEFAULT`       | `131072`   | `0x0020000` |
| `CUPS_PRINTER_FAX`           | `262144`   | `0x0040000` |
| `CUPS_PRINTER_REJECTING`     | `524288`   | `0x0080000` |
| `CUPS_PRINTER_DELETE`        | `1048576`  | `0x0100000` |
| `CUPS_PRINTER_NOT_SHARED`    | `2097152`  | `0x0200000` |
| `CUPS_PRINTER_AUTHENTICATED` | `4194304`  | `0x0400000` |
| `CUPS_PRINTER_COMMANDS`      | `8388608`  | `0x0800000` |
| `CUPS_PRINTER_OPTIONS`       | `16777216` | `0x1000000` |
| `CUPS_PRINTER_DISCOVERED`    | `33554432` | `0x2000000` |

Note: `CUPS_PRINTER_LOCAL` is `0` (the base value), not a bit. `printer_type & cups.CUPS_PRINTER_LOCAL` is always falsy. A printer is "local" when neither `CUPS_PRINTER_CLASS` nor `CUPS_PRINTER_REMOTE` is set.

Decoding examples:

- `36948` = `VARIABLE` (32768) | `SMALL` (4096) | `COPIES` (64) | `DUPLEX` (16) | `BW` (4): Local B&W duplex printer
- `61468` = `VARIABLE` (32768) | `LARGE` (16384) | `MEDIUM` (8192) | `SMALL` (4096) | `DUPLEX` (16) | `COLOR` (8) | `BW` (4): Local color printer, all media sizes

---

### HTTP Encryption Constants (`HTTP_ENCRYPT_*`)

| Constant                    | Value |
| --------------------------- | ----- |
| `HTTP_ENCRYPT_IF_REQUESTED` | `0`   |
| `HTTP_ENCRYPT_NEVER`        | `1`   |
| `HTTP_ENCRYPT_REQUIRED`     | `2`   |
| `HTTP_ENCRYPT_ALWAYS`       | `3`   |

---

### Document Format Constants (`CUPS_FORMAT_*`)

These are string constants (MIME types), not integers.

| Constant                 | Value                            |
| ------------------------ | -------------------------------- |
| `CUPS_FORMAT_AUTO`       | `"application/octet-stream"`     |
| `CUPS_FORMAT_COMMAND`    | `"application/vnd.cups-command"` |
| `CUPS_FORMAT_PDF`        | `"application/pdf"`              |
| `CUPS_FORMAT_POSTSCRIPT` | `"application/postscript"`       |
| `CUPS_FORMAT_RAW`        | `"application/vnd.cups-raw"`     |
| `CUPS_FORMAT_TEXT`       | `"text/plain"`                   |

---

### HTTP Status Constants (`HTTP_STATUS_*`)

| Constant                                  | Value  |
| ----------------------------------------- | ------ |
| `HTTP_STATUS_ERROR`                       | `-1`   |
| `HTTP_STATUS_OK`                          | `200`  |
| `HTTP_STATUS_NOT_MODIFIED`                | `304`  |
| `HTTP_STATUS_BAD_REQUEST`                 | `400`  |
| `HTTP_STATUS_UNAUTHORIZED`                | `401`  |
| `HTTP_STATUS_FORBIDDEN`                   | `403`  |
| `HTTP_STATUS_NOT_FOUND`                   | `404`  |
| `HTTP_STATUS_REQUEST_TIMEOUT`             | `408`  |
| `HTTP_STATUS_UPGRADE_REQUIRED`            | `426`  |
| `HTTP_STATUS_SERVER_ERROR`                | `500`  |
| `HTTP_STATUS_NOT_IMPLEMENTED`             | `501`  |
| `HTTP_STATUS_BAD_GATEWAY`                 | `502`  |
| `HTTP_STATUS_SERVICE_UNAVAILABLE`         | `503`  |
| `HTTP_STATUS_GATEWAY_TIMEOUT`             | `504`  |
| `HTTP_STATUS_NOT_SUPPORTED`               | `505`  |
| `HTTP_STATUS_CUPS_AUTHORIZATION_CANCELED` | `1000` |
| `HTTP_STATUS_CUPS_PKI_ERROR`              | `1001` |

Legacy names (`HTTP_*` without the `STATUS_` prefix) are also exported with identical values.

---

### PPD UI Constants (`PPD_UI_*`)

| Constant          | Value |
| ----------------- | ----- |
| `PPD_UI_BOOLEAN`  | `0`   |
| `PPD_UI_PICKONE`  | `1`   |
| `PPD_UI_PICKMANY` | `2`   |

---

### PPD Order Dependency Constants (`PPD_ORDER_*`)

| Constant             | Value |
| -------------------- | ----- |
| `PPD_ORDER_ANY`      | `0`   |
| `PPD_ORDER_DOCUMENT` | `1`   |
| `PPD_ORDER_EXIT`     | `2`   |
| `PPD_ORDER_JCL`      | `3`   |
| `PPD_ORDER_PAGE`     | `4`   |
| `PPD_ORDER_PROLOG`   | `5`   |

---

### IPP Job State Constants (`IPP_JOB_*`)

| Constant             | Value |
| -------------------- | ----- |
| `IPP_JOB_PENDING`    | `3`   |
| `IPP_JOB_HELD`       | `4`   |
| `IPP_JOB_PROCESSING` | `5`   |
| `IPP_JOB_STOPPED`    | `6`   |
| `IPP_JOB_CANCELED`   | `7`   |
| `IPP_JOB_ABORTED`    | `8`   |
| `IPP_JOB_COMPLETED`  | `9`   |

---

### IPP Printer State Constants (`IPP_PRINTER_*`)

| Constant                 | Value |
| ------------------------ | ----- |
| `IPP_PRINTER_IDLE`       | `3`   |
| `IPP_PRINTER_PROCESSING` | `4`   |
| `IPP_PRINTER_STOPPED`    | `5`   |

---

### IPP Resolution Constants (`IPP_RES_*`)

| Constant           | Value |
| ------------------ | ----- |
| `IPP_RES_PER_INCH` | `3`   |
| `IPP_RES_PER_CM`   | `4`   |

---

### IPP Finishing Constants (`IPP_FINISHINGS_*`)

| Constant                             | Value             |
| ------------------------------------ | ----------------- |
| `IPP_FINISHINGS_NONE`                | `3`               |
| `IPP_FINISHINGS_STAPLE`              | `4`               |
| `IPP_FINISHINGS_PUNCH`               | `5`               |
| `IPP_FINISHINGS_COVER`               | `6`               |
| `IPP_FINISHINGS_BIND`                | `7`               |
| `IPP_FINISHINGS_SADDLE_STITCH`       | `8`               |
| `IPP_FINISHINGS_EDGE_STITCH`         | `9`               |
| `IPP_FINISHINGS_FOLD`                | `10`              |
| `IPP_FINISHINGS_TRIM`                | `11`              |
| `IPP_FINISHINGS_BALE`                | `12`              |
| `IPP_FINISHINGS_BOOKLET_MAKER`       | `13`              |
| `IPP_FINISHINGS_JOB_OFFSET`          | `14` (deprecated) |
| `IPP_FINISHINGS_STAPLE_TOP_LEFT`     | `20`              |
| `IPP_FINISHINGS_STAPLE_BOTTOM_LEFT`  | `21`              |
| `IPP_FINISHINGS_STAPLE_TOP_RIGHT`    | `22`              |
| `IPP_FINISHINGS_STAPLE_BOTTOM_RIGHT` | `23`              |
| `IPP_FINISHINGS_EDGE_STITCH_LEFT`    | `24`              |
| `IPP_FINISHINGS_EDGE_STITCH_TOP`     | `25`              |
| `IPP_FINISHINGS_EDGE_STITCH_RIGHT`   | `26`              |
| `IPP_FINISHINGS_EDGE_STITCH_BOTTOM`  | `27`              |
| `IPP_FINISHINGS_STAPLE_DUAL_LEFT`    | `28`              |
| `IPP_FINISHINGS_STAPLE_DUAL_TOP`     | `29`              |
| `IPP_FINISHINGS_STAPLE_DUAL_RIGHT`   | `30`              |
| `IPP_FINISHINGS_STAPLE_DUAL_BOTTOM`  | `31`              |
| `IPP_FINISHINGS_BIND_LEFT`           | `50`              |
| `IPP_FINISHINGS_BIND_TOP`            | `51`              |
| `IPP_FINISHINGS_BIND_RIGHT`          | `52`              |
| `IPP_FINISHINGS_BIND_BOTTOM`         | `53`              |

---

### IPP Orientation Constants (`IPP_ORIENT_*`)

| Constant                       | Value |
| ------------------------------ | ----- |
| `IPP_ORIENT_PORTRAIT`          | `3`   |
| `IPP_ORIENT_LANDSCAPE`         | `4`   |
| `IPP_ORIENT_REVERSE_LANDSCAPE` | `5`   |
| `IPP_ORIENT_REVERSE_PORTRAIT`  | `6`   |

Legacy names (`IPP_PORTRAIT`, etc.) are also exported with identical values.

---

### IPP Quality Constants (`IPP_QUALITY_*`)

| Constant             | Value |
| -------------------- | ----- |
| `IPP_QUALITY_DRAFT`  | `3`   |
| `IPP_QUALITY_NORMAL` | `4`   |
| `IPP_QUALITY_HIGH`   | `5`   |

---

### IPP Status Constants (`IPP_STATUS_*`)

| Constant                                         | Decimal | Hex      |
| ------------------------------------------------ | ------- | -------- |
| `IPP_STATUS_OK`                                  | `0`     | `0x0000` |
| `IPP_STATUS_OK_IGNORED_OR_SUBSTITUTED`           | `1`     | `0x0001` |
| `IPP_STATUS_OK_CONFLICTING`                      | `2`     | `0x0002` |
| `IPP_STATUS_OK_IGNORED_SUBSCRIPTIONS`            | `3`     | `0x0003` |
| `IPP_STATUS_OK_IGNORED_NOTIFICATIONS`            | `4`     | `0x0004` |
| `IPP_STATUS_OK_TOO_MANY_EVENTS`                  | `5`     | `0x0005` |
| `IPP_STATUS_OK_BUT_CANCEL_SUBSCRIPTION`          | `6`     | `0x0006` |
| `IPP_STATUS_OK_EVENTS_COMPLETE`                  | `7`     | `0x0007` |
| `IPP_STATUS_REDIRECTION_OTHER_SITE`              | `512`   | `0x0200` |
| `IPP_STATUS_ERROR_BAD_REQUEST`                   | `1024`  | `0x0400` |
| `IPP_STATUS_ERROR_FORBIDDEN`                     | `1025`  | `0x0401` |
| `IPP_STATUS_ERROR_NOT_AUTHENTICATED`             | `1026`  | `0x0402` |
| `IPP_STATUS_ERROR_NOT_AUTHORIZED`                | `1027`  | `0x0403` |
| `IPP_STATUS_ERROR_NOT_POSSIBLE`                  | `1028`  | `0x0404` |
| `IPP_STATUS_ERROR_TIMEOUT`                       | `1029`  | `0x0405` |
| `IPP_STATUS_ERROR_NOT_FOUND`                     | `1030`  | `0x0406` |
| `IPP_STATUS_ERROR_GONE`                          | `1031`  | `0x0407` |
| `IPP_STATUS_ERROR_REQUEST_ENTITY`                | `1032`  | `0x0408` |
| `IPP_STATUS_ERROR_REQUEST_VALUE`                 | `1033`  | `0x0409` |
| `IPP_STATUS_ERROR_DOCUMENT_FORMAT_NOT_SUPPORTED` | `1034`  | `0x040A` |
| `IPP_STATUS_ERROR_ATTRIBUTES_OR_VALUES`          | `1035`  | `0x040B` |
| `IPP_STATUS_ERROR_URI_SCHEME`                    | `1036`  | `0x040C` |
| `IPP_STATUS_ERROR_CHARSET`                       | `1037`  | `0x040D` |
| `IPP_STATUS_ERROR_CONFLICTING`                   | `1038`  | `0x040E` |
| `IPP_STATUS_ERROR_COMPRESSION_NOT_SUPPORTED`     | `1039`  | `0x040F` |
| `IPP_STATUS_ERROR_COMPRESSION_ERROR`             | `1040`  | `0x0410` |
| `IPP_STATUS_ERROR_DOCUMENT_FORMAT_ERROR`         | `1041`  | `0x0411` |
| `IPP_STATUS_ERROR_DOCUMENT_ACCESS`               | `1042`  | `0x0412` |
| `IPP_STATUS_ERROR_ATTRIBUTES_NOT_SETTABLE`       | `1043`  | `0x0413` |
| `IPP_STATUS_ERROR_IGNORED_ALL_SUBSCRIPTIONS`     | `1044`  | `0x0414` |
| `IPP_STATUS_ERROR_TOO_MANY_SUBSCRIPTIONS`        | `1045`  | `0x0415` |
| `IPP_STATUS_ERROR_IGNORED_ALL_NOTIFICATIONS`     | `1046`  | `0x0416` |
| `IPP_STATUS_ERROR_PRINT_SUPPORT_FILE_NOT_FOUND`  | `1047`  | `0x0417` |
| `IPP_STATUS_ERROR_INTERNAL`                      | `1280`  | `0x0500` |
| `IPP_STATUS_ERROR_OPERATION_NOT_SUPPORTED`       | `1281`  | `0x0501` |
| `IPP_STATUS_ERROR_SERVICE_UNAVAILABLE`           | `1282`  | `0x0502` |
| `IPP_STATUS_ERROR_VERSION_NOT_SUPPORTED`         | `1283`  | `0x0503` |
| `IPP_STATUS_ERROR_DEVICE`                        | `1284`  | `0x0504` |
| `IPP_STATUS_ERROR_TEMPORARY`                     | `1285`  | `0x0505` |
| `IPP_STATUS_ERROR_NOT_ACCEPTING_JOBS`            | `1286`  | `0x0506` |
| `IPP_STATUS_ERROR_BUSY`                          | `1287`  | `0x0507` |
| `IPP_STATUS_ERROR_JOB_CANCELED`                  | `1288`  | `0x0508` |
| `IPP_STATUS_ERROR_MULTIPLE_JOBS_NOT_SUPPORTED`   | `1289`  | `0x0509` |
| `IPP_STATUS_ERROR_PRINTER_IS_DEACTIVATED`        | `1290`  | `0x050A` |
| `IPP_STATUS_ERROR_CUPS_AUTHENTICATION_CANCELED`  | `4096`  | `0x1000` |
| `IPP_STATUS_ERROR_CUPS_PKI`                      | `4097`  | `0x1001` |
| `IPP_STATUS_ERROR_CUPS_UPGRADE_REQUIRED`         | `4098`  | `0x1002` |

Legacy names (`IPP_OK`, `IPP_NOT_FOUND`, etc.) are also exported with identical values. Note that `1030` (`IPP_STATUS_ERROR_NOT_FOUND`) is the code behind the common "The printer or class does not exist" error.

---

### IPP State Constants (`IPP_STATE_*`)

| Constant              | Value |
| --------------------- | ----- |
| `IPP_STATE_ERROR`     | `-1`  |
| `IPP_STATE_IDLE`      | `0`   |
| `IPP_STATE_HEADER`    | `1`   |
| `IPP_STATE_ATTRIBUTE` | `2`   |
| `IPP_STATE_DATA`      | `3`   |

Legacy names (`IPP_ERROR`, `IPP_IDLE`, etc.) are also exported with identical values.

---

### IPP Tag Constants (`IPP_TAG_*`)

| Constant            | Decimal | Hex    |
| ------------------- | ------- | ------ |
| `IPP_TAG_ZERO`      | `0`     | `0x00` |
| `IPP_TAG_OPERATION` | `1`     | `0x01` |
| `IPP_TAG_JOB`       | `2`     | `0x02` |
| `IPP_TAG_PRINTER`   | `4`     | `0x04` |
| `IPP_TAG_INTEGER`   | `33`    | `0x21` |
| `IPP_TAG_BOOLEAN`   | `34`    | `0x22` |
| `IPP_TAG_ENUM`      | `35`    | `0x23` |
| `IPP_TAG_STRING`    | `48`    | `0x30` |
| `IPP_TAG_RANGE`     | `51`    | `0x33` |
| `IPP_TAG_TEXT`      | `65`    | `0x41` |
| `IPP_TAG_NAME`      | `66`    | `0x42` |
| `IPP_TAG_KEYWORD`   | `68`    | `0x44` |
| `IPP_TAG_URI`       | `69`    | `0x45` |
| `IPP_TAG_CHARSET`   | `71`    | `0x47` |
| `IPP_TAG_LANGUAGE`  | `72`    | `0x48` |
| `IPP_TAG_MIMETYPE`  | `73`    | `0x49` |

---

### Server Administration Constants

These are string constants used as keys in the dictionaries returned by `Connection.adminGetServerSettings()` and passed to `Connection.adminSetServerSettings()`.

| Constant                      | Value                |
| ----------------------------- | -------------------- |
| `CUPS_SERVER_DEBUG_LOGGING`   | `"_debug_logging"`   |
| `CUPS_SERVER_REMOTE_ADMIN`    | `"_remote_admin"`    |
| `CUPS_SERVER_REMOTE_ANY`      | `"_remote_any"`      |
| `CUPS_SERVER_REMOTE_PRINTERS` | `"_remote_printers"` |
| `CUPS_SERVER_SHARE_PRINTERS`  | `"_share_printers"`  |
| `CUPS_SERVER_USER_CANCEL_ANY` | `"_user_cancel_any"` |
