# nrf-sdk-tools
A collection of scripts and useful things in relation to the Nordic nRF SDKs

#copyExample.py
Yup, even something simple like copying a example project out of the SDK can be a giant pain. I don't agree to the sentiment that development should be done within the example SDK path, there is no way I'll do that. That's just wrong. So to never have to edit the projectfiles again I of course made a script.

## Usage
    python nrf-skd-tools/15.2/copyExample.py <sdk path> <example to copy from> <where you'd like the example to be put>

## Example
    python nrf-sdk-tools/15.2/copyExample.py nRF5_SDK_15.2.0/ nRF5_SDK_15.2.0/examples/ble_peripheral/ble_app_hids_mouse nrf52-media-ctrl

## Program flow
- Copies the SDK example to the destination path
- Removes all projects that are not Segger Embedded Studio
- Locates all *.emProject files, and replaces all relative references to SDK with $(SDK). It first checks whether the file is local in the example, so it does not reference the SDK main.c for example.

## Segger Embedded Studio setup
You need to setup a global macro that points to the SDK. In Segger Embedded Studio, do Tools -> Options -> Building, find the Global Macros line, and add the macro for SDK, for example 
    SDK=/Users/wulff/pro/nRF5_SDK_15.2.0
